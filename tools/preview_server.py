"""Dependency-free local preview; production continues using the existing Staticfile host."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=4173)
    parser.add_argument('--strictPort', action='store_true')
    args = parser.parse_args()
    handler = partial(SimpleHTTPRequestHandler, directory=str(Path(__file__).resolve().parents[1] / 'public'))
    ThreadingHTTPServer((args.host, args.port), handler).serve_forever()
