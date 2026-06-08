#!/usr/bin/env python3
"""Enumerate and classify open tracker issues for the resolve-tracker-issue skill.

The daily tracker cron (~/law-tracker/run.sh) detects what's new across the
watched sources and emits ONE GitHub issue per genuine hit, labelled `tracker`
plus a tier (`tier-1/2/3`) and a topic. Those issues — not the
data/tracker-state.yaml hash diff — are the flagged information a human has to
integrate. This script reads them via `gh`, parses the structured body the cron
writes (Source / URL / Detected at / Why / Excerpt), classifies each issue, and
joins it to data/watchlist.yaml so the resolver knows which downstream docs the
source feeds (`affects`).

It deliberately surfaces ONE issue at a time (`--issue N`) so each flag gets its
own focused plan — the skill never bundles issues.

A secondary `--from-state` mode cross-checks the tracker-state.yaml hash diff
against the issues, to catch a source whose hash moved but for which no issue was
opened (or vice-versa).

Usage:
  tracker_issues.py --list                 # human table of open tracker issues
  tracker_issues.py --json                  # same, as JSON (for the cron loop)
  tracker_issues.py --issue 18              # one issue, resolved + joined, JSON
  tracker_issues.py --list --include-triaged
  tracker_issues.py --from-state --since HEAD~3

Requires: gh (authenticated), python3, pyyaml.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("error: pyyaml not installed (pip install pyyaml)\n")
    sys.exit(2)

# Label the resolver adds to an issue once it has opened a plan PR, so reruns skip it.
TRIAGED_LABEL = "plan-drafted"

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
# The watchlist lives in the repo-root tracker.yaml (under `watchlist.sources`), the single
# source of truth for this tracker's file identity. A legacy data/watchlist.yaml is still
# honoured as a fallback if present.
TRACKER_CONFIG_PATH = os.path.join(REPO_ROOT, "tracker.yaml")
LEGACY_WATCHLIST_PATH = os.path.join(REPO_ROOT, "data", "watchlist.yaml")
STATE_PATH = os.path.join(REPO_ROOT, "data", "tracker-state.yaml")

CODE_RE = re.compile(r"\bT[123]-\d{2}\b")


# --------------------------------------------------------------------------- gh
def _gh_json(args: list[str]):
    try:
        out = subprocess.run(
            ["gh"] + args, capture_output=True, text=True, check=True, cwd=REPO_ROOT
        ).stdout
    except FileNotFoundError:
        sys.stderr.write("error: gh CLI not found on PATH\n")
        sys.exit(2)
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"error: gh {' '.join(args)} failed:\n{e.stderr}\n")
        sys.exit(2)
    return json.loads(out) if out.strip() else None


def list_tracker_issues():
    return _gh_json(
        [
            "issue", "list", "--label", "tracker", "--state", "open",
            "--limit", "100",
            "--json", "number,title,labels,body,url,createdAt,updatedAt",
        ]
    ) or []


def get_issue(number: int):
    return _gh_json(
        [
            "issue", "view", str(number),
            "--json", "number,title,labels,body,url,createdAt,updatedAt",
        ]
    )


# ---------------------------------------------------------------------- watchlist
def load_watchlist() -> dict:
    # Preferred: tracker.yaml -> watchlist.sources
    if os.path.exists(TRACKER_CONFIG_PATH):
        with open(TRACKER_CONFIG_PATH) as f:
            cfg = yaml.safe_load(f) or {}
        sources = (cfg.get("watchlist") or {}).get("sources")
        if sources:
            return sources
    # Fallback: legacy data/watchlist.yaml -> sources
    if os.path.exists(LEGACY_WATCHLIST_PATH):
        with open(LEGACY_WATCHLIST_PATH) as f:
            data = yaml.safe_load(f) or {}
        return data.get("sources", {})
    return {}


# ------------------------------------------------------------------- classification
def _field(body: str, label: str) -> str | None:
    """Pull a `**Label:** value` line from the cron's issue body."""
    m = re.search(rf"\*\*{re.escape(label)}:\*\*\s*(.+)", body)
    return m.group(1).strip() if m else None


def _excerpt(body: str) -> str | None:
    m = re.search(r"\*\*Excerpt / new items:\*\*\s*(.+?)(?:\n---|\Z)", body, re.S)
    return m.group(1).strip() if m else None


