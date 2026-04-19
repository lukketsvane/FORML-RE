# Formlære - build automation
# Usage: make | make clean

.PHONY: all clean figures

all: formlaere.pdf

figures:
	cd figures && python _generate_article_figures.py
	cd figures && python _generate_empiri_figures.py
	cd figures && python _generate_grafisk_samandrag.py
	cd figures && python _generate_grensetilfelle.py

formlaere.pdf: formlaere.tex formlaere.bib
	xelatex -interaction=nonstopmode formlaere.tex
	bibtex formlaere
	xelatex -interaction=nonstopmode formlaere.tex
	xelatex -interaction=nonstopmode formlaere.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.pdf
