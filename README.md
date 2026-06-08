# <SHORT-NAME> Tracker — File <FILE-ID>

A personal, open tracker for the EU **<SHORT-NAME>** proposal. Strand: <STRAND>.

> **Built from the EU legislative-tracker template.** The file this repo follows is set
> once in [`tracker.yaml`](tracker.yaml); `python3 bootstrap.py` fills the `<PLACEHOLDER>` tokens in
> this README, `CLAUDE.md` and `STATUS.md`. Some pages still carry **EXAMPLE** content from the
> reference file `2025/0360 (COD)` — replace it per `SETUP.md`.

> **Scope.** This repo tracks **one file only: `<FILE-ID>`** — Commission proposal
> **<PROPOSAL-ID> final** of <PROPOSAL-DATE>.
> It is **not** `<KEEP-APART-ID>` (<KEEP-APART-NOTE>), which is a separate proposal on a separate
> track. See [`tracker.yaml`](tracker.yaml) (`file_id` vs `keep_apart`) and `STATUS.md`
> for why the two are kept apart.

**Current status (high level):** see the full snapshot in **`STATUS.md`**.

---

## How this repo is organised

The repo deliberately separates three layers so that links stay stable over time:

| Layer | Folder | What it is | Mutable? |
|---|---|---|---|
| **Primary sources** | [`sources/`](sources/) | Register of every official document, with links to authoritative copies | append-only |
| **Operative-text extracts** | [`extracts/`](extracts/) | Diffable plain-text of the operative articles, for `git diff` across versions — [`commission/`](extracts/commission/) is the Commission base text, [`council/`](extracts/council/) the compromise texts | versioned |
| **Analysis** | [`docs/`](docs/) | The human-readable analysis that links *to* the layers above | living |

### Navigation

- **`STATUS.md`** — where the file stands right now (one screen).
- **[`TIMELINE.md`](TIMELINE.md)** — full chronology, every entry linked to a source.
- **[`docs/summary.md`](docs/summary.md)** — the plain-language summary.
- **[`docs/commission-proposal.md`](docs/commission-proposal.md)** — digest of the Commission proposal's explanatory memorandum.
- **[`docs/advisory/`](docs/advisory/)** — digests of the advisory-body opinions.
- **[`docs/institutional-positions.md`](docs/institutional-positions.md)** — Commission vs Council vs Parliament comparison table.
- **[`docs/member-state-positions.md`](docs/member-state-positions.md)** — what individual Council delegations are saying.
- **[`docs/fault-lines.md`](docs/fault-lines.md)** — the contested issues likely to dominate trilogue.
- **[`docs/stakeholders.md`](docs/stakeholders.md)** — NGO / industry / academic positions.
- **[`docs/provisions/`](docs/provisions/)** — one file per tracked provision.
- **[`docs/instruments/`](docs/instruments/)** — what changes per amended/repealed instrument (driven by `tracker.yaml` `instruments`).
- **[`sources/README.md`](sources/README.md)** — the document register.
- **[`extracts/commission/`](extracts/commission/)** — base-text extracts of the Commission proposal (the diff baseline).
- **[`extracts/council/`](extracts/council/)** — operative-text extracts of the Council compromise texts.

---

## Linking conventions

1. **Relative links only.** Never link to `github.com/...` absolute URLs inside the repo — relative
   paths survive renames, forks and a move to a private mirror.
2. **Deep-link into extracts, not PDFs.** GitHub's PDF viewer does not support reliable
   `#page=` anchors, so to point at a specific article use the markdown extract's heading anchor,
   e.g. `extracts/council/ST-<nnnn>-<yyyy>_gdpr-art3-amendments.md#point-8--article-33-breach-notification`.
3. **Source PDFs are committed in `sources/`.** The Council compromise texts (incl. LIMITE ones)
   are hosted in this repo for transparency and offline diffing; the register also records the
   document number, the Council register reference, and any national-parliament record or public
   mirror so provenance stays traceable. See [`NOTICE`](NOTICE) §2. The markdown extracts in
   [`extracts/`](extracts/) remain the *linkable* working copies — link `extracts/...md#anchor`,
   not `sources/...pdf#page`.

## Naming convention for documents

`<INSTITUTIONAL-ID>_<short-description>_<ISO-date>.<ext>` — the stable document number first,
ISO date last, so chronological sort always works
(e.g. `ST-9547-2026_council-presidency-compromise_2026-05-21`).

## Contributing / adding a document

Open an issue using [`.github/ISSUE_TEMPLATE/new-document.md`](.github/ISSUE_TEMPLATE/new-document.md),
or run the `register-document` skill: it adds the entry to [`data/documents.yaml`](data/documents.yaml),
regenerates the register row in [`sources/README.md`](sources/README.md), and (if it is a new compromise
text) hands transcription to the `transcribe-council-extract` skill for a matching set under
[`extracts/`](extracts/).

---

## Reusing this template for another EU file

This repo is a **GitHub template**. To track a different file: *Use this template* → fill
[`tracker.yaml`](tracker.yaml) → run `python3 bootstrap.py` → follow `SETUP.md`.

## Disclaimer & licence

This is a **personal project** published in a personal capacity. It is **not legal advice** and does
**not** represent the views of any employer. See **[`DISCLAIMER.md`](DISCLAIMER.md)**.

- Original analysis and commentary in this repo: licensed under **CC BY 4.0** — see [`LICENSE`](LICENSE).
- EU documents and third-party works are **not** covered by that licence — see [`NOTICE`](NOTICE).
