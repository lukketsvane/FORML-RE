# GRUNNLAUS DESIGN — omslag
#   omslag.pdf       smussomslag (dust jacket, med flikar)
#   omslag-perm.pdf  hardcase-perm (case wrap, utan flikar)
# Krev: xelatex + python3 (Pillow).

.PHONY: all art clean

all: omslag.pdf omslag-perm.pdf

art: art/title-frost.png

art/title-frost.png: make-art.py
	python3 make-art.py

omslag.pdf: omslag.tex art/title-frost.png
	xelatex -interaction=nonstopmode omslag.tex
	xelatex -interaction=nonstopmode omslag.tex

omslag-perm.pdf: omslag-perm.tex art/title-frost.png
	xelatex -interaction=nonstopmode omslag-perm.tex
	xelatex -interaction=nonstopmode omslag-perm.tex

clean:
	rm -f *.aux *.log *.out
