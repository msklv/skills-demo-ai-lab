#!/usr/bin/env bash
# Переимпорт скиллов из апстрима (anthropics/skills) по пину.
# Копирование каталогов без правок содержимого: свои скиллы живут отдельными каталогами,
# а не правками импортированных.
#
#   ./scripts/sync-upstream.sh                # переимпорт по пину из UPSTREAM.md
#   ./scripts/sync-upstream.sh <commit|tag>   # другой ref (пин в UPSTREAM.md правится вручную)
#
# Требует: curl, tar. Каталоги без LICENSE.txt не импортируются (права не заявлены).
set -euo pipefail
cd "$(dirname "$0")/.."

REPO=${UPSTREAM_REPO:-anthropics/skills}
PIN=$(awk -F'`' '/^\| Коммит /{print $2; exit}' UPSTREAM.md)
REF=${1:-${PIN:-main}}
[ -n "$REF" ] || { echo "не нашёл пин в UPSTREAM.md — передайте ref аргументом" >&2; exit 1; }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

echo "апстрим: $REPO @ $REF"
curl -fsSL -o "$TMP/up.tgz" "https://codeload.github.com/$REPO/tar.gz/$REF"
tar xzf "$TMP/up.tgz" -C "$TMP"
SRC=$(find "$TMP" -maxdepth 1 -type d -name 'skills-*' -print -quit)
[ -d "$SRC/skills" ] || { echo "в архиве нет каталога skills/" >&2; exit 1; }

imported=0
skipped=0
for dir in "$SRC"/skills/*/; do
  name=$(basename "$dir")
  if [ ! -f "$dir/LICENSE.txt" ]; then
    echo "skip  $name — нет LICENSE.txt (права на распространение не заявлены)"
    skipped=$((skipped + 1))
    continue
  fi
  rm -rf "skills/$name"
  cp -R "$dir" "skills/$name"
  echo "import $name"
  imported=$((imported + 1))
done

{
  echo "<!-- Скопировано дословно из github.com/$REPO@$REF (THIRD_PARTY_NOTICES.md): атрибуция"
  echo "сторонних компонентов, которые тянут скиллы (imageio, FFmpeg и др.). Не редактируется —"
  echo "при обновлении пина копируется заново скриптом scripts/sync-upstream.sh. -->"
  echo
  cat "$SRC/THIRD_PARTY_NOTICES.md"
} > THIRD_PARTY_NOTICES.md

echo "импортировано: $imported, пропущено: $skipped"
echo "дальше: python3 scripts/check-catalog.py; обновить пин/таблицы в UPSTREAM.md и README.md"
