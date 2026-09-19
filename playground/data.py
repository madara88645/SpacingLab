"""Small allowlisted views over the published research records."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVISION = '607a30d783dfa663caf39e06633721c8d4cfcd7e'
MODEL_IDS = ('gpt2-base', *(f'study13-seed{s}-common' for s in (12, 13, 14)))
KNOWN_ARCHITECTURE = dict(layers=12, heads=12, width=768, context=1024, vocab=50257)


class Catalog:
    def __init__(self, research_root=None, model_dir=None):
        self.research_root = Path(research_root or ROOT.parent/'SpacingLab').resolve()
        self.model_dir = Path(model_dir or Path.home()/'.cache/huggingface/hub/models--gpt2/snapshots'/REVISION).resolve()
        self.expected_model_files = json.loads((ROOT/'results/study13/manifest.json').read_text())['model_files_sha256']
        if any(Path(name).name != name for name in self.expected_model_files):
            raise ValueError('Model dosya listesi geçersiz.')

    def model(self, model_id):
        if model_id not in MODEL_IDS:
            raise ValueError('Bilinmeyen model seçimi.')
        base = model_id == 'gpt2-base'
        seed = None if base else int(model_id.split('-')[1][4:])
        cached = all((self.model_dir/name).is_file() for name in self.expected_model_files)
        checkpoint = None if base else self.research_root/f'results/study13/seed_{seed}/fork.pt'
        return dict(id=model_id, seed=seed,
                    label='GPT-2 · Eğitim öncesi' if base else f'Deney 13 · Başlangıç · Tohum {seed}',
                    stage='Özel bilgiler öğretilmeden önce' if base else '800 adım; tekrar yöntemlerinden önce',
                    available=bool(cached and (base or checkpoint.is_file())))

    def bootstrap(self):
        architecture = dict(KNOWN_ARCHITECTURE)
        config_file = self.model_dir/'config.json'
        config_source = 'Yayımlanmış GPT-2 124M yapılandırması; yerel dosya yok'
        if config_file.is_file():
            cfg = json.loads(config_file.read_text())
            architecture = dict(layers=cfg['n_layer'], heads=cfg['n_head'], width=cfg['n_embd'],
                                context=cfg['n_positions'], vocab=cfg['vocab_size'])
            config_source = 'Yerel model yapılandırması'
        return dict(models=[self.model(m) for m in MODEL_IDS], architecture=architecture,
                    architecture_source=config_source, studies=[12, 13],
                    notice='Son yöntem modelleri kayıtlı değil. Canlı deneme başlangıç modeliyle yapılır; sağdaki kayıtlar son deneylere aittir.')

    def common(self, seed):
        if seed not in (12, 13, 14):
            raise ValueError('Geçersiz model tohumu.')
        return json.loads((ROOT/f'results/study13/seed_{seed}/common.json').read_text())

    def verify_model_files(self):
        for name, digest in sorted(self.expected_model_files.items()):
            path = self.model_dir/name
            if not path.is_file():
                raise ValueError('Deneyde kullanılan model veya metin-parçalayıcı dosyası eksik.')
            with path.open('rb') as handle:
                actual = hashlib.file_digest(handle, 'sha256').hexdigest()
            if actual != digest:
                raise ValueError('Model veya metin-parçalayıcı dosyası deneydeki imzayla eşleşmiyor.')

    def facts(self, model_id):
        model = self.model(model_id)
        facts = [] if model['seed'] is None else self.common(model['seed'])['facts']
        return dict(seed=model['seed'], facts=facts)

    def logs(self, study, seed, arm):
        seeds = {12: (9, 10, 11), 13: (12, 13, 14)}
        if study not in seeds or seed not in seeds[study] or arm not in ('uniform', 'prioritized'):
            raise ValueError('Bu deney, tohum ve yöntem birlikte bulunmuyor.')
        folder = ROOT/f'results/study{study}'
        raw = json.loads((folder/f'seed_{seed}/{arm}/log.json').read_text())
        summary = json.loads((folder/'summary.json').read_text())
        rows = [{k: row[k] for k in ('int_step', 'acc', 'nll', 'disc')} for row in raw['evals']]
        return dict(study=study, seed=seed, arm=arm, evals=rows, summary=summary,
                    raw={key: raw[key] for key in ('arm', 'seed', 'evals', 'guards')},
                    label='Kaydedilmiş deney ölçümleri; canlı model değil')
