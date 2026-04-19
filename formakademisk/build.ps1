# Build script for Formlære
Write-Host "Starting build for formlaere.tex..."

xelatex -interaction=nonstopmode formlaere.tex
if ($LASTEXITCODE -ne 0) { Write-Error "First xelatex run failed"; exit $LASTEXITCODE }

bibtex formlaere
if ($LASTEXITCODE -ne 0) { Write-Error "BibTeX run failed"; exit $LASTEXITCODE }

xelatex -interaction=nonstopmode formlaere.tex
if ($LASTEXITCODE -ne 0) { Write-Error "Second xelatex run failed"; exit $LASTEXITCODE }

xelatex -interaction=nonstopmode formlaere.tex
if ($LASTEXITCODE -ne 0) { Write-Error "Third xelatex run failed"; exit $LASTEXITCODE }

Write-Host "Build complete! Output: formlaere.pdf"
