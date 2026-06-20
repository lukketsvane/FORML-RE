# GRUNNLAUST — Makefile
# Krev: xelatex (med EB Garamond eller TeX Gyre Pagella som fallback).

SRCDIR = src
PDFDIR = pdf
MAIN   = grunnlaust
XELATEX = xelatex -interaction=nonstopmode -output-directory=../$(PDFDIR)

.PHONY: all clean

all: $(PDFDIR)/$(MAIN).pdf

$(PDFDIR)/$(MAIN).pdf: $(SRCDIR)/$(MAIN).tex $(wildcard $(SRCDIR)/*.tex)
	mkdir -p $(PDFDIR)
	cd $(SRCDIR) && $(XELATEX) $(MAIN).tex
	cd $(SRCDIR) && $(XELATEX) $(MAIN).tex   # andre gong for innhaldsliste

clean:
	rm -f $(PDFDIR)/*.aux $(PDFDIR)/*.log $(PDFDIR)/*.toc $(PDFDIR)/*.out
