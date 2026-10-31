.PHONY: all web pdf check
all: web pdf
web:
	node nettstad/build.mjs
pdf:
	python3 scripts/sync_latex.py
	mkdir -p build
	cd src && xelatex -interaction=nonstopmode -halt-on-error -output-directory=../build traktat.tex
	cd src && xelatex -interaction=nonstopmode -halt-on-error -output-directory=../build traktat.tex
check:
	node --test nettstad/reader.test.mjs
