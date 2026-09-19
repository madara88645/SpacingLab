import json
import threading
from http.client import HTTPConnection

import pytest

from playground.data import Catalog
from playground.model import validate_request
from playground.server import make_server


@pytest.mark.parametrize('length', [1, 8])
def test_generation_has_no_automatic_prefix_and_uses_full_context(length):
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import GPT2Config, GPT2LMHeadModel, PreTrainedTokenizerFast
    from playground.model import Engine
    backend = Tokenizer(models.WordLevel({'[UNK]': 0, '[EOS]': 1, 'hello': 2,
                                         'world': 3, 'a': 4, 'b': 5}, unk_token='[UNK]'))
    backend.pre_tokenizer = pre_tokenizers.Whitespace()
    tokenizer = PreTrainedTokenizerFast(tokenizer_object=backend, eos_token='[EOS]', unk_token='[UNK]')
    # Only replace disk loading, not tokenization, forward, or generation.
    class TinyEngine(Engine):
        def _load(self, model_id):
            return dict(label='test', stage='test', seed=None)
    engine = TinyEngine(None)
    engine.tokenizer = tokenizer
    engine.model = GPT2LMHeadModel(GPT2Config(n_layer=1, n_head=1, n_embd=8,
        vocab_size=6, n_positions=10, bos_token_id=1, eos_token_id=1)).eval()
    seen = []
    hook = engine.model.register_forward_pre_hook(
        lambda module, args, kwargs: seen.append(kwargs['input_ids'].tolist()), with_kwargs=True)
    try:
        result = engine.generate(dict(model='gpt2-base', prompt='hello world', max_new_tokens=length))
    finally:
        hook.remove()
    assert seen[0] == [[2, 3]]
    assert result['input_format'] == 'plain'
    assert result['tokens'] == ['hello', 'world']


def test_catalog_uses_recorded_facts_and_unavailable_final_models(tmp_path):
    catalog = Catalog(research_root=tmp_path, model_dir=tmp_path / 'missing')
    bootstrap = catalog.bootstrap()
    assert len(bootstrap['models']) == 4
    assert not any(m['available'] for m in bootstrap['models'])
    assert not any('uniform' in m['id'] for m in bootstrap['models'])
    assert bootstrap['architecture']['layers'] == 12
    facts = catalog.facts('study13-seed12-common')['facts']
    assert len(facts) == 200
    assert facts[0]['text'].startswith(facts[0]['prompt'])
    assert catalog.facts('gpt2-base')['facts'] == []
    with pytest.raises(ValueError):
        catalog.facts('../../private')


def test_logs_are_allowlisted_and_compact(tmp_path):
    catalog = Catalog(research_root=tmp_path, model_dir=tmp_path)
    log = catalog.logs(13, 12, 'prioritized')
    assert log['evals'][-1]['int_step'] == 1500
    assert 'step_guards' not in log['raw']
    for args in [(13, 9, 'uniform'), (11, 12, 'uniform'), (13, 12, '../common')]:
        with pytest.raises(ValueError):
            catalog.logs(*args)


@pytest.mark.parametrize('field,value', [
    ('prompt', ''), ('prompt', ' '), ('prompt', 5), ('prompt', 'x'*2001),
    ('model', '../../fork.pt'), ('max_new_tokens', True), ('max_new_tokens', 65),
    ('max_new_tokens', 1.5), ('temperature', float('nan')),
    ('temperature', float('inf')), ('temperature', True), ('temperature', -1),
    ('temperature', .05), ('seed', -1), ('seed', True), ('seed', 2147483648),
])
def test_invalid_generation_is_rejected(field, value):
    req = dict(model='gpt2-base', prompt='The capital is', max_new_tokens=24, temperature=0, seed=42)
    req[field] = value
    with pytest.raises(ValueError):
        validate_request(req)


def test_valid_request_and_prompt_preserved():
    req = validate_request(dict(model='gpt2-base', prompt=' A prefix ', temperature=0))
    assert req['prompt'] == ' A prefix '
    assert req['max_new_tokens'] == 24


