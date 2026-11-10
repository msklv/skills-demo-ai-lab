#!/usr/bin/env python3
"""check-catalog.py — гейт каталога скиллов.

Проверяет, что репозиторий остаётся каталогом, а не набором файлов:
  1. каждый `skills/<name>/` содержит `SKILL.md` с frontmatter `name` и `description`;
  2. `name` в frontmatter совпадает с именем каталога (по нему агент находит скилл);
  3. у каждого скилла есть `LICENSE.txt` — без заявленной лицензии публиковать нельзя;
  4. таблица «Каталог» в README перечисляет ровно те скиллы, что лежат в `skills/`
     (нет ни пропущенных, ни фантомных строк);
  5. в каталогах скиллов нет приватных артефактов (`*.local.md`, `.env*`);
  6. `upstreams.tsv` — пины по коммиту (40 hex), notices апстрима скопирован в `notices/`;
  7. лицензия каждого скилла — из белого списка открытых (непроприетарных) лицензий.

Коды выхода: 0 — каталог цел, 1 — есть расхождения.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
UPSTREAMS = ROOT / "upstreams.tsv"
NOTICES = ROOT / "notices"
PIN = re.compile(r"^[0-9a-f]{40}$")

FORBIDDEN = re.compile(r"(^|/)\.env(\..*)?$|\.local\.md$")

# Белый список: только открытые лицензии. Порядок важен — проверяем по маркерам текста.
OPEN_LICENSES = (
    ("Apache-2.0", "Apache License"),
    ("MIT", "MIT License"),
    ("MIT", "Permission is hereby granted, free of charge"),
    ("BSD-2-Clause", "BSD 2-Clause"),
    ("BSD-3-Clause", "BSD 3-Clause"),
    ("ISC", "ISC License"),
    ("MPL-2.0", "Mozilla Public License Version 2.0"),
    ("OFL-1.1", "SIL OPEN FONT LICENSE"),
    ("CC0-1.0", "CC0 1.0 Universal"),
    ("CC-BY-4.0", "Creative Commons Attribution 4.0"),
    ("Unlicense", "This is free and unencumbered software released into the public domain"),
)


def open_license(path: Path) -> str | None:
    """Возвращает SPDX-подобный идентификатор, если текст лицензии узнан как открытый."""
    text = path.read_text(encoding="utf-8", errors="replace")
    for spdx, marker in OPEN_LICENSES:
        if marker in text:
            return spdx
    return None


def frontmatter(text: str) -> dict[str, str]:
    """Плоский разбор YAML-frontmatter без зависимостей: name, description (в т.ч. block-scalar)."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out: dict[str, str] = {}
    key = None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^[A-Za-z_][\w-]*:", line):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            out[key] = "" if value in (">", ">−", "|", "|-", ">-", "") else value.strip("\"'")
        elif key and line.startswith((" ", "\t")):
            out[key] = (out.get(key, "") + " " + line.strip()).strip()
    return out


def main() -> int:
    problems: list[str] = []
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir()) if SKILLS.is_dir() else []
    if not dirs:
        print(f"FAIL: нет каталога {SKILLS} или он пуст")
        return 1

    for skill in dirs:
        md = skill / "SKILL.md"
        if not md.is_file():
            problems.append(f"{skill.name}: нет SKILL.md")
            continue
        fm = frontmatter(md.read_text(encoding="utf-8"))
        if not fm.get("name"):
            problems.append(f"{skill.name}: в frontmatter нет name")
        elif fm["name"] != skill.name:
            problems.append(f"{skill.name}: name={fm['name']!r} не совпадает с каталогом")
        if not fm.get("description"):
            problems.append(f"{skill.name}: в frontmatter нет description")
        lic = skill / "LICENSE.txt"
        if not lic.is_file():
            problems.append(f"{skill.name}: нет LICENSE.txt")
        elif not open_license(lic):
            problems.append(f"{skill.name}: лицензия не распознана как открытая — публиковать нельзя")
        for f in skill.rglob("*"):
            if f.is_file() and FORBIDDEN.search(str(f.relative_to(skill))):
                problems.append(f"{skill.name}: приватный файл в каталоге — {f.relative_to(skill)}")

    # апстримы: пин коммитом, notices на месте
    if not UPSTREAMS.is_file():
        problems.append("нет upstreams.tsv")
    else:
        for line in UPSTREAMS.read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            field = line.split("\t")
            if len(field) < 4:
                problems.append(f"upstreams.tsv: строка без 4 колонок — {line[:60]}")
                continue
            repo, pin, _skills_dir, notices = field[0], field[1], field[2], field[3]
            if "/" not in repo:
                problems.append(f"upstreams.tsv: repo без owner/name — {repo}")
            if not PIN.match(pin):
                problems.append(f"upstreams.tsv: пин не коммит 40 hex — {repo}: {pin[:20]}")
            slug = repo.replace("/", "-").lower()
            target = NOTICES / f"{slug}.md"
            if notices and not target.is_file():
                problems.append(f"upstreams.tsv: нет notices/{slug}.md (заявлен {notices})")

    names = {p.name for p in dirs}
    if not README.is_file():
        problems.append("нет README.md")
    else:
        text = README.read_text(encoding="utf-8")
        listed = set(re.findall(r"^\|\s*\[([a-z0-9-]+)\]\(skills/", text, re.M))
        missing = names - listed
        phantom = listed - names
        if missing:
            problems.append(f"README: не перечислены скиллы — {', '.join(sorted(missing))}")
        if phantom:
            problems.append(f"README: строки без каталога — {', '.join(sorted(phantom))}")

    if problems:
        print(f"FAIL: {len(problems)} расхождени(й)")
        for p in problems:
            print(f"  - {p}")
        return 1

    kinds: dict[str, int] = {}
    for skill in dirs:
        lic = skill / "LICENSE.txt"
        if lic.is_file():
            kinds[open_license(lic) or "?"] = kinds.get(open_license(lic) or "?", 0) + 1
    summary = ", ".join(f"{k} ×{v}" for k, v in sorted(kinds.items()))
    print(f"OK: {len(dirs)} скиллов ({summary}); SKILL.md + LICENSE.txt + строка в README у каждого; пины валидны")
    return 0


if __name__ == "__main__":
    sys.exit(main())
