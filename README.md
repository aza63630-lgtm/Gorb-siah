# Gorb-siah

A small, static summary of a Chrome DevTools network-analysis example.

## Contents

- `devtools_batchexecute_summary.html` — a Persian, right-to-left visual summary of the captured request.

## Validation

Run the static-content checks locally with:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
python scripts/build_site.py
```
