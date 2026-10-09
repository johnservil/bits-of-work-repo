PYTHON ?= python3
LATEXMK ?= latexmk
BUILD := ../tmp/pdfs/whitepaper
OUTPUT := ../output/pdf/cryptanalytic-effort-whitepaper.pdf
SITE_OUTPUT := ../docs/assets/cryptanalytic-effort-whitepaper.pdf

.PHONY: all tables clean
all: tables
	mkdir -p $(BUILD) ../output/pdf ../docs/assets
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -outdir=$(BUILD) whitepaper.tex
	cp $(BUILD)/whitepaper.pdf $(OUTPUT)
	cp $(OUTPUT) $(SITE_OUTPUT)

tables:
	$(PYTHON) -I generate_tables.py

clean:
	$(LATEXMK) -C -outdir=$(BUILD) whitepaper.tex
