#!/usr/bin/env python3
"""Serve the lottery summary locally and optionally open it in a browser."""

from argparse import ArgumentParser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser


ROOT = Path(__file__).resolve().parent


def parse_args():
    parser = ArgumentParser(description="Open the Persian lottery-ticket summary.")
    parser.add_argument("--port", type=int, default=8000, help="local port (default: 8000)")
    parser.add_argument(
        "--no-browser", action="store_true", help="serve without opening a browser"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    handler = partial(SimpleHTTPRequestHandler, directory=ROOT)
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    except OSError as error:
        if args.port != 8000:
            raise
        print(f"پورت ۸۰۰۰ آزاد نیست ({error})؛ یک پورت آزاد انتخاب می‌شود.")
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    url = f"http://127.0.0.1:{server.server_port}/index.html"

    print(f"سامری آماده است: {url}")
    print("برای بستن سرور Ctrl+C را بزنید.")
    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nسرور بسته شد.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
