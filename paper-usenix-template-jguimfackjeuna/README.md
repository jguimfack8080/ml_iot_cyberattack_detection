# Paper USENIX -- Jordan Guimfack Jeuna (38184)
## Erklaerbare Erkennung von Cyberangriffen in IoT-Netzwerken

Seminararbeit -- IT-Sicherheit, M.Sc. IVS, Hochschule Bremerhaven
Betreuer : Prof. Dr. Lars Fischer

---

## Structure du repertoire

```
paper-usenix-template-jguimfackjeuna/
  build.sh                          Script de compilation (WSL)
  .latexmkrc                        Configuration latexmk
  usenix-2020-09.sty                Style USENIX 2019
  jguimfackjeuna-main.tex           Fichier LaTeX principal
  jguimfackjeuna-abstract.tex       Kurzfassung
  jguimfackjeuna-introduction.tex   Einleitung (section 1)
  jguimfackjeuna-related-work.tex   Related Work (section 2)
  jguimfackjeuna-methodik.tex       Methodik (section 3)
  jguimfackjeuna-evaluation.tex     Evaluation (section 4)
  jguimfackjeuna-discussion.tex     Diskussion (section 5)
  jguimfackjeuna-conclusion.tex     Fazit (section 6)
  references.bib                    Bibliographie (10 sources)
  build/                            Artefacts de compilation (genere, exclut du git)
  jguimfackjeuna-main.pdf           PDF genere (genere, exclu du git)
```

---

## Prerequis -- Installation de LaTeX dans WSL

### 1. Ouvrir WSL (Ubuntu/Debian)

Dans PowerShell Windows :
```powershell
wsl
```

### 2. Installer texlive et latexmk

**IMPORTANT : `texlive-lang-german` est obligatoire** (le paper est en allemand et
utilise `\usepackage[ngerman]{babel}`). Sans ce paquet, la compilation echoue avec :
`! Package babel Error: Unknown option 'ngerman'`

```bash
# Option recommandee : installation complete (environ 5 Go, installation unique)
sudo apt-get update
sudo apt-get install -y texlive-full

# Option minimale (plus rapide, suffisante pour ce paper)
sudo apt-get update
sudo apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-lang-german \
    texlive-fonts-recommended \
    texlive-bibtex-extra \
    latexmk
```

**Si l'erreur `Unknown option 'ngerman'` apparait malgre tout :**
```bash
sudo apt-get install -y texlive-lang-german
```

### 3. Verifier l'installation

```bash
latexmk --version
pdflatex --version
```

Les deux commandes doivent afficher un numero de version sans erreur.

---

## Compilation du paper (WSL)

### Etape 1 -- Naviguer vers le repertoire du paper dans WSL

Le projet est sur le disque Windows. Dans WSL, les disques Windows sont accessibles
via `/mnt/c/`, `/mnt/d/`, etc.

```bash
cd "/mnt/c/Users/jeuna/OneDrive/Bureau/Studium/M.Sc. IVS/Smester2/IT-Sicherheit/ml_iot_cyberattack_detection/paper-usenix-template-jguimfackjeuna"
```

Verification -- vous devez voir les fichiers .tex :
```bash
ls *.tex
# Attendu : jguimfackjeuna-main.tex jguimfackjeuna-abstract.tex ...
```

### Etape 2 -- Rendre le script executable (une seule fois)

```bash
chmod +x build.sh
```

### Etape 3 -- Compiler le paper

```bash
bash build.sh
```

Le script affiche la progression et indique le chemin du PDF a la fin :

```
======================================================================
 Compilation : jguimfackjeuna-main.tex
 Repertoire  : /mnt/c/Users/.../paper-usenix-template-jguimfackjeuna
 Artefacts   : .../paper-usenix-template-jguimfackjeuna/build/
======================================================================
[build] Outil : latexmk
...
======================================================================
 SUCCES : PDF genere
 Chemin WSL     : .../jguimfackjeuna-main.pdf
 Chemin Windows : C:\Users\jeuna\...\jguimfackjeuna-main.pdf
======================================================================
```

### Etape 4 -- Ouvrir le PDF depuis Windows

Apres compilation, le fichier `jguimfackjeuna-main.pdf` est genere directement
dans le repertoire `paper-usenix-template-jguimfackjeuna/`.

