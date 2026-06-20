# GRUNNLAUST — Makefile
# Krev: xelatex + biber (forfattar–år-bibliografi via biblatex).

SRCDIR = src
PDFDIR = pdf
MAIN   = grunnlaust
XELATEX = xelatex -interaction=nonstopmode

.PHONY: all clean

all: $(PDFDIR)/$(MAIN).pdf

# Full sekvens: xelatex → biber → xelatex → xelatex (kryssreferansar + bibliografi).
$(PDFDIR)/$(MAIN).pdf: $(SRCDIR)/$(MAIN).tex $(wildcard $(SRCDIR)/*.tex) referansar.bib
	mkdir -p $(PDFDIR)
	cd $(SRCDIR) && $(XELATEX) -output-directory=../$(PDFDIR) $(MAIN).tex
	cd $(PDFDIR) && biber $(MAIN)
	cd $(SRCDIR) && $(XELATEX) -output-directory=../$(PDFDIR) $(MAIN).tex
	cd $(SRCDIR) && $(XELATEX) -output-directory=../$(PDFDIR) $(MAIN).tex

clean:
	rm -f $(PDFDIR)/*.aux $(PDFDIR)/*.log $(PDFDIR)/*.toc $(PDFDIR)/*.out \
	      $(PDFDIR)/*.bbl $(PDFDIR)/*.bcf $(PDFDIR)/*.blg $(PDFDIR)/*.run.xml
