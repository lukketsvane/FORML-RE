# GRUNNLAUS DESIGN — smussomslag (dust jacket)
# Krev: xelatex + python3 (Pillow, python-barcode).

.PHONY: all art clean

all: omslag.pdf

art: art/title-frost.png art/ean13.png

art/title-frost.png art/ean13.png: make-art.py
	python3 make-art.py

omslag.pdf: omslag.tex art/title-frost.png art/ean13.png
	xelatex -interaction=nonstopmode omslag.tex
	xelatex -interaction=nonstopmode omslag.tex

clean:
	rm -f omslag.aux omslag.log omslag.out