Il est accessible depuis Windows dans l'Explorateur de fichiers :
```
C:\Users\jeuna\OneDrive\Bureau\Studium\M.Sc. IVS\Smester2\IT-Sicherheit\
    ml_iot_cyberattack_detection\paper-usenix-template-jguimfackjeuna\
    jguimfackjeuna-main.pdf
```

Ou depuis WSL, l'ouvrir directement dans le navigateur PDF Windows :
```bash
# Ouvrir avec le lecteur PDF par defaut de Windows
explorer.exe "$(wslpath -w "$(pwd)/jguimfackjeuna-main.pdf")"
```

---

## Commandes disponibles

| Commande | Description |
|----------|-------------|
| `bash build.sh` | Compilation complete (recommandee) |
| `bash build.sh --clean` | Supprimer tous les artefacts et le PDF |
| `bash build.sh --watch` | Recompiler automatiquement a chaque sauvegarde |

### Compilation propre (apres modifications importantes)

```bash
bash build.sh --clean
bash build.sh
```

### Mode surveillance (utile pendant la redaction)

```bash
bash build.sh --watch
# Modifier un .tex, sauvegarder -> le PDF se regenere automatiquement
# Ctrl+C pour arreter
```

---

## Sequence de compilation detaillee

Le script execute la sequence standard pour pdflatex + BibTeX :

```
1. pdflatex jguimfackjeuna-main.tex   -> genere .aux (references)
2. bibtex   jguimfackjeuna-main       -> genere .bbl (bibliographie)
3. pdflatex jguimfackjeuna-main.tex   -> resout les citations
4. pdflatex jguimfackjeuna-main.tex   -> passage final
5. Copie du PDF vers le repertoire principal
```

Avec `latexmk` (recommande), toutes ces passes sont gerees automatiquement.

---

## Depannage

### Erreur : `Unknown option 'ngerman'` (babel)

Le paquet de langue allemande n'est pas installe :
```bash
sudo apt-get install -y texlive-lang-german
bash build.sh
```

### Erreur : "command not found: latexmk"

```bash
sudo apt-get install -y latexmk
```

Si latexmk n'est pas disponible, le script utilise automatiquement pdflatex
directement (4 passes manuelles).

### Erreur : "command not found: pdflatex"

```bash
sudo apt-get install -y texlive-latex-base
```

### Erreur : fichier .sty introuvable

Verifier que `usenix-2020-09.sty` est bien present dans le repertoire :
```bash
ls usenix-2020-09.sty
```
Si absent, le copier depuis la racine du projet :
```bash
cp ../usenix-2020-09.sty .
```

### Erreur LaTeX : citation non resolue (undefined citation)

Verifier que `references.bib` est bien present et que les cles BibTeX
dans les fichiers .tex correspondent exactement a celles de references.bib :
```bash
grep "\\\\cite{" jguimfackjeuna-*.tex | grep -oP '\\\\cite\{[^}]+\}' | sort -u
grep "^@" references.bib | grep -oP '\{[^,]+' | tr -d '{' | sort
```

### Erreur LaTeX : "File ended while scanning use of ..."

Indique une accolade `{` ou `}` non fermee dans un .tex.
Verifier le fichier cite dans le log d'erreur :
```bash
grep -n "error" build/jguimfackjeuna-main.log | head -20
```

### OneDrive sync -- permission refusee

Si OneDrive est en cours de synchronisation, les fichiers peuvent etre
verrouilles. Attendre la fin de la synchronisation ou desactiver
temporairement OneDrive pendant la compilation.

### Chemin avec espaces

Le chemin du projet contient des espaces ("M.Sc. IVS"). Le script gere
cela correctement. Ne pas modifier la commande `cd` du README.

---

## Fichiers exclus du git

Le fichier `.gitignore` a la racine du projet exclut :
- `paper-usenix-template-jguimfackjeuna/build/` (artefacts de compilation)
- `paper-usenix-template-jguimfackjeuna/*.pdf` (PDF genere)

Ces fichiers sont regenerables a tout moment avec `bash build.sh`.

---

## Regles du paper

- Langue : 100% allemand academique dans tous les fichiers .tex
- Limite : 10 pages maximum (format USENIX deux colonnes)
- Sources : 10 sources BibTeX uniquement (references.bib)
- Interdits : tirets cadratins (-- et ---) dans le texte LaTeX
- Chaque affirmation doit etre tracable a une des 10 sources ou aux
  resultats experimentaux du Backend