def classify(issue: dict, watchlist: dict) -> dict:
    title = issue.get("title", "")
    body = issue.get("body", "") or ""
    labels = [l["name"] for l in issue.get("labels", [])]
    triaged = TRIAGED_LABEL in labels

    out = {
        "number": issue.get("number"),
        "title": title,
        "issue_url": issue.get("url"),
        "labels": labels,
        "triaged": triaged,
        "type": "unknown",
        "codes": [],
        "source_url": None,
        "detected_at": None,
        "why": None,
        "excerpt": None,
        "affects": [],
        "document_id": None,
        "watchlist_label": None,
        "playbook": None,
    }

    # Special tracker housekeeping issues.
    if "run-summary" in labels or "Run summary" in title:
        out["type"] = "run-summary"
        out["playbook"] = "skip"
        out["codes"] = sorted(set(CODE_RE.findall(body)))
        return out
    if "Source health" in title:
        out["type"] = "source-health"
        out["playbook"] = "source-health"
        out["codes"] = sorted(set(CODE_RE.findall(body)))
        out["affects"] = ["data/watchlist.yaml", "data/documents.yaml", "sources/README.md"]
        return out
    if "State commit blocked" in title:
        out["type"] = "state-blocked"
        out["playbook"] = "source-health"
        out["affects"] = ["data/tracker-state.yaml"]
        return out

    # A normal content hit: parse the structured body.
    source = _field(body, "Source")
    out["source_url"] = _field(body, "URL")
    out["detected_at"] = _field(body, "Detected at")
    out["why"] = _field(body, "Why this looks relevant")
    out["excerpt"] = _excerpt(body)

    code = None
    if source:
        m = CODE_RE.search(source)
        code = m.group(0) if m else None
    if not code:  # fall back to any code mentioned in the body
        m = CODE_RE.search(body)
        code = m.group(0) if m else None
    if code:
        out["codes"] = [code]
        entry = watchlist.get(code, {})
        out["affects"] = entry.get("affects", [])
        out["document_id"] = entry.get("document_id")
        out["watchlist_label"] = entry.get("label")

    # Pick a playbook from the tier / source kind.
    if "tier-3" in labels or "bluesky" in labels:
        out["type"] = "social"
        out["playbook"] = "stakeholder-social"
    elif "tier-2" in labels:
        out["type"] = "stakeholder"
        out["playbook"] = "stakeholder-social"
    elif "tier-1" in labels:
        out["type"] = "institutional"
        out["playbook"] = "institutional"
        # Council-text sources route to the transcription-heavy variant.
        if code in ("T1-08", "T1-09") or "council" in labels:
            out["playbook"] = "council-text"
    return out


# ----------------------------------------------------------------------- state diff
def _read_state_at(rev: str | None) -> dict:
    if rev is None:
        with open(STATE_PATH) as f:
            return yaml.safe_load(f) or {}
    out = subprocess.run(
        ["git", "show", f"{rev}:data/tracker-state.yaml"],
        capture_output=True, text=True, cwd=REPO_ROOT,
    )
    if out.returncode != 0:
        sys.stderr.write(f"error: cannot read tracker-state.yaml at {rev}\n{out.stderr}\n")
        sys.exit(2)
    return yaml.safe_load(out.stdout) or {}


def state_diff(since: str) -> list[dict]:
    """Classify per-code deltas between `since` and the working tree."""
    old = (_read_state_at(since).get("sources") or {})
    new = (_read_state_at(None).get("sources") or {})
    changes = []
    for code in sorted(set(old) | set(new)):
        o, n = old.get(code), new.get(code)
        if o is None and n is not None:
            kind = "recovered"
        elif o is not None and n is None:
            kind = "newly-unreachable"
        elif o == n:
            continue
        else:
            oh, nh = o.get("last_seen_hash"), n.get("last_seen_hash")
            oi, ni = o.get("last_seen_indexed_at"), n.get("last_seen_indexed_at")
            if oh != nh or oi != ni:
                kind = "content-changed"
            else:
                kind = "noise"  # only last_seen_at moved
        changes.append({"code": code, "delta": kind})
    return changes


# --------------------------------------------------------------------------- output
def print_table(rows: list[dict]):
    if not rows:
        print("No open tracker issues.")
        return
    print(f"{'#':>4}  {'TYPE':<14} {'CODES':<10} {'TRIAGED':<7} TITLE")
    print("-" * 88)
    for r in rows:
        codes = ",".join(r["codes"]) or "-"
        print(
            f"{r['number']:>4}  {r['type']:<14} {codes:<10} "
            f"{'yes' if r['triaged'] else 'no':<7} {r['title'][:48]}"
        )
    print(f"\n{len(rows)} issue(s). Resolve one with: /tracker-issue <number>")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="human-readable table (default)")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--issue", type=int, metavar="N", help="resolve one issue by number")
    ap.add_argument("--include-triaged", action="store_true",
                    help=f"include issues already labelled '{TRIAGED_LABEL}'")
    ap.add_argument("--from-state", action="store_true",
                    help="secondary: diff tracker-state.yaml instead of listing issues")
    ap.add_argument("--since", default="HEAD~1", metavar="REV",
                    help="git rev for --from-state (default HEAD~1)")
    args = ap.parse_args()

    if args.from_state:
        changes = state_diff(args.since)
        meaningful = [c for c in changes if c["delta"] != "noise"]
        if args.json:
            print(json.dumps(changes, indent=2))
        else:
            if not meaningful:
                print(f"No meaningful state changes since {args.since} (timestamp-only rows suppressed).")
            for c in meaningful:
                print(f"  {c['code']:<8} {c['delta']}")
        return 0

    watchlist = load_watchlist()

    if args.issue is not None:
        issue = get_issue(args.issue)
        if not issue:
            sys.stderr.write(f"error: issue #{args.issue} not found\n")
            return 1
        result = classify(issue, watchlist)
        print(json.dumps(result, indent=2))
        return 0

    rows = [classify(i, watchlist) for i in list_tracker_issues()]
    rows = [r for r in rows if r["playbook"] != "skip"]
    if not args.include_triaged:
        rows = [r for r in rows if not r["triaged"]]

    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print_table(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
