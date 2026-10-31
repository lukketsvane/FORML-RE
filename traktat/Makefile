.PHONY: all web pdf check
all: pdf web
web:
	node nettstad/build.mjs
pdf:
	python3 scripts/sync_latex.py
	mkdir -p build
	cd src && xelatex -interaction=nonstopmode -halt-on-error -output-directory=../build traktat.tex
	cd src && xelatex -interaction=nonstopmode -halt-on-error -output-directory=../build traktat.tex
	cp build/traktat.pdf pdf/traktat.pdf
check:
	node --test nettstad/reader.test.mjs