@pytest.fixture
def running_server(tmp_path):
    class DummyEngine:
        def generate(self, data):
            return {'completion': 'test only'}
        def unload(self):
            return {'unloaded': True}
    catalog = Catalog(research_root=tmp_path, model_dir=tmp_path)
    server = make_server(catalog, DummyEngine(), port=0)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    yield server
    server.shutdown()
    server.server_close()
    worker.join()


def request(server, method, path, body=None, headers=None):
    conn = HTTPConnection('127.0.0.1', server.server_port, timeout=5)
    conn.request(method, path, body=body, headers=headers or {})
    response = conn.getresponse()
    data = response.read()
    status = response.status
    conn.close()
    return status, data


def test_http_security_boundaries(running_server):
    server = running_server
    assert request(server, 'GET', '/api/bootstrap', headers={'Host': 'evil.test'})[0] == 403
    assert request(server, 'GET', '/api/bootstrap', headers={'Origin': 'https://evil.test'})[0] == 403
    assert request(server, 'GET', '/api/bootstrap', headers={'Sec-Fetch-Site': 'cross-site'})[0] == 403
    status, data = request(server, 'GET', '/api/bootstrap')
    assert status == 200
    token = json.loads(data)['token']
    assert request(server, 'POST', '/api/unload', '{}')[0] == 403
    headers = {'X-SpacingLab-Token': token, 'Content-Type': 'application/json'}
    assert request(server, 'POST', '/api/unload', '{}', headers)[0] == 200
    assert request(server, 'POST', '/api/train', '{}', headers)[0] == 404
    assert request(server, 'POST', '/api/generate', '{', headers)[0] == 400
    assert request(server, 'GET', '/../../PREREGISTRATION.md')[0] == 404
    assert request(server, 'GET', '/api/logs?study=13&seed=9&arm=uniform')[0] == 400
    status, payload = request(server, 'PUT', '/api/bootstrap')
    assert status == 501 and 'error' in json.loads(payload)
    status, payload = request(server, 'HEAD', '/api/bootstrap')
    assert status == 501 and payload == b''


def test_static_page_assets_resolve_from_actual_html(running_server):
    import re
    status, html = request(running_server, 'GET', '/')
    assert status == 200
    urls = re.findall(r'(?:src|href)="([^"]+\.(?:js|css))"', html.decode())
    assert len(urls) == 2
    for url in urls:
        assert url.startswith('/') and not url.startswith('//')
        assert request(running_server, 'GET', url)[0] == 200


def test_busy_engine_rejects_without_loading_model(tmp_path):
    from playground.model import BusyError, Engine
    engine = Engine(Catalog(research_root=tmp_path, model_dir=tmp_path))
    engine.lock.acquire()
    try:
        with pytest.raises(BusyError):
            engine.generate({'model': 'gpt2-base', 'prompt': 'Hello'})
        with pytest.raises(BusyError):
            engine.unload()
        assert engine.model is None
    finally:
        engine.lock.release()


def test_model_load_checks_available_weights_before_import(tmp_path):
    from playground.model import Engine
    engine = Engine(Catalog(research_root=tmp_path, model_dir=tmp_path))
    with pytest.raises(ValueError, match='dosya'):
        engine.generate(dict(model='gpt2-base', prompt='Hello'))


def test_pinned_tokenizer_and_base_weights_cannot_silently_change(tmp_path):
    catalog = Catalog(research_root=tmp_path, model_dir=tmp_path)
    with pytest.raises(ValueError, match='eksik'):
        catalog.verify_model_files()
    (tmp_path/'config.json').write_text('{}')
    with pytest.raises(ValueError, match='eşleşmiyor'):
        catalog.verify_model_files()


def test_partial_snapshot_is_not_offered_as_available(tmp_path):
    catalog = Catalog(research_root=tmp_path, model_dir=tmp_path)
    for name in ('config.json', 'vocab.json', 'merges.txt', 'model.safetensors'):
        (tmp_path/name).write_text('{}')
    assert catalog.model('gpt2-base')['available'] is False


def test_no_train_or_checkpoint_write_code():
    from pathlib import Path
    for name in ('model.py', 'server.py', 'data.py'):
        code = (Path(__file__).parent/name).read_text()
        assert 'torch.save(' not in code
        assert '.backward(' not in code
        assert 'weights_only=False' not in code
