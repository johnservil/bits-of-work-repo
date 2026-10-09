#!/bin/sh
# Sequential OpenAlex chain (one harvester at a time, per CLAUDE.md).
# 1. abstracts for core-venue DBLP items  2. resolve seeds  3. backward refs  4. forward citers
set -e
cd "$(dirname "$0")/.."
python3 -I pipeline/fetch_openalex.py dois data/raw/dblp/enrich_dois.txt data/raw/openalex
python3 -I pipeline/fetch_openalex.py resolve data/raw/openalex/seeds_all.jsonl data/raw/openalex
python3 -I pipeline/fetch_openalex.py backward data/raw/openalex
python3 -I pipeline/fetch_openalex.py forward data/raw/openalex 400
echo CHAIN DONE
