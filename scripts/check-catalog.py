#!/usr/bin/env python3
"""check-catalog.py — гейт каталога скиллов.

Проверяет, что репозиторий остаётся каталогом, а не набором файлов:
  1. каждый `skills/<name>/` содержит `SKILL.md` с frontmatter `name` и `description`;
  2. `name` в frontmatter совпадает с именем каталога (по нему агент находит скилл);
  3. у каждого скилла есть `LICENSE.txt` — без заявленной лицензии публиковать нельзя;
  4. таблица «Каталог» в README перечисляет ровно те скиллы, что лежат в `skills/`
     (нет ни пропущенных, ни фантомных строк);
  5. в каталогах скиллов нет приватных артефактов (`*.local.md`, `.env*`).

Коды выхода: 0 — каталог цел, 1 — есть расхождения.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
README = ROOT / "README.md"

FORBIDDEN = re.compile(r"(^|/)\.env(\..*)?$|\.local\.md$")


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
        if not (skill / "LICENSE.txt").is_file():
            problems.append(f"{skill.name}: нет LICENSE.txt")
        for f in skill.rglob("*"):
            if f.is_file() and FORBIDDEN.search(str(f.relative_to(skill))):
                problems.append(f"{skill.name}: приватный файл в каталоге — {f.relative_to(skill)}")

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

    print(f"OK: {len(dirs)} скиллов, все с SKILL.md + LICENSE.txt и строкой в README")
    return 0


if __name__ == "__main__":
    sys.exit(main())
