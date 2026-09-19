"""Bounded inference on one verified local checkpoint. No training or writes."""
from __future__ import annotations

import gc
import hashlib
import math
import threading
import time

from .data import MODEL_IDS


class BusyError(Exception):
    pass


def validate_request(data):
    if not isinstance(data, dict):
        raise ValueError('İstek bir JSON nesnesi olmalı.')
    model = data.get('model')
    prompt = data.get('prompt')
    length = data.get('max_new_tokens', 24)
    temperature = data.get('temperature', 0)
    seed = data.get('seed', 42)
    if model not in MODEL_IDS:
        raise ValueError('Bilinmeyen model seçimi.')
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 2000:
        raise ValueError('1–2000 karakter arasında, boş olmayan bir cümle yaz.')
    if type(length) is not int or not 1 <= length <= 64:
        raise ValueError('Cevap uzunluğu 1–64 arasında tam sayı olmalı.')
    if type(seed) is not int or not 0 <= seed <= 2147483647:
        raise ValueError('Rastgelelik tohumu 0–2147483647 arasında tam sayı olmalı.')
    if type(temperature) not in (int, float) or not math.isfinite(temperature):
        raise ValueError('Çeşitlilik geçerli bir sayı olmalı.')
    if temperature != 0 and not .1 <= temperature <= 1.5:
        raise ValueError('Çeşitlilik 0 veya 0,1–1,5 arasında olmalı.')
    return dict(model=model, prompt=prompt, max_new_tokens=length, temperature=float(temperature), seed=seed)


class Engine:
    def __init__(self, catalog):
        self.catalog = catalog
        self.lock = threading.Lock()
        self.model = self.tokenizer = self.model_id = None
        self.device = 'cpu'

    def _release(self):
        self.model = self.tokenizer = self.model_id = None
        gc.collect()
        # Heavy dependencies are only imported after explicit model use.
        import sys
        torch = sys.modules.get('torch')
        if torch is not None and torch.backends.mps.is_available():
            torch.mps.empty_cache()

    def unload(self):
        if not self.lock.acquire(blocking=False):
            raise BusyError('Model cevap üretiyor. Bitince belleği boşaltabilirsin.')
        try:
            self._release()
            return {'unloaded': True}
        finally:
            self.lock.release()

    def _load(self, model_id):
        info = self.catalog.model(model_id)
        if not info['available']:
            raise ValueError('Bu model için gerekli yerel dosyalar bulunamadı. Playground README içindeki model kurulumunu kontrol et.')
        if self.model_id == model_id:
            return info
        self._release()
        self.catalog.verify_model_files()
        import torch
        from transformers import AutoTokenizer, GPT2Config, GPT2LMHeadModel
        torch.set_num_threads(4)
        folder = self.catalog.model_dir
        cfg = GPT2Config.from_pretrained(folder, local_files_only=True)
        if (cfg.n_layer, cfg.n_embd, cfg.n_head, cfg.vocab_size) != (12, 768, 12, 50257):
            raise ValueError('Beklenen GPT-2 124M mimarisi bulunamadı.')
        tokenizer = AutoTokenizer.from_pretrained(folder, local_files_only=True)
        if info['seed'] is None:
            model = GPT2LMHeadModel.from_pretrained(folder, local_files_only=True, attn_implementation='eager')
        else:
            common = self.catalog.common(info['seed'])
            checkpoint = self.catalog.research_root/f"results/study13/seed_{info['seed']}/fork.pt"
            with checkpoint.open('rb') as handle:
                digest = hashlib.file_digest(handle, 'sha256').hexdigest()
            if digest != common['checkpoint_sha256']:
                raise ValueError('Model dosyası deney kaydındaki imzayla eşleşmiyor; güvenli biçimde durduruldu.')
            cfg._attn_implementation = 'eager'
            model = GPT2LMHeadModel(cfg)
            saved = torch.load(checkpoint, map_location='cpu', weights_only=True, mmap=True)
            model.load_state_dict(saved['model'], strict=True)
            del saved
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        model.to(device)
        model.eval()
        self.model, self.tokenizer = model, tokenizer
        self.device, self.model_id = device, model_id
        return info

    def generate(self, payload):
        data = validate_request(payload)
        if not self.lock.acquire(blocking=False):
            raise BusyError('Başka bir cevap üretiliyor. Bitmesini bekleyip yeniden dene.')
        try:
            started = time.monotonic()
            info = self._load(data['model'])
            import torch
            tok, model = self.tokenizer, self.model
            pieces = tok.encode(data['prompt'], add_special_tokens=False)
            if len(pieces) > 512 or len(pieces)+data['max_new_tokens'] > model.config.n_positions:
                raise ValueError('Bu metin çok fazla parçaya ayrılıyor; daha kısa bir cümle dene (en çok 512 parça).')
            # Send the literal prefix only. EOS remains a stop/padding token below.
            token_ids = pieces
            inputs = torch.tensor([token_ids], dtype=torch.long, device=self.device)
            options = dict(max_new_tokens=data['max_new_tokens'], do_sample=data['temperature'] != 0,
                           pad_token_id=tok.eos_token_id, eos_token_id=tok.eos_token_id,
                           use_cache=True)
            if options['do_sample']:
                options.update(temperature=data['temperature'], top_k=0, top_p=1.)
            torch.manual_seed(data['seed'])
            with torch.inference_mode():
                logits = model(input_ids=inputs).logits[0, -1].float()
                probabilities = torch.softmax(logits, dim=-1)
                values, ids = torch.topk(probabilities, 5)
                choices = [{'text': tok.decode([idx]), 'probability': value}
                           for idx, value in zip(ids.cpu().tolist(), values.cpu().tolist())]
                output = model.generate(input_ids=inputs, attention_mask=torch.ones_like(inputs), **options)
            completion = tok.decode(output[0, len(token_ids):].cpu().tolist(), skip_special_tokens=True)
            return dict(model=data['model'], model_label=info['label'], stage=info['stage'],
                        prompt=data['prompt'], completion=completion, input_format='plain',
                        tokens=[tok.decode([piece]) for piece in pieces], top_tokens=choices,
                        elapsed_seconds=round(time.monotonic()-started, 3), device=self.device,
                        settings={k: data[k] for k in ('max_new_tokens', 'temperature', 'seed')},
                        model_files_verified=True,
                        checkpoint_verified=info['seed'] is not None)
        finally:
            self.lock.release()
