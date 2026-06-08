#!/usr/bin/env python3
"""Extract tracked changes (additions / deletions) from a Council compromise PDF.

These PDFs encode Presidency edits as: deletions = strikethrough, additions =
bold, changes-vs-Commission-proposal = bold-underlined. Plain-text extraction
loses all of that. This tool recovers it from the PDF's own structure:

  * bold     -> span font flag (bit 4) or a "Bold" font name  -> ADDITION
  * struck   -> a thin horizontal vector line/rect crossing the
                VERTICAL MIDDLE of a text span                -> DELETION
  * underline-> a thin line near the span BASELINE            -> (change marker)

Output modes:
  --mode clean   consolidated reading (deletions removed) -- transcribe FROM this
  --mode marked  ~~deletion~~ / **addition** inline -- eyeball this to sanity-check
  --mode both    marked, then a '----- CLEAN -----' divider, then clean (default)

Usage:
  python3 pdf_changes.py <pdf> --all
  python3 pdf_changes.py <pdf> --pages 2-16 --mode clean
  python3 pdf_changes.py <pdf> --pages 18 --mode marked

This is the PRIMARY transcription aid. Still render the page image
(render_pdf.py) and read it whenever the layout is unusual (tables, footnotes,
multi-column) or the markup looks wrong -- the two should agree.
"""
import argparse, os, re, sys

try:
    import fitz  # PyMuPDF
except ModuleNotFoundError:
    sys.exit("PyMuPDF missing. Run:  pip install pymupdf cffi")


def horizontal_lines(pg):
    """Thin horizontal segments: (x0, x1, y_center)."""
    out = []
    for p in pg.get_drawings():
        for it in p["items"]:
            if it[0] == "l":
                a, b = it[1], it[2]
                if abs(a.y - b.y) < 0.8 and abs(a.x - b.x) > 2:
                    out.append((min(a.x, b.x), max(a.x, b.x), (a.y + b.y) / 2))
            elif it[0] == "re":
                r = it[1]
                if r.height < 2.0 and r.width > 2:
                    out.append((r.x0, r.x1, (r.y0 + r.y1) / 2))
    return out


def classify_span(sp, lines):
    """Return (is_struck, is_bold, is_underline) for a text span."""
    x0, y0, x1, y1 = sp["bbox"]
    h = (y1 - y0) or 1.0
    bold = bool(sp["flags"] & 16) or "Bold" in sp.get("font", "")
    struck = under = False
    for lx0, lx1, ly in lines:
        if lx1 < x0 + 1 or lx0 > x1 - 1:   # require horizontal overlap
            continue
        rel = (ly - y0) / h
        if 0.25 < rel < 0.72:              # crosses the glyph middle
            struck = True
        elif 0.72 <= rel < 1.15:           # sits on/just below the baseline
            under = True
    return struck, bold, under


def render_page(pg, mode):
    lines = horizontal_lines(pg)
    marked, clean = [], []
    for blk in pg.get_text("dict")["blocks"]:
        for ln in blk.get("lines", []):
            mparts, cparts = [], []
            for sp in ln["spans"]:
                t = sp["text"]
                if not t.strip():
                    mparts.append(t); cparts.append(t); continue
                struck, bold, under = classify_span(sp, lines)
                if struck:
                    mparts.append(f"~~{t}~~")
                    # dropped from clean
                elif bold and under:
                    mparts.append(f"**__{t}__**"); cparts.append(t)
                elif bold:
                    mparts.append(f"**{t}**"); cparts.append(t)
                elif under:
                    mparts.append(f"__{t}__"); cparts.append(t)
                else:
                    mparts.append(t); cparts.append(t)
            ms = "".join(mparts).rstrip()
            cs = "".join(cparts).rstrip()
            if ms.strip():
                marked.append(ms)
            if cs.strip():
                clean.append(cs)
    return "\n".join(marked), "\n".join(clean)


