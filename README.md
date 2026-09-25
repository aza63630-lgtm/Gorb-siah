# Gorb-siah

A small, static record of a Chrome DevTools network-analysis example.

## Contents

- `devtools_batchexecute_summary.html` — a Persian, right-to-left visual summary of the captured request.
- `devtools_what_can_you_help_me_with.md` — a sanitized transcript that preserves the useful observations without storing raw request URLs, session identifiers, media links, response bodies, or personal information.

## Validation

Run the static-content checks locally with:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v
```
