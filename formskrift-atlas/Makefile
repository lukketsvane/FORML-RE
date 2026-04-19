# Formskrift-atlaset - Makefile
# Krev: xelatex, pdfunite, Symbola-fonten

TEXDIR = tex
PDFDIR = pdf
XELATEX = xelatex -interaction=nonstopmode -output-directory=$(PDFDIR)

# Alle kjelder
SOURCES = forside notasjon \
          pg-seksjon-1 pg-seksjon-2 pg-seksjon-3 pg-seksjon-4 \
          pg-seksjon-5 pg-seksjon-6 pg-seksjon-7 pg-seksjon-8 \
          skalahierarki \
          formskrift-einside formskrift-bevis-einside

PDFS = $(SOURCES:%=$(PDFDIR)/%.pdf)

# Default: byg alt
.PHONY: all atlas formskrift clean

all: atlas

# Bygg alle komponentar og sett saman
atlas: $(PDFDIR)/formlaere-atlas-samla.pdf

$(PDFDIR)/formlaere-atlas-samla.pdf: $(PDFS)
	cd $(PDFDIR) && pdfunite \
		forside.pdf notasjon.pdf \
		pg-seksjon-1.pdf pg-seksjon-2.pdf pg-seksjon-3.pdf pg-seksjon-4.pdf \
		pg-seksjon-5.pdf pg-seksjon-6.pdf pg-seksjon-7.pdf pg-seksjon-8.pdf \
		skalahierarki.pdf \
		formskrift-einside.pdf formskrift-bevis-einside.pdf \
		formlaere-atlas-samla.pdf

# Berre formskrift-sidene
formskrift: $(PDFDIR)/formskrift-einside.pdf $(PDFDIR)/formskrift-bevis-einside.pdf

# Kompileringsregel for kvar .tex
$(PDFDIR)/%.pdf: $(TEXDIR)/%.tex
	$(XELATEX) $<
	$(XELATEX) $< # andre gong for referansar

clean:
	rm -f $(PDFDIR)/*.aux $(PDFDIR)/*.log $(PDFDIR)/*.out

distclean: clean
	rm -f $(PDFDIR)/*.pdf
