#!/usr/bin/env python3
"""Export the public subset of this repository into a separate public repo.

Usage (from the repo root):
  python3 -I pipeline/export_public.py ~/Dropbox/src2/bits-of-work-repo [--ref COMMIT]

--ref exports an older private commit instead of HEAD (used to publish a pinned snapshot,
tagged snapshot-<commit> in the public repo, that the methodology page links to).

Exports a committed revision (never uncommitted work) and removes:
  - full-text copies of papers and specifications (HAWK pilot packet, held-out set, paper extract);
  - third-party abstracts: 'abstract' keys in JSON/JSONL, and every classifier input batch
    (batches*/, screen/ directories), which embed titles and abstracts;
  - person-level author data (names with career data and per-person effort); only the
    aggregate data/authors/fte_by_year.csv is kept, and the per-person "Top 25" lists are
    cut from analysis/author_map.txt;
  - analysis/review_sheet.md (abstracts) and stray notes.
Then it verifies that no abstract text from the private data survives anywhere in the export,
and that every link from docs/ into the public repository resolves.
Stdlib only. It never commits or pushes; the caller reviews and does that.
"""
from pathlib import Path
import json, re, shutil, subprocess, sys

SRC = Path(__file__).resolve().parent.parent
PRIVATE_URL = 'github.com/matthewdgreen/literature-search'
PUBLIC_URL = 'github.com/matthewdgreen/bits-of-work-repo'
# links pinned to a private commit point at the public snapshot tag for that commit
PINNED = re.compile(r'github\.com/matthewdgreen/literature-search/(blob|tree)/([0-9a-f]{7,40})\b')
PUBLIC_LINK = re.compile(r'github\.com/matthewdgreen/bits-of-work-repo/(?:blob|tree)/([^/"\'#)\s]+)/([^"\'#)\s]*)')

DROP_DIRS = {'batches', 'batches_pass2', 'batches_p1', 'batches_p2', 'screen'}
DROP_PREFIXES = (
    'data/ai_effort/pilot_hawk/packet/',
    'data/ai_effort/pilot_hawk/heldout/',
    'tmp/',
    'pipeline/public_files/',             # copied to the public repo's root instead (see below)
)
DROP_FILES = {
    'docs/CNAME',                         # the site is served from the private repo
    'data/ai_effort/pilot_hawk/anthropic_paper_extract.md',
    'analysis/review_sheet.md',
    'notes/claude-memory-project.md',
}
KEEP_AUTHOR_FILES = {'data/authors/fte_by_year.csv'}
DROP_KEYS = {'abstract'}


def git(*args, cwd=SRC):
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, check=True).stdout


def excluded(path):
    parts = path.split('/')
    if any(p in DROP_DIRS for p in parts[:-1]):
        return 'classifier input batch (embeds abstracts)'
    if path.startswith(DROP_PREFIXES):
        return 'full text or scratch'
    if path in DROP_FILES:
        return 'abstracts / full text / stray note'
    if path.startswith('data/authors/') and path not in KEEP_AUTHOR_FILES:
        return 'person-level author data'
    return None


def strip_json(obj):
    if isinstance(obj, dict):
        return {k: strip_json(v) for k, v in obj.items() if k not in DROP_KEYS}
    if isinstance(obj, list):
        return [strip_json(v) for v in obj]
    return obj


def transform(path, data):
    if path.endswith('.jsonl'):
        out = []
        for line in data.decode().splitlines():
            out.append(json.dumps(strip_json(json.loads(line)), ensure_ascii=False) if line.strip() else line)
        return ('\n'.join(out) + '\n').encode()
    if path.endswith('.json'):
        try:
            return (json.dumps(strip_json(json.loads(data)), ensure_ascii=False, indent=1) + '\n').encode()
        except ValueError:
            return data
    if path == 'analysis/author_map.txt':
        # cut each "Top 25 by author-fractional credit" block (header through the next blank line)
        out, skip = [], False
        for line in data.decode().splitlines():
            if line.startswith('Top 25 by'):
                skip = True
                out.append(line.split(':')[0] + ': [per-person list omitted from the public export]')
                continue
            if skip and not line.strip():
                skip = False
            if not skip:
                out.append(line)
        return ('\n'.join(out) + '\n').encode()
    if path.startswith('docs/') and path.endswith(('.html', '.js')):
        text = PINNED.sub(lambda m: f'{PUBLIC_URL}/{m[1]}/snapshot-{m[2][:7]}', data.decode())
        return text.replace(PRIVATE_URL, PUBLIC_URL).encode()
    return data


WORD = re.compile(r'\w+')
GRAM = 12         # an abstract "leaks" if any run of 12 consecutive words from its middle reappears


def grams(text):
    w = WORD.findall(text.lower())
    return {hash(tuple(w[i:i + GRAM])) for i in range(len(w) - GRAM + 1)}


