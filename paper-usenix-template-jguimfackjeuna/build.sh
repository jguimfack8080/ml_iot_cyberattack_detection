#!/usr/bin/env bash
# =============================================================================
# build.sh -- Compilation du paper USENIX (pdflatex + BibTeX)
#
# Genere : jguimfackjeuna-main.pdf dans le repertoire courant
# Artefacts de compilation : stockes dans build/ (exclu du git)
#
# Usage :
#   bash build.sh            Compilation complete
#   bash build.sh --clean    Suppression des artefacts et du PDF
#   bash build.sh --watch    Recompile automatiquement a chaque modification
# =============================================================================
set -euo pipefail

MAIN="jguimfackjeuna-main"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"

cd "$SCRIPT_DIR"

# -----------------------------------------------------------------------
# --clean : supprime les artefacts de compilation et le PDF genere
# -----------------------------------------------------------------------
if [[ "${1:-}" == "--clean" ]]; then
    echo "[clean] Suppression de build/ ..."
    rm -rf "$BUILD_DIR"
    rm -f "$SCRIPT_DIR/$MAIN.pdf"
    echo "[clean] Termine."
    exit 0
fi

# -----------------------------------------------------------------------
# --watch : recompile automatiquement a chaque modification des .tex/.bib
# -----------------------------------------------------------------------
if [[ "${1:-}" == "--watch" ]]; then
    if ! command -v latexmk &>/dev/null; then
        echo "[erreur] --watch requiert latexmk. Installer : sudo apt-get install latexmk" >&2
        exit 1
    fi
    echo "[watch] Surveillance activee. Ctrl+C pour arreter."
    latexmk -pdf -pvc \
        -pdflatex="pdflatex -interaction=nonstopmode -halt-on-error %O %S" \
        -output-directory="$BUILD_DIR" \
        "$MAIN.tex"
    exit 0
fi

# -----------------------------------------------------------------------
# Verification des prerequis
# -----------------------------------------------------------------------
if [[ ! -f "$MAIN.tex" ]]; then
    echo "[erreur] Fichier principal introuvable : $MAIN.tex" >&2
    echo "         Verifier que le script est dans paper-usenix-template-jguimfackjeuna/" >&2
    exit 1
fi

if [[ ! -f "usenix-2020-09.sty" ]]; then
    echo "[erreur] Style USENIX introuvable : usenix-2020-09.sty" >&2
    exit 1
fi

if [[ ! -f "references.bib" ]]; then
    echo "[erreur] Bibliographie introuvable : references.bib" >&2
    exit 1
fi

# Verifier pdflatex
if ! command -v pdflatex &>/dev/null; then
    echo "[erreur] pdflatex introuvable. Installer TexLive :" >&2
    echo "         sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-lang-german texlive-fonts-recommended latexmk" >&2
    exit 1
fi

# Verifier le support de la langue allemande (babel ngerman)
if ! kpsewhich ngerman.ldf &>/dev/null 2>&1; then
    echo "" >&2
    echo "[erreur] Support de l'allemand introuvable (ngerman.ldf)" >&2
    echo "         Installer le paquet langue : sudo apt-get install -y texlive-lang-german" >&2
    echo "" >&2
    exit 1
fi

# -----------------------------------------------------------------------
# Compilation
# -----------------------------------------------------------------------
mkdir -p "$BUILD_DIR"

echo "======================================================================"
echo " Compilation : $MAIN.tex"
echo " Repertoire  : $SCRIPT_DIR"
echo " Artefacts   : $BUILD_DIR/"
echo "======================================================================"

if command -v latexmk &>/dev/null; then
    # Methode recommandee : latexmk gere toutes les passes automatiquement
    echo "[build] Outil : latexmk"
    latexmk -pdf \
        -pdflatex="pdflatex -interaction=nonstopmode -halt-on-error %O %S" \
        -bibtex \
        -output-directory="$BUILD_DIR" \
        "$MAIN.tex"
else
    # Methode de secours : compilation manuelle en 4 passes
    echo "[build] Outil : pdflatex + bibtex (latexmk non disponible)"
    echo "[build] Passe 1/4 : pdflatex (generation des .aux)"
    pdflatex -interaction=nonstopmode -halt-on-error \
        -output-directory="$BUILD_DIR" "$MAIN.tex"

    echo "[build] Passe 2/4 : bibtex (resolution de la bibliographie)"
    # BIBINPUTS indique a bibtex ou trouver references.bib
    (cd "$BUILD_DIR" && BIBINPUTS="$SCRIPT_DIR:." bibtex "$MAIN")

    echo "[build] Passe 3/4 : pdflatex (references croisees)"
    pdflatex -interaction=nonstopmode -halt-on-error \
        -output-directory="$BUILD_DIR" "$MAIN.tex"

    echo "[build] Passe 4/4 : pdflatex (passage final)"
    pdflatex -interaction=nonstopmode -halt-on-error \
        -output-directory="$BUILD_DIR" "$MAIN.tex"
fi

# -----------------------------------------------------------------------
# Copie du PDF dans le repertoire du paper
# -----------------------------------------------------------------------
PDF_BUILD="$BUILD_DIR/$MAIN.pdf"
PDF_OUT="$SCRIPT_DIR/$MAIN.pdf"

if [[ -f "$PDF_BUILD" ]]; then
    cp "$PDF_BUILD" "$PDF_OUT"
    echo ""
    echo "======================================================================"
    echo " SUCCES : PDF genere"
    echo " Chemin WSL     : $PDF_OUT"
    if command -v wslpath &>/dev/null; then
        WIN_PATH="$(wslpath -w "$PDF_OUT" 2>/dev/null || echo "(wslpath indisponible)")"
        echo " Chemin Windows : $WIN_PATH"
    fi
    echo "======================================================================"
else
    echo ""
    echo "[erreur] PDF non genere."
    echo "         Consulter le log : $BUILD_DIR/$MAIN.log"
    echo "         Commande rapide  : grep -i 'error' '$BUILD_DIR/$MAIN.log' | head -20"
    exit 1
fi
