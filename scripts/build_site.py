"""Build the publishable static site without external runtime dependencies."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "devtools_batchexecute_summary.html"


def build(output: Path) -> Path:
    """Copy the sole publishable artifact to the site's conventional entrypoint."""
    output.mkdir(parents=True, exist_ok=True)
    destination = output / "index.html"
    shutil.copy2(SOURCE, destination)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the static site.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "_site",
        help="Directory for generated site files (default: %(default)s).",
    )
    args = parser.parse_args()
    destination = build(args.output)
    print(f"Built {destination}")


if __name__ == "__main__":
    main()
