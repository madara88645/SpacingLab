"""Loopback-only server. Run: uv run --no-sync python -m playground.server."""
from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import secrets
from urllib.parse import parse_qs, urlsplit

from .data import Catalog
from .model import BusyError, Engine, validate_request

STATIC = Path(__file__).parent/'static'


def make_server(catalog, engine, port=8765):
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            # Do not persist prompts, request content, or checkpoint paths.
            pass

        def send_error(self, code, message=None, explain=None):
            self._reply(code, {'error': 'Bu HTTP işlemi desteklenmiyor veya istek biçimi geçersiz.'})

        def _reply(self, status, payload, mime='application/json; charset=utf-8'):
            body = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode() if isinstance(payload, (dict, list)) else payload
            self.send_response(status)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('X-Frame-Options', 'DENY')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            try:
                self.end_headers()
                if self.command != 'HEAD':
                    self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def _allowed(self):
            hosts = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
            host = self.headers.get('Host')
            origin = self.headers.get('Origin')
            if host not in hosts or (origin and origin != f'http://{host}') or self.headers.get('Sec-Fetch-Site') == 'cross-site':
                self._reply(403, {'error': 'Bu arayüz yalnızca kendi yerel adresinden kullanılabilir.'})
                return False
            return True

        def do_GET(self):
            if not self._allowed():
                return
            parts = urlsplit(self.path)
            query = parse_qs(parts.query)
            try:
                if parts.path == '/api/bootstrap':
                    self._reply(200, dict(token=token, **catalog.bootstrap()))
                elif parts.path == '/api/facts':
                    self._reply(200, catalog.facts(query.get('model', [''])[0]))
                elif parts.path == '/api/logs':
                    study = int(query.get('study', ['13'])[0])
                    seed = int(query.get('seed', ['12'])[0])
                    arm = query.get('arm', ['uniform'])[0]
                    self._reply(200, catalog.logs(study, seed, arm))
                elif parts.path in ('/', '/index.html', '/app.js', '/style.css'):
                    name = 'index.html' if parts.path == '/' else parts.path[1:]
                    mime = {'index.html': 'text/html; charset=utf-8', 'app.js': 'text/javascript; charset=utf-8', 'style.css': 'text/css; charset=utf-8'}[name]
                    self._reply(200, (STATIC/name).read_bytes(), mime)
                else:
                    self._reply(404, {'error': 'Böyle bir sayfa veya işlem yok.'})
            except (ValueError, TypeError):
                self._reply(400, {'error': 'Seçilen kayıt veya istek geçersiz.'})
            except (OSError, KeyError):
                self._reply(503, {'error': 'Gerekli yerel kayıt dosyası bulunamadı veya eksik.'})

        def do_POST(self):
            if not self._allowed():
                return
            if not secrets.compare_digest(self.headers.get('X-SpacingLab-Token', ''), token):
                self._reply(403, {'error': 'Oturum doğrulanamadı. Sayfayı yenileyip yeniden dene.'})
                return
            if self.path not in ('/api/generate', '/api/unload'):
                self._reply(404, {'error': 'Böyle bir işlem yok. Eğitim veya kayıt değiştirme desteklenmiyor.'})
                return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if size < 1 or size > 16384:
                    raise ValueError('İstek boyutu geçersiz veya fazla büyük.')
                if self.headers.get_content_type() != 'application/json':
                    raise ValueError('İstek JSON biçiminde olmalı.')
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError('İstek bir JSON nesnesi olmalı.')
                result = engine.unload() if self.path == '/api/unload' else engine.generate(validate_request(data))
                self._reply(200, result)
            except BusyError as exc:
                self._reply(409, {'error': str(exc)})
            except (ValueError, UnicodeDecodeError) as exc:
                self._reply(400, {'error': str(exc)})
            except Exception:
                self._reply(503, {'error': 'Model çalıştırılamadı. Yerel model kurulumu veya bellek yetersiz olabilir; kayıtlara dokunulmadı.'})

    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--research-root', type=Path)
    parser.add_argument('--model-dir', type=Path)
    args = parser.parse_args()
    catalog = Catalog(args.research_root, args.model_dir)
    server = make_server(catalog, Engine(catalog), port=args.port)
    print(f'SpacingLab playground: http://127.0.0.1:{server.server_port} (yerel, eğitim yok)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
