# Care as Compass — build automation
# Usage: make en | make nn | make all | make figures | make clean

.PHONY: all en nn figures clean

all: figures en nn

figures:
	cd figures && python fig-2-morphospace.py
	cd figures && python fig-3-landscape.py

en: main-en.pdf

nn: main-nn.pdf

main-en.pdf: main-en.tex preamble.tex references.bib sections/*.tex figures/fig-1-architecture.tex
	pdflatex -interaction=nonstopmode main-en.tex
	biber main-en
	pdflatex -interaction=nonstopmode main-en.tex
	pdflatex -interaction=nonstopmode main-en.tex

main-nn.pdf: main-nn.tex preamble.tex references.bib sections/*-nn.tex
	pdflatex -interaction=nonstopmode main-nn.tex
	biber main-nn
	pdflatex -interaction=nonstopmode main-nn.tex
	pdflatex -interaction=nonstopmode main-nn.tex

clean:
	rm -f *.aux *.bbl *.bcf *.blg *.log *.out *.run.xml *.toc *.fls *.fdb_latexmk
	rm -f main-en.pdf main-nn.pdf
