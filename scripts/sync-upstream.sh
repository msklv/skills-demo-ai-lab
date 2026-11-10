#!/usr/bin/env bash
# Переимпорт скиллов из апстримов, перечисленных в upstreams.tsv, по пинам.
# Копирование каталогов без правок содержимого: свои скиллы живут отдельными каталогами,
# а не правками импортированных.
#
#   ./scripts/sync-upstream.sh                       # все апстримы, пины из upstreams.tsv
#   ./scripts/sync-upstream.sh anthropics/skills     # только один апстрим
#   UPSTREAM_REF=<commit|tag> ./scripts/sync-upstream.sh anthropics/skills   # пробный ref
#
# Требует: curl, tar. Каталог без SKILL.md не импортируется. Если у скилла нет своего
# LICENSE.txt, а у апстрима есть корневой LICENSE, он кладётся в каталог скилла: установленный
# отдельно скилл должен приезжать вместе с лицензией (Apache-2.0, п. 4 — сохранение notices).
set -euo pipefail
cd "$(dirname "$0")/.."

ONLY=${1:-}
TAB=$(printf '\t')
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p notices

total_imported=0
total_skipped=0

while IFS="$TAB" read -r repo pin skills_dir notices exclude; do
  case "${repo:-}" in ''|\#*) continue ;; esac
  if [ -n "$ONLY" ] && [ "$ONLY" != "$repo" ]; then continue; fi

  ref=${UPSTREAM_REF:-$pin}
  base=$(basename "$repo")
  slug=$(printf '%s' "$repo" | tr '/' '-' | tr '[:upper:]' '[:lower:]')
  echo "=== $repo @ $ref"

  curl -fsSL -o "$TMP/$base.tgz" "https://codeload.github.com/$repo/tar.gz/$ref"
  tar xzf "$TMP/$base.tgz" -C "$TMP"
  src=$(find "$TMP" -maxdepth 1 -type d -name "$base-*" -print -quit)
  [ -d "$src/$skills_dir" ] || { echo "  в архиве нет каталога $skills_dir" >&2; exit 1; }

  # Каталог в манифесте может быть папкой со скиллами, одним скиллом или всем репозиторием ("."):
  # если в нём самом лежит SKILL.md — импортируется он один (иначе приехали бы соседи по каталогу).
  if [ -f "$src/$skills_dir/SKILL.md" ]; then
    set -- "$src/$skills_dir"
  else
    set -- "$src/$skills_dir"/*/
  fi

  for dir in "$@"; do
    # имя берём из frontmatter (в режиме "." имя каталога — это распакованный архив апстрима)
    name=$(sed -n 's/^name:[[:space:]]*//p' "$dir/SKILL.md" | head -1 | tr -d "\"'" )
    [ -n "$name" ] || name=$(basename "$dir")
    case ",$exclude," in
      *",$name,"*) echo "  skip  $name — исключён (upstreams.tsv)"; total_skipped=$((total_skipped+1)); continue ;;
    esac
    if [ ! -f "$dir/SKILL.md" ]; then
      echo "  skip  $name — нет SKILL.md (не скилл)"
      total_skipped=$((total_skipped+1))
      continue
    fi
    rm -rf "skills/$name"
    cp -R "$dir" "skills/$name"
    # режим ".": не тащим инфраструктуру апстрима (CI, плагин-манифесты, node_modules)
    if [ "$skills_dir" = "." ]; then
      rm -rf "skills/$name"/.[!.]* "skills/$name"/node_modules "skills/$name"/package.json
    fi
    # лицензия элемента главнее репозиторной: у агрегатора в каталоге может лежать
    # вендоренный элемент со своим копирайтом (тогда автор — не владелец репозитория)
    if [ -f "skills/$name/LICENSE" ] && [ ! -f "skills/$name/LICENSE.txt" ]; then
      mv "skills/$name/LICENSE" "skills/$name/LICENSE.txt"
    fi
    if [ ! -f "skills/$name/LICENSE.txt" ]; then
      if [ -f "$src/LICENSE" ]; then
        cp "$src/LICENSE" "skills/$name/LICENSE.txt"
      else
        echo "  ВНИМАНИЕ: $name без лицензии — публиковать нельзя, разбирайся с апстримом" >&2
      fi
    fi
    echo "  import $name"
    total_imported=$((total_imported+1))
  done

  if [ -n "$notices" ] && [ -f "$src/$notices" ]; then
    {
      echo "<!-- Скопировано дословно из github.com/$repo@$ref ($notices): атрибуция сторонних"
      echo "компонентов, которые тянут скиллы. Не редактируется — переимпорт кладёт файл заново. -->"
      echo
      cat "$src/$notices"
    } > "notices/$slug.md"
    echo "  notices → notices/$slug.md"
  fi
done < upstreams.tsv

echo "импортировано: $total_imported, пропущено: $total_skipped"
echo "дальше: python3 scripts/check-catalog.py; обновить таблицы в UPSTREAM.md и README.md"
