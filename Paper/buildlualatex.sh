#!/bin/bash

set -euo pipefail

tex_main="${TEX_MAIN:-hauptdatei.tex}"
outdir="${OUTDIR:-log}"

if [ "${1:-}" = "--remote-only" ]; then
  script_dir="$(cd "$(dirname "$0")" && pwd -P)"
  tex_main_path="$tex_main"
  if [[ "$tex_main_path" != /* ]]; then
    tex_main_abs="$(cd "$script_dir" && cd "$(dirname "$tex_main_path")" && pwd -P)/$(basename "$tex_main_path")"
  else
    tex_main_abs="$tex_main_path"
  fi
  build_dir="$(cd "$(dirname "$tex_main_abs")" && pwd -P)"
  tex_main_base="$(basename "$tex_main_abs")"
  pdf_basename="${tex_main_base%.tex}.pdf"
  outdir_abs="$build_dir/$outdir"
  mkdir -p "$outdir_abs"
  set +e
  if [ "$tex_main_base" = "usenix2019_v3.1.tex" ] || [ "$tex_main_base" = "jguimfackjeuna-related-work.tex" ]; then
    (cd "$build_dir" && latexmk -pdf -interaction=nonstopmode -f -outdir="$outdir" "$tex_main_base")
  else
    (cd "$build_dir" && latexmk -pdf -lualatex -interaction=nonstopmode -f -outdir="$outdir" "$tex_main_base")
  fi
  latexmk_rc=$?
  set -e
  if [ "$latexmk_rc" -ne 0 ] && [ -f "$outdir_abs/$pdf_basename" ]; then
    latexmk_rc=0
  fi
  if [ -f "$outdir_abs/$pdf_basename" ]; then
    mv -f "$outdir_abs/$pdf_basename" "$script_dir/$pdf_basename"
  else
    echo "Kein PDF erzeugt: $outdir_abs/$pdf_basename" >&2
  fi
  publish_dir="${PUBLISH_DIR:-/var/www/html/${USER}/}"
  if [ -n "$publish_dir" ]; then
    mkdir -p "${publish_dir%/}/"
    cp -f "$script_dir/$pdf_basename" "${publish_dir%/}/"
  fi
  exit "$latexmk_rc"
fi

remote_host="${REMOTE_HOST:-hopper}"
remote_tmp_parent="${REMOTE_TMP_PARENT:-/tmp}"
keep_remote="${KEEP_REMOTE:-0}"

paper_dir="$(cd "$(dirname "$0")" && pwd -P)"
project_root="$(cd "$paper_dir/.." && pwd -P)"
tex_main_base="$(basename "$tex_main")"
pdf_basename="${tex_main_base%.tex}.pdf"

control_dir="$(mktemp -d)"
control_path="$control_dir/ctl"

ssh_opts=(
  -o ControlMaster=auto
  -o ControlPersist=60
  -o ControlPath="$control_path"
)

cleanup() {
  rm -rf "$control_dir"
}
trap cleanup EXIT

ssh_cmd() {
  ssh "${ssh_opts[@]}" "$remote_host" "$@"
}

remote_build_dir="$(ssh_cmd "mktemp -d \"$remote_tmp_parent/ml_iot_paper_build.XXXXXXXX\"")"
remote_build_dir="${remote_build_dir//$'\r'/}"
remote_build_dir="${remote_build_dir//$'\n'/}"

tex_main_abs="$(cd "$paper_dir" && cd "$(dirname "$tex_main")" && pwd -P)/$(basename "$tex_main")"
remote_pdf_path="$remote_build_dir/$pdf_basename"
remote_script_dir="$remote_build_dir"
remote_script_path="./buildlualatex.sh"

if [[ "$tex_main_abs" == "$paper_dir/"* ]]; then
  tar -C "$paper_dir" \
    --exclude="./log" \
    --exclude="./*.pdf" \
    --exclude="./.git" \
    -czf - . \
    | ssh "${ssh_opts[@]}" "$remote_host" "tar -xzf - -C \"$remote_build_dir\""
else
  if [[ "$tex_main_abs" != "$project_root/"* ]]; then
    echo "TEX_MAIN liegt außerhalb des Projektverzeichnisses und kann nicht remote gebaut werden: $tex_main_abs" >&2
    exit 2
  fi
  tex_main_rel="${tex_main_abs#$project_root/}"
  if [ ! -f "$project_root/usenix-2020-09.sty" ]; then
    echo "Fehlende Datei im Projekt-Root: usenix-2020-09.sty" >&2
    exit 2
  fi
  tar -C "$project_root" \
    --exclude="./Paper/log" \
    --exclude="./Paper/*.pdf" \
    --exclude="./Paper/.git" \
    -czf - Paper "$tex_main_rel" "jguimfackjeuna-related-work.tex" "usenix-2020-09.sty" \
    | ssh "${ssh_opts[@]}" "$remote_host" "tar -xzf - -C \"$remote_build_dir\""
  remote_script_dir="$remote_build_dir/Paper"
  remote_script_path="./buildlualatex.sh"
  remote_pdf_path="$remote_build_dir/Paper/$pdf_basename"
fi

ssh_cmd "cd \"$remote_script_dir\" && TEX_MAIN=\"$tex_main\" OUTDIR=\"$outdir\" bash \"$remote_script_path\" --remote-only"
if ssh_cmd "test -f \"$remote_pdf_path\""; then
  ssh_cmd "cat \"$remote_pdf_path\"" > "$paper_dir/$pdf_basename"
else
  echo "Remote PDF nicht gefunden: $remote_pdf_path" >&2
  exit 1
fi

if [ "$keep_remote" != "1" ]; then
  ssh_cmd "rm -rf \"$remote_build_dir\""
fi
