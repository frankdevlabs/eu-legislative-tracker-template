# Parliament extracts — working rules

> **OPTIONAL layer.** This directory holds European Parliament committee-text extracts. It is only
> relevant while the file this repo tracks has a live EP stage — omit/ignore it for already-adopted
> directives or post-adoption files with no live Parliament reading. See [`../../SETUP.md`](../../SETUP.md).

Before adding or editing any file in this directory, read
[`_TRANSCRIPTION_GUIDE.md`](./_TRANSCRIPTION_GUIDE.md) and follow it. It is the canonical standard
for transcribing **European Parliament committee texts** (draft opinions, draft reports, tabled
amendments, adopted texts).

Unlike [`../council/`](../council/) consolidated compromise texts, EP committee texts are **discrete
numbered amendments** in two-column tables — transcribe them as tabled, do **not** consolidate, and do
**not** use `pdf_changes.py` (there are no tracked-change redlines to recover). One file per committee
document, named `<DOC-ID>_<short-desc>.md`. The **primary** read method is the **Read tool on the
committed PDF** (it renders the pages); `render_pdf.py` is an optional cross-check only if pymupdf is
available. Source of truth is the committed file under
[`../../sources/parliament/`](../../sources/parliament/); `doceo` bot-blocks automated fetches (HTTP
202 / AWS-WAF), so obtain the file via a browser download or non-WAF mirror first. Use explicit
`<a id="...">` HTML anchors, **not** `{#...}` heading suffixes.
