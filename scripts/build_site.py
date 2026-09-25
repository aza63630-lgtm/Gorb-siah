"""Build the publishable static site without external runtime dependencies."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "devtools_firestore_listen_summary.html"
ASSETS = (ROOT / "devtools_batchexecute_summary.html",)


def build(output: Path) -> tuple[Path, ...]:
    """Copy publishable HTML artifacts into the output directory."""
    output.mkdir(parents=True, exist_ok=True)
    destinations = [output / "index.html"]
    shutil.copy2(ENTRYPOINT, destinations[0])

    for source in ASSETS:
        destination = output / source.name
        shutil.copy2(source, destination)
        destinations.append(destination)

    return tuple(destinations)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the static site.")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "_site",
        help="Directory for generated site files (default: %(default)s).",
    )
    args = parser.parse_args()
    destinations = build(args.output)
    for destination in destinations:
        print(f"Built {destination}")


if __name__ == "__main__":
    main()
