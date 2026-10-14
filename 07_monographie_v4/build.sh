#!/bin/sh
# Reconstruit intégralement le volume PRISME v4.0 à partir des données.
set -e
cd "$(dirname "$0")/scripts"
python3 01_build_data.py
python3 02_stats.py
python3 03_catalogue.py
python3 04_generated.py
python3 05_figures.py
python3 06_textes.py
cd ../tex
rm -f main.aux main.toc main.lof main.lot main.out chapitres/*.aux
for i in 1 2 3; do xelatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null; done
echo "PDF : tex/main.pdf ($(pdfinfo main.pdf | awk '/Pages/{print $2}') pages)"
