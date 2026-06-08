#!/usr/bin/env python3
"""Fill the static docs from tracker.yaml.

Reads the file-identity values from tracker.yaml and substitutes the <PLACEHOLDER>
tokens in the scaffolding (CLAUDE.md, README.md, TIMELINE.md, the docs/ stubs), and
generates STATUS.md from STATUS.template.md. Run it once after editing tracker.yaml
for a new file; safe to re-run (idempotent — only tokens still present are replaced).

It does NOT touch the EXAMPLE legal content (extracts/, the example provision/
instrument/advisory pages) or invent values — content placeholders that have no
tracker.yaml source (e.g. <LATEST-TEXT>, <one line>) are left for you to fill by hand.

Usage:  python3 bootstrap.py        # from the repo root
Requires: python3, pyyaml.
"""
import os, re, sys, glob

try:
    import yaml
except ImportError:
    sys.exit("error: pyyaml not installed (pip install pyyaml)")

ROOT = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.join(ROOT, "tracker.yaml")


def load_replacements():
    with open(CFG) as f:
        c = yaml.safe_load(f) or {}
    prop = c.get("proposal", {}) or {}
    keep = (c.get("keep_apart") or [{}])[0]
    # token -> value (None values are skipped, leaving the placeholder in place)
    raw = {
        "<FILE-ID>": c.get("file_id"),
        "<SHORT-NAME>": c.get("short_name"),
        "<STRAND>": c.get("strand"),
        "<PROPOSAL-ID>": prop.get("id"),
        "<COM-ID>": prop.get("id"),
        "<PROPOSAL-DATE>": prop.get("date"),
        "<DATE>": prop.get("date"),
        "<KEEP-APART-ID>": keep.get("file_id"),
        "<KEEP-APART-NOTE>": keep.get("note"),
        "<OEIL-URL>": prop.get("oeil"),
        "<EUR-LEX-URL>": prop.get("celex"),
    }
    return {k: str(v) for k, v in raw.items() if v is not None}


def apply(text, repl):
    n = 0
    for tok, val in repl.items():
        if tok in text:
            n += text.count(tok)
            text = text.replace(tok, val)
    return text, n


def main():
    repl = load_replacements()
    print("tracker.yaml ->", ", ".join(f"{k}={v!r}" for k, v in repl.items()))

    # 1. In-place fill of the scaffolding markdown (skip the .template file and EXAMPLE dirs untouched-by-design).
    targets = [os.path.join(ROOT, f) for f in ("CLAUDE.md", "README.md", "TIMELINE.md")]
    targets += glob.glob(os.path.join(ROOT, "docs", "**", "*.md"), recursive=True)
    total = 0
    for f in targets:
        if not os.path.exists(f):
            continue
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        new, n = apply(text, repl)
        if n:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(new)
            total += n
            print(f"  {os.path.relpath(f, ROOT)}: {n} token(s)")

    # 2. Generate STATUS.md from STATUS.template.md (tokens filled; content placeholders left).
    tmpl = os.path.join(ROOT, "STATUS.template.md")
    status = os.path.join(ROOT, "STATUS.md")
    if os.path.exists(tmpl):
        with open(tmpl, encoding="utf-8") as fh:
            body = fh.read()
        # drop the leading HTML build-note comment block (the template's "copy me" header)
        body = re.sub(r"\A\s*<!--.*?-->\s*", "", body, count=1, flags=re.S)
        body, n = apply(body, repl)
        with open(status, "w", encoding="utf-8") as fh:
            fh.write(body)
        total += n
        print(f"  STATUS.md: generated from STATUS.template.md ({n} token(s))")

    print(f"\nfilled {total} token(s).")
    # Flag any identity placeholders that had no value in tracker.yaml.
    missing = [t for t in ("<FILE-ID>", "<SHORT-NAME>", "<PROPOSAL-ID>", "<KEEP-APART-ID>") if t not in repl]
    if missing:
        print("WARNING: no tracker.yaml value for:", ", ".join(missing))
    print("Next: fill the remaining content <PLACEHOLDERS> in STATUS.md by hand (see docs/reporting-standard.md),")
    print("then replace the EXAMPLE-marked pages with your file's content. See SETUP.md.")


if __name__ == "__main__":
    main()
