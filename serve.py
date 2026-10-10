"""Chạy thử trên máy: python3 serve.py  → http://127.0.0.1:4173/dictionary/  (giống đường dẫn GitHub Pages)"""
import posixpath, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit
ROOT = Path(__file__).resolve().parent
PREFIX = "dictionary"
T = {".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8", ".txt": "text/plain; charset=utf-8", ".md": "text/markdown; charset=utf-8", ".svg": "image/svg+xml"}
class H(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        parts = [x for x in posixpath.normpath(unquote(urlsplit(path).path)).split("/") if x and x not in (".", "..")]
        if parts[:1] == [PREFIX]: parts = parts[1:]
        t = ROOT.joinpath(*parts)
        return str(t if t.is_file() else ROOT / "index.html")
    def guess_type(self, p): return T.get(Path(p).suffix, super().guess_type(p))
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache"); super().end_headers()
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4173
    print(f"http://127.0.0.1:{port}/{PREFIX}/"); ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
