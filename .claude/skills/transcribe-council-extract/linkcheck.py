#!/usr/bin/env python3
"""Internal relative-link + anchor checker for the repo's markdown files.
Skips external (http/https/mailto) links; resolves relative targets against each
file's directory and asserts existence; for #fragments, asserts the fragment
matches an <a id=...>/<a name=...> or a GitHub-slugified heading in the target."""
import os, re, sys, glob

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
LINK = re.compile(r'\[(?:[^\]]*)\]\(([^)]+)\)')
ANCHOR_TAG = re.compile(r'<a\s+(?:id|name)\s*=\s*["\']([^"\']+)["\']', re.I)
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')

def slug(text):
    # strip markdown emphasis/links/code, then GitHub-style slugify
    t = re.sub(r'`([^`]*)`', r'\1', text)
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'[*_~]', '', t)
    t = t.strip().lower()
    t = ''.join(c for c in t if c.isalnum() or c in ' -')
    return t.replace(' ', '-')

def anchors_for(path):
    out = set()
    seen = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            for m in ANCHOR_TAG.finditer(line):
                out.add(m.group(1))
            hm = HEADING.match(line)
            if hm:
                s = slug(hm.group(2))
                if s in seen:
                    seen[s] += 1
                    out.add(f"{s}-{seen[s]}")
                else:
                    seen[s] = 0
                    out.add(s)
    return out

files = [p for p in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True)
         if ".git" not in p and not p.endswith(".template.md")]  # skip placeholder templates
anchor_cache = {}
broken = []
checked = 0
for f in files:
    base = os.path.dirname(f)
    with open(f, encoding='utf-8') as fh:
        text = fh.read()
    for m in LINK.finditer(text):
        tgt = m.group(1).strip()
        if tgt.startswith('<') and tgt.endswith('>'):
            tgt = tgt[1:-1].strip()
        low = tgt.lower()
        if low.startswith(('http://', 'https://', 'mailto:', 'tel:', '//')):
            continue
        checked += 1
        path_part, _, frag = tgt.partition('#')
        if path_part == '':
            target_file = f
        else:
            target_file = os.path.normpath(os.path.join(base, path_part))
        rel = os.path.relpath(f, ROOT)
        if not os.path.exists(target_file):
            broken.append(f"{rel}: missing file -> {tgt}")
            continue
        if frag:
            if target_file not in anchor_cache:
                anchor_cache[target_file] = anchors_for(target_file) if target_file.endswith('.md') else set()
            if frag not in anchor_cache[target_file]:
                broken.append(f"{rel}: missing anchor '#{frag}' in {path_part or os.path.basename(f)}")

print(f"Scanned {len(files)} markdown files; checked {checked} internal links.")
if broken:
    print(f"\nBROKEN ({len(broken)}):")
    for b in broken:
        print("  " + b)
    sys.exit(1)
print("All internal links and anchors resolve. (0 broken)")
