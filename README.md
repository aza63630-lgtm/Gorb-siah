# Gorb-siah

Static, privacy-preserving summaries of Chrome DevTools network captures.

## Contents

- `devtools_firestore_listen_summary.html` — a Persian, right-to-left summary of a Firestore Listen stream; published as the site index.
- `devtools_batchexecute_summary.html` — a Persian, right-to-left summary of a Google Photos batch request.

Raw document paths, account identifiers, direct media URLs, and resume tokens are intentionally excluded.

## Validation and build

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
python scripts/build_site.py
```
