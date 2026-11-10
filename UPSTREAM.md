# UPSTREAM — происхождение и пин апстрима

Импорт — **копирование каталогов**, без правок содержимого. Пересобрать всё можно одной
командой (`scripts/sync-upstream.sh`), поэтому пин и список исключений здесь — единственный
источник правды о происхождении файлов в `skills/`.

## Пин

| Параметр | Значение |
|---|---|
| Репозиторий | [`anthropics/skills`](https://github.com/anthropics/skills) (`skills/`) |
| Коммит | `2c5958ecac7cee2b583967a2c4981d0f4a75c579` (main, дата коммита 2026-11-06) |
| Дата импорта | 2026-11-10 |
| Импортировано | 18 скиллов, 439 файлов, ≈11,6 МБ |
| Лицензия апстрима | у каждого скилла свой `LICENSE.txt` — **Apache-2.0** у всех 18 (см. разбор ниже) |

## Что импортировано

| Скилл | Файлов | КБ | Лицензия |
|---|---|---|---|
| `academy-guide` | 2 | 19 | Apache-2.0 |
| `algorithmic-art` | 4 | 58 | Apache-2.0 |
| `brand-guidelines` | 2 | 13 | Apache-2.0 |
| `canvas-design` | 83 | 5424 | Apache-2.0 |
| `claude-api` | 96 | 2031 | Apache-2.0 |
| `discernment-nudge` | 2 | 21 | Apache-2.0 |
| `docx` | 61 | 1112 | Apache-2.0 |
| `frontend-design` | 2 | 19 | Apache-2.0 |
| `internal-comms` | 6 | 22 | Apache-2.0 |
| `mcp-builder` | 11 | 155 | Apache-2.0 |
| `pdf` | 12 | 67 | Apache-2.0 |
| `pptx` | 56 | 1122 | Apache-2.0 |
| `skill-creator` | 18 | 220 | Apache-2.0 |
| `slack-gif-creator` | 7 | 43 | Apache-2.0 |
| `theme-factory` | 13 | 141 | Apache-2.0 |
| `web-artifacts-builder` | 5 | 45 | Apache-2.0 |
| `webapp-testing` | 6 | 22 | Apache-2.0 |
| `xlsx` | 53 | 1087 | Apache-2.0 |

Каталоги апстрима `spec/`, `template/`, `.claude-plugin/` не импортируются: это не скиллы
(`spec/` — описание формата, `template/` — болванка нового скилла, `.claude-plugin/` — манифест
маркетплейса Claude Code).

## Что исключено и почему

| Каталог апстрима | Причина |
|---|---|
| `doc-coauthoring` | **нет `LICENSE.txt`** (в апстриме файла нет, у репозитория нет корневой лицензии) — права на перераспространение не заявлены. Не публикуем и не переимпортируем, пока лицензия не появится |

## Лицензионный разбор (2026-11-10)

`LICENSE.txt` в апстриме существует у 19 из 20 каталогов апстрима и встречается в трёх вариантах
текста — все три являются **Apache License 2.0**, различаются только оформлением:

| Вариант | md5 | Где | Отличие |
|---|---|---|---|
| A | `0ee6429f…` | 15 скиллов | Apache-2.0, appendix с `Copyright 2026 Anthropic, PBC.` |
| B | `17579251…` | `docx`, `pdf`, `pptx`, `xlsx` | Apache-2.0, appendix с плейсхолдерами |
| C | `2ee41112…` | `frontend-design` | Apache-2.0 без appendix |

Проверка: `diff` любого файла против канонического текста Apache-2.0 даёт только строку
копирайта/appendix — ограничительных дополнений (запрет на commercial use, source-available
оговорок) нет. Файлы сохранены дословно в каталогах скиллов.

Ассеты: шрифты `canvas-design/canvas-fonts/*.ttf` сопровождаются `*-OFL.txt` (SIL OFL 1.1);
сторонние runtime-компоненты (imageio, FFmpeg и др.) — `THIRD_PARTY_NOTICES.md`, скопирован из
апстрима дословно.

## Обновление пина

```bash
scripts/sync-upstream.sh <новый-commit-sha>   # копирует каталоги заново, исключения — ниже
scripts/check-catalog.py                      # гейт: у всех скиллов SKILL.md/description/LICENSE
```

После импорта: обновить таблицы в этом файле (пин, дата, файлы/размеры) и строки в
`README.md`, если состав изменился; в репозитории `msklv/demo-ai-lab` — ничего
(ADR-0010 фиксирует механизм, а не список файлов).
