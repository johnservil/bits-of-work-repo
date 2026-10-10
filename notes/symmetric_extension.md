# Symmetric extension: what we changed, and why

This repository adds one assumption class, **Symmetric** (cryptanalysis of block ciphers, stream ciphers, hash functions, MACs, and permutations), to the study as Matthew Green published it. This note records every change to the study's code, data, and method, so its authors and anyone else can see what differs, check it, reproduce it, or vary it.

- **Baseline:** commit `172f562`, the public export from the study's private repository at `90e638c`.
- **Class definitions, fixed before measurement:** `notes/symmetric_preregistration.md` (commit `a565658`, 2026-10-10).
- **Every code change:** `git diff 172f562 -- pipeline analysis`.
- **Published at:** https://github.com/johnservil/bits-of-work-repo, branch `symmetric`; its `main` mirrors the study's.

## Effect on the study's existing results

Every public-key number stays as published: the committed labels, counts, exports, and records are untouched. Rerunning the public-key keyword screen on the new ePrint harvest with our code yields the same 4,754 candidates, with the same keyword hits, as the baseline code (check below). FSE's addition to the DBLP venue lists (change 4) is the one change that could add public-key candidates on a full rerun; that rerun has yet to be done.

## Changes

Each entry gives the date, the change, the reason, and its effect on the public-key classes.

1. **2026-10-10. Raw data re-harvested.** The study's raw pulls are outside the public export, and its committed ePrint file has no abstracts.
   - ePrint, via `pipeline/fetch_eprint_oai.py`: 57 OAI-PMH pages; 27,272 records after 838 deleted stubs, parsed by `pipeline/parse_eprint_oai.py` to `data/raw/eprint/eprint_oai.jsonl` (sha256 `ddf8d134eb0d5a19116312a8a8cd23743f917ef96a5a1f78435a19fa0c969308`). The committed `data/eprint.jsonl` is unchanged.
   - DBLP dump `dblp.xml.gz` downloaded 2026-10-10, 1,110,469,870 bytes (sha256 `d02df2909fc497390c78ea142bc2cc05397dcb6873161a9306c9a4e2d38e960f`), with `dblp.dtd` (sha256 `2d864498f9eef9298662df11e3874171ff24cd4a21ab5974f1369c90acdb1ef6`).
   - `pipeline/parse_dblp.py` keeps 385,011 of 8,712,838 DBLP records (the study kept 375,911); about 4,100 symmetric title hits are absent from ePrint.
   - Both pulls are one day newer than the study's; the public-key labels keep the study's pulls.
2. **2026-10-10. Harvester identity.** Every harvester (`fetch_eprint_oai.py`, `fetch_openalex.py`, `fetch_zbmath.py`, `fetch_arxiv.py`, `authors_enrich.py`) now identify this extension and John Servil (https://github.com/johnservil) in place of the study author's address; the 2026-10-10 ePrint and DBLP downloads sent `bits-of-work-symmetric-extension/0.1`. `fetch_openalex.py` drops its `mailto=` parameter, which needs a working email address, and so uses OpenAlex's general pool: 1,000 credits a day without a key, against the study's keyed 10,000. The harvester already waits for each daily reset.
3. **2026-10-10. Symmetric keyword screen.** `pipeline/candidates.py` gains a `symmetric` class with four patterns: names of symmetric-cryptanalysis techniques (matched alone), hash-attack phrases, primitive names beside an attack word, and generic or quantum symmetric attacks. Primitive names that are also English words (PRESENT, IDEA, GIFT, Grain, SIMON, and others) match case-sensitively. On ePrint the screen yields 3,016 symmetric candidates; precision is the classifier's job, as in the study.
4. **2026-10-10. FSE added to DBLP venue lists.** `pipeline/parse_dblp.py` (`VENUES`) and `pipeline/merge_sources.py` (`CORE`) include FSE, the main symmetric venue. `IACR Trans` already covered ToSC. Effect: a full public-key rerun would also keep every FSE record and fetch FSE abstracts, which could add a few public-key candidates.
5. **2026-10-10. Weak "discrete log" rule ignores symmetric hits.** The study drops a candidate whose only hit is the generic `discrete log` keyword. A symmetric hit would have counted as a second class and kept 11 extra ePrint items as ECDLP candidates. The rule now ignores symmetric hits, in all three copies (`candidates.py`, `parse_dblp.py`, `merge_sources.py`); the public-key screen is identical to the baseline's.

## Decisions still open

- **Classifier runs.** The study labeled with subagents: Sonnet for pass 1, Opus for pass 2, model versions unrecorded (the same sessions used Opus 5.5 for other work). We plan the same two passes and prompts through the OpenRouter API, with `anthropic/claude-sonnet-5.5` and `anthropic/claude-opus-5.5`. Each API call carries the rubric and a batch in its prompt, where a subagent read them from files. Question for the study's authors: which versions did you use?
- **Items already labeled for public-key classes.** 523 ePrint candidates hit both a public-key class and Symmetric. They carry labels from rubric v0.3.4, which ruled symmetric work out of scope, so they need symmetric labels under the extended rubric.
- **Rubric v0.4.** The symmetric section, written from the pre-registration.
- **Other sources.** OpenAlex phrase queries and zbMATH queries for symmetric work; tiering for the larger DBLP pool; the OpenAlex contact address.

## How to check this work

Public-key screen identical to the baseline:

```bash
git show 172f562:pipeline/candidates.py > /tmp/candidates_orig.py
python3 -I /tmp/candidates_orig.py data/raw/eprint/eprint_oai.jsonl /tmp/cand_orig.jsonl
python3 -I pipeline/candidates.py data/raw/eprint/eprint_oai.jsonl /tmp/cand_new.jsonl
python3 - <<'E'
import json
a = {json.loads(l)["eprint_id"]: json.loads(l)["kw_hits"] for l in open("/tmp/cand_orig.jsonl")}
b = {json.loads(l)["eprint_id"]: json.loads(l)["kw_hits"] for l in open("/tmp/cand_new.jsonl")}
pk = {e: {k: v for k, v in h.items() if k != "symmetric"} for e, h in b.items()}
assert {e: h for e, h in pk.items() if h} == a
print("public-key screen identical")
E
```

Re-harvest: as in `STATUS.md` ("Raw re-harvest"), with the User-Agent above.