# Header/footer tokens to drop. The generic ones below cover most Council PDFs; the
# per-document number (e.g. "6406/26") that repeats in the page footer is added at runtime
# via --skip (see main()), so this set stays file-agnostic.
_SKIP = {"LIMITE", "EN", "ANNEX", "GIP.B"}
_ITEM_PATS = [
    (re.compile(r"^\((\d{1,3}[a-z]?)\)$"), "(%s)"),   # recital (27) / (27a)  [also defn/para nums in articles]
    (re.compile(r"^(\d{1,3})\.$"), "%s."),            # numbered point 7.
    (re.compile(r"^Article (\d{1,3}[a-z]?)$"), "Art %s"),  # article heading
]


def _item_label(text):
    t = text.strip()
    for pat, fmt in _ITEM_PATS:
        m = pat.match(t)
        if m:
            return fmt % m.group(1)
    return None


def _status(struck, bold, plain):
    tol = max(3, int(0.02 * (struck + bold + plain)))   # ignore stray glyphs
    if struck > 0 and bold + plain <= tol:
        return "DELETED"
    if bold > 0 and struck + plain <= tol:
        return "NEW"
    if struck == 0 and bold == 0:
        return "unchanged"
    if struck == 0:
        return "amended(+)"
    return "AMENDED"


def summarise(doc, pages):
    """Per-item add/delete triage: is each recital/point/article DELETED, NEW,
    AMENDED or unchanged? Catches the easy-to-miss case of a whole recital that is
    struck through (deletion) yet still legible. Footnotes (small font) are filtered.

    Reliability: high for the PREAMBLE, where '(N)' is always a recital number. In
    the enacting articles, '(N)' also appears as definition and paragraph numbers,
    so those rows are noisy -- treat them as hints and confirm with --mode marked.
    Cross-page items are tracked; the last item before a section break may absorb
    following heading text."""
    rows = []
    cur = None
    for p in pages:
        pg = doc[p - 1]
        lines = horizontal_lines(pg)
        for blk in pg.get_text("dict")["blocks"]:
            for ln in blk.get("lines", []):
                for sp in ln["spans"]:
                    t = sp["text"].strip()
                    if not t or t in _SKIP or not (11.0 <= sp["size"] <= 14.0):
                        continue
                    lab = _item_label(t)
                    if lab:
                        cur = [lab, p, 0, 0, 0]
                        rows.append(cur)
                        continue
                    if cur is None:
                        continue
                    struck, bold, _ = classify_span(sp, lines)
                    n = len(t)
                    if struck:
                        cur[2] += n
                    elif bold:
                        cur[3] += n
                    else:
                        cur[4] += n
    out = ["# item status (triage; confirm with --mode marked):"]
    for lab, p, s, b, pl in rows:
        out.append(f"p{p:>2}  {lab:>8}  {_status(s, b, pl)}")
    return "\n".join(out)


def parse_pages(spec, n):
    out = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1); out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return [p for p in out if 1 <= p <= n]


def main():
    ap = argparse.ArgumentParser(description="Recover tracked changes from a Council compromise PDF.")
    ap.add_argument("pdf")
    ap.add_argument("--pages", help="1-based pages/ranges, e.g. 2-16")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--mode", choices=["clean", "marked", "both", "summary"], default="both")
    ap.add_argument("--skip", default="", metavar="TOKENS",
                    help="comma-separated extra header/footer tokens to drop, e.g. the document "
                         "number that repeats in the footer ('6406/26'). Added to the generic set.")
    args = ap.parse_args()

    if args.skip:
        _SKIP.update(t.strip() for t in args.skip.split(",") if t.strip())

    if not os.path.exists(args.pdf):
        sys.exit(f"No such PDF: {args.pdf}")
    doc = fitz.open(args.pdf)
    n = doc.page_count
    pages = list(range(1, n + 1)) if (args.all or not args.pages) else parse_pages(args.pages, n)

    if args.mode == "summary":
        print(summarise(doc, pages))
        return

    for p in pages:
        marked, clean = render_page(doc[p - 1], args.mode)
        print(f"\n############### PAGE {p} ###############")
        if args.mode in ("marked", "both"):
            print(marked)
        if args.mode == "both":
            print("\n----------------- CLEAN -----------------")
        if args.mode in ("clean", "both"):
            print(clean)


if __name__ == "__main__":
    main()
