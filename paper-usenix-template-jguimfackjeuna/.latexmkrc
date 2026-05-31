# .latexmkrc -- Configuration latexmk pour le paper USENIX
# Format : pdflatex (pas LuaLaTeX)

# Mode PDF via pdflatex
$pdf_mode = 1;

# Commande pdflatex
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error %O %S';

# Activer BibTeX pour la bibliographie
$bibtex_use = 1;

# Extensions supplementaires a supprimer avec latexmk --clean
$clean_ext = 'bbl blg fdb_latexmk fls idx ilg ind lof lol lot run.xml synctex.gz toc nav snm vrb';
