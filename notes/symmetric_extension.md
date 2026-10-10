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
2. **2026-10-10. Harvester identity.** Every harvester (`fetch_eprint_oai.py`, `fetch_openalex.py`, `fetch_zbmath.py`, `fetch_arxiv.py`, `authors_enrich.py`) identifies this extension and John Servil (johnservil@proton.me, https://github.com/johnservil) in place of the study author's address; `fetch_openalex.py` sends that address as `mailto=`, exactly as the study sent its own. The 2026-10-10 ePrint and DBLP downloads sent `bits-of-work-symmetric-extension/0.1`. Without an API key OpenAlex allows 1,000 credits a day (the study had a key with 10,000); the address leaves that limit unchanged.
3. **2026-10-10. Symmetric keyword screen.** `pipeline/candidates.py` gains a `symmetric` class with four patterns: names of symmetric-cryptanalysis techniques (matched alone), hash-attack phrases, primitive names beside an attack word, and generic or quantum symmetric attacks. Primitive names that are also English words (PRESENT, IDEA, GIFT, Grain, SIMON, and others) match case-sensitively. On ePrint the screen yields 3,016 symmetric candidates; precision is the classifier's job, as in the study.
4. **2026-10-10. FSE added to DBLP venue lists.** `pipeline/parse_dblp.py` (`VENUES`) and `pipeline/merge_sources.py` (`CORE`) include FSE, the main symmetric venue. `IACR Trans` already covered ToSC. Effect: a full public-key rerun would also keep every FSE record and fetch FSE abstracts, which could add a few public-key candidates.
5. **2026-10-10. Weak "discrete log" rule ignores symmetric hits.** The study drops a candidate whose only hit is the generic `discrete log` keyword. A symmetric hit would have counted as a second class and kept 11 extra ePrint items as ECDLP candidates. The rule now ignores symmetric hits, in all three copies (`candidates.py`, `parse_dblp.py`, `merge_sources.py`); the public-key screen is identical to the baseline's.

6. **2026-10-10. Rubric v0.4.** `pipeline/rubric.md` gains the `symmetric` tag, worded from the pre-registration, with ten calibration examples; the out-of-scope list under `other` drops "hash/symmetric cryptanalysis". The public-key rules are unchanged, and the study's labels keep v0.3.4.
7. **2026-10-10. API classifier.** `pipeline/classify_openrouter.py` sends each batch in one OpenRouter call, with the instructions in `pipeline/classify_prompt.md` ("API pass 1/2") plus the rubric as the system message. The instructions are the study's pass-1 and pass-2 prompts, minus their file and tool steps, and minus "chaos-based image encryption" from the list of non-cryptographic papers, since the pre-registration counts such cryptanalysis. The runner checks every line and every id itself, and records each call's tokens and cost in `usage.tsv` beside the labels.
8. **2026-10-10. Symmetric searches.** `fetch_openalex.py` (24 phrases) and `fetch_zbmath.py` (11 queries) gain symmetric searches, and an optional class argument that harvests one class alone.
9. **2026-10-10. Pilot.** 60 randomly drawn ePrint symmetric candidates (seed 20261010), labeled by pass 1 with `anthropic/claude-sonnet-5.5` and the study's 1,000-character abstract cap: 34 yes (23 A, 5 C, 4 F, 2 G), 26 no; one call, 31,093 prompt and 7,075 completion tokens, $0.13. Labels: `data/symmetric/pilot_p1/`. Pools and batches embed third-party abstracts, so they stay in the gitignored `data/raw/symmetric/`, as the study's public export omits its own.

10. **2026-10-10. ePrint pass 1.** All 3,016 ePrint symmetric candidates (including the 523 that also hit a public-key class), 51 batches, `anthropic/claude-sonnet-5.5`, abstract cap 1,000: every batch valid on its first call, $6.78. Labels: `data/symmetric/eprint_p1/`. These labels serve the symmetric weight only; the public-key classes keep the study's labels.
11. **2026-10-10. ePrint pass 2.** `make_pass2.py` unchanged (seed 20261008, 10% audit of exclusions, abstract cap 1,500), `anthropic/claude-opus-5.5`: 2,145 yes/borderline items plus 87 sampled exclusions, 38 batches; passes 1 and 2 together cost $20.47. `merge_pass2.py`: include kappa 0.83, category agreement 0.94, 0 of 87 audited exclusions flipped (the study: 0.84-0.89, 0.92, 1.1%). As in the study, pass 2 sees the pass-1 label. Manifest `data/symmetric/eprint_p2_manifest.json`, labels `data/symmetric/eprint_p2/`, statistics `data/symmetric/eprint_agreement.txt`.
12. **2026-10-10. Runner retries truncated responses.** A response cut off mid-read (`http.client.IncompleteRead`) stopped the first pass-2 run after 28 of 38 batches; `classify_openrouter.py` now retries `http.client.HTTPException` like other network errors, and the rerun finished the remaining 10.

13. **2026-10-10. One screen and one merge for both tracks.** `candidates.py` and `merge_sources.py` take an optional class argument, like the harvesters. Without it they behave exactly as the study's code did, ignoring symmetric hits (`candidates.py` output matches the baseline code byte for byte on the new ePrint harvest). With `symmetric` they keep symmetric candidates only. Symmetric runs also take ePrint coverage and snowball seeds from `data/raw/symmetric/eprint_labeled_final.jsonl`, and write to `data/raw/symmetric/candidates_merged.jsonl`, `data/raw/openalex/seeds_symmetric*.jsonl` and `data/symmetric/coverage.txt`; the committed study files stay untouched. The symmetric pool is untiered, since every symmetric hit is tier A under the study's rule.
14. **2026-10-10. Merge and round 1.** OpenAlex DOI lookups (39,555 DOIs of core-venue DBLP items lacking abstracts, 39,292 works returned), then `merge_sources.py symmetric`: 9,429 screened symmetric items, 1,285 covered by the ePrint pool, 8,144 new (5,473 with abstracts). Pass 1 on the 8,144 started (`data/symmetric/r1_p1/`). Snowball: 1,428 resolved seeds plus 556 by title, then backward and forward (cap 400 citers per seed), as in `run_openalex_chain.sh`.

15. **2026-10-10. Runner restores the subagents' self-check.** In 3 of 136 round-1 batches, pass 1 left out one item on every attempt; a diagnostic call showed a normal reply with one ordinary item skipped. The study's subagents counted their lines and fixed any gap (pass-1 prompt, step 4). The runner now does the same: when a reply lacks some ids, it asks once, in the same conversation, for exactly those lines (`pipeline/classify_prompt.md` records the wording). The three batches then completed. Two diagnostic calls ($0.23) ran outside the runner and are absent from `usage.tsv`.
16. **2026-10-10. Round 1 labeled.** Pass 1, 136 batches; pass 2 (`make_pass2.py` unchanged), 4,206 yes/borderline items plus 393 sampled exclusions, 77 batches. `merge_pass2.py`: include kappa 0.84, category agreement 0.91, 2 of 393 audited exclusions flipped (estimated miss rate 0.5%). Labels `data/symmetric/r1_p1/`, `data/symmetric/r1_p2/`; manifest `data/symmetric/r1_p2_manifest.json`; statistics `data/symmetric/r1_agreement.txt`. Recorded spend through round 1: $62.48.

## Decisions still open

- **Model versions.** The study recorded "Sonnet" and "Opus" without versions (its sessions used Opus 5.5 for other work). We use `anthropic/claude-sonnet-5.5` for pass 1 and `anthropic/claude-opus-5.5` for pass 2. Question for the study's authors: which versions did you use?
- **Snowball round.** Classifying the snowball's new candidates, then counts and research-allocation years.

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
