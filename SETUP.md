# SETUP — start a tracker for a new EU file

This repo is a **GitHub template** for tracking one EU legislative file end-to-end (sources →
operative-text extracts → analysis), with three Claude Code skills and a daily change-tracker.

It ships filled in with the reference file **`2025/0360 (COD)`** (the Digital Omnibus) as a complete
worked example — every `EXAMPLE`-marked page shows the pattern you replace. Follow the steps below to
re-point it at your file.

## 0. Create your repo

On GitHub: **Use this template** → new repo. Clone it. (No GitHub remote is required for the local
parts, but the tracker opens issues, so a remote is recommended.)

```bash
pip install pymupdf cffi pyyaml   # cffi is required by the PDF driver; pyyaml by bootstrap + skills
```

## 1. Fill `tracker.yaml` — the single source of truth

[`tracker.yaml`](tracker.yaml) is the one place that defines *which* file this repo follows. Replace
**every** value with your file's:

- `file_id`, `short_name`, `strand`
- `proposal` (`id`, `date`, `swd`, `celex`, `oeil`)
- `keep_apart` — sibling file(s) that are easy to confuse with yours and must **not** be tracked here
  (this drives the scope-guard text and the skills' scope rule)
- `legal_bases`, `instruments` (the laws your file amends/repeals — drives `docs/instruments/`)
- `extract_slices` — the per-version operative-text file set (follows *your* file's article groupings;
  the shipped ones are 2025/0360's)
- `co_legislators`, `advisory_bodies`
- `watchlist.sources` — the URLs the daily tracker watches (ships with a representative subset)

## 2. Run the bootstrap

```bash
python3 bootstrap.py
```

This fills the `<PLACEHOLDER>` tokens in `CLAUDE.md`, `README.md`, `TIMELINE.md` and the `docs/` stubs
from `tracker.yaml`, and generates `STATUS.md` from [`STATUS.template.md`](STATUS.template.md). It does
**not** invent content — placeholders with no `tracker.yaml` source (e.g. `<LATEST-TEXT>`, `<one line>`)
are left for you. Re-run it any time you change identity values in `tracker.yaml`.

## 3. Replace the EXAMPLE content

Everything still carrying 2025/0360 substance is marked `EXAMPLE` — replace it with your file's:

| Layer | What ships (EXAMPLE) | Replace with |
|---|---|---|
| `extracts/commission/` | `COM-2025-837_*` base-text set | your Commission proposal's operative text (one file per `extract_slices`) |
| `extracts/council/` | `ST-9547-2026_*` one version set | your file's compromise versions (use the `transcribe-council-extract` skill) |
| `docs/provisions/` | `gdpr-art33-breach-notification.md` | one page per tracked provision |
| `docs/instruments/` | `gdpr-2016-679.md` | one page per amended/repealed instrument |
| `docs/advisory/` | `edpb-edps-jo-2-2026.md` | one digest per advisory-body opinion |
| `docs/` stubs | `summary`, `commission-proposal`, `institutional-positions`, `member-state-positions`, `fault-lines`, `stakeholders` | fill in for your file |
| `data/documents.yaml` + `sources/README.md` | 4 EXAMPLE rows | your documents (use the `register-document` skill) |
| `data/positions.csv` | 1 EXAMPLE row | one row per provision |
| `STATUS.md` / `docs/what-changed.md` / `TIMELINE.md` | EXAMPLE rows | your file's snapshot / diff / chronology |

Seed your first documents with the **`register-document`** skill (it appends to `data/documents.yaml`
and renders `sources/README.md`). Verify links after each change:

```bash
python3 .claude/skills/transcribe-council-extract/linkcheck.py .   # must end "0 broken"
```

## 4. Wire the daily tracker (optional but recommended)

The change-tracker is a **local cron** (not part of this repo) that hashes each source in
`tracker.yaml` (`watchlist.sources`), opens one `[tracker]` GitHub issue per genuine change, and updates
[`data/tracker-state.yaml`](data/tracker-state.yaml). Set up `~/law-tracker/run.sh` + `prompt.md` mirroring
your `watchlist.sources` (keep the two in sync). Triage each issue with the **`resolve-tracker-issue`**
skill (`/tracker-issue <n>`) — it joins the issue to its `affects` list and drafts one focused plan under
`docs/triage/`. `STATUS.md`'s **As of** date = `tracker-state.yaml` `last_run`.

Two lessons worth baking into your cron prompt:

- **Council outcomes need a mirror.** consilium.europa.eu serves a browser-check page to curl, so
  meeting outcomes ("main results") are invisible to the tracker — keep the shipped
  `INSIGHT EU MONITORING` source (T2-03, file-agnostic) and filter it on your file's keywords.
- **New-source baseline rule.** When a source is added to the watchlist later, its first poll has no
  stored hash — instruct the tracker to store the baseline silently instead of opening a false hit.

## 5. Sanity check

```bash
python3 .claude/skills/transcribe-council-extract/linkcheck.py .        # 0 broken
python3 -c "import yaml; yaml.safe_load(open('tracker.yaml')); yaml.safe_load(open('data/documents.yaml'))"
grep -rn "2025/0360\|<FILE-ID>\|<PROPOSAL-ID>" --include='*.md' . | grep -v EXAMPLE   # should be empty
```

## The three-layer model (why it's shaped this way)

See [`CLAUDE.md`](CLAUDE.md): `sources/` (append-only register) → `extracts/` (diffable operative text,
one set per version) → `docs/` (living analysis that links *down*). The split keeps links stable as the
file evolves. The reporting format is fixed by [`docs/reporting-standard.md`](docs/reporting-standard.md)
so sibling trackers read alike.