def private_abstract_snippets():
    """Three 12-word sequences (at 1/3, 2/3 and the end) from every abstract of 40+ words in the private data.

    Sequences that also occur in a title are ignored: some sources put the title in the
    abstract field, and titles are bibliographic metadata that the export keeps.
    Matching on words rather than characters is fast and ignores JSON escaping."""
    snips, titles, n = {}, set(), 0
    for path in git('ls-files', '*.jsonl', '*.json').decode().split():
        try:
            text = (SRC / path).read_text()
        except (OSError, UnicodeDecodeError):
            continue
        rows = text.splitlines() if path.endswith('.jsonl') else [text]
        for row in rows:
            try:
                obj = json.loads(row)
            except ValueError:
                continue
            stack = [obj]
            while stack:
                o = stack.pop()
                if isinstance(o, dict):
                    for k, v in o.items():
                        if k in DROP_KEYS and isinstance(v, str) and len(v) >= 160:
                            w = WORD.findall(v.lower())
                            if len(w) < 40:      # citation strings misfiled as abstracts, not prose
                                continue
                            n += 1
                            for m in (len(w) // 3, 2 * len(w) // 3, len(w) - GRAM):
                                snips.setdefault(hash(tuple(w[m:m + GRAM])), set()).add(n)
                        elif k == 'title' and isinstance(v, str):
                            titles |= grams(v)
                        else:
                            stack.append(v)
                elif isinstance(o, list):
                    stack.extend(o)
    return {g: ids for g, ids in snips.items() if g not in titles}


def leaked(snips, text):
    """True if two or more sampled sequences of the same abstract occur in text.

    One match alone is usually a citation (title and authors) quoted inside an abstract."""
    hits = {}
    for g in grams(text).intersection(snips):
        for i in snips[g]:
            hits[i] = hits.get(i, 0) + 1
            if hits[i] >= 2:
                return True
    return False


def main():
    args = sys.argv[1:]
    ref = 'HEAD'
    if '--ref' in args:
        i = args.index('--ref'); ref = args[i + 1]; del args[i:i + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    dst = Path(args[0]).expanduser().resolve()
    if not (dst / '.git').exists() or dst == SRC:
        sys.exit(f'{dst} is not a separate git repository')
    # clear the destination tree (keeps .git)
    for p in dst.iterdir():
        if p.name != '.git':
            shutil.rmtree(p) if p.is_dir() else p.unlink()

    head = git('rev-parse', '--short', ref).decode().strip()
    kept, dropped = 0, {}
    for path in git('ls-tree', '-r', '--name-only', '-z', ref).decode().split('\0'):
        if not path:
            continue
        why = excluded(path)
        if why:
            dropped[why] = dropped.get(why, 0) + 1
            continue
        try:
            data = git('show', f'{ref}:{path}')
        except subprocess.CalledProcessError:
            continue                       # deleted in the working tree but still listed
        out = dst / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(transform(path, data))
        kept += 1

    # README (what this copy omits), licenses and .github/ (issue templates), kept in pipeline/public_files/
    for f in (SRC / 'pipeline/public_files').iterdir():
        if f.is_dir():
            shutil.copytree(f, dst / f.name, dirs_exist_ok=True)
        else:
            shutil.copyfile(f, dst / f.name)

    # verification: no private abstract text may survive
    snips = private_abstract_snippets()
    leaks = []
    for f in dst.rglob('*'):
        if '.git' in f.parts or not f.is_file():
            continue
        try:
            text = f.read_text()
        except UnicodeDecodeError:
            continue
        if leaked(snips, text):
            leaks.append(str(f.relative_to(dst)))
    # verification: every docs/ link into the public repo must resolve
    broken = []
    for f in (dst / 'docs').rglob('*.html'):
        for ref_, p in set(PUBLIC_LINK.findall(f.read_text())):
            p = p.rstrip('/')
            if ref_ == 'main' or ref_ == f'snapshot-{head}':   # this export itself
                ok = (dst / p).exists() if p else True
            else:
                try:
                    git('cat-file', '-e', f'{ref_}:{p}' if p else ref_, cwd=dst); ok = True
                except subprocess.CalledProcessError:
                    ok = False
            if not ok:
                broken.append(f'{f.name}: {ref_}/{p}')
    print(f'exported {ref} ({head}): {kept} files kept')
    for why, n in sorted(dropped.items()):
        print(f'  dropped {n:4d}  {why}')
    print(f'abstract-leak check: {len({i for ids in snips.values() for i in ids})} abstracts, {len(leaks)} files with matches')
    for f in leaks[:20]:
        print('  LEAK', f)
    print(f'link check: {len(broken)} broken links into the public repo')
    for b in broken[:30]:
        print('  BROKEN', b)
    sys.exit(1 if leaks or broken else 0)


if __name__ == '__main__':
    main()
