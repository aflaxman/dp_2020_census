# dp_2020_census

Notebooks and draft text for Abraham D. Flaxman and Samantha Petti's
analyses of the US Census Bureau's TopDown algorithm applied to the
1940s US Census.

python compile_writeup.py; pandoc --filter pandoc-citeproc --bibliography=references.bib \
 --csl style.csl plugged_text.md -o dp_2020_census.docx