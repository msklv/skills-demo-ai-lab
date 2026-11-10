# UPSTREAM — происхождение и пины апстримов

Импорт — **копирование каталогов**, без правок содержимого. Пересобрать всё можно одной
командой (`scripts/sync-upstream.sh`), поэтому пины и исключения живут в `upstreams.tsv`, а
описание и лицензионный разбор — здесь.

## Апстримы

| Репозиторий | Пин (коммит) | Дата коммита | Импортировано | Лицензия |
|---|---|---|---|---|
| [`anthropics/skills`](https://github.com/anthropics/skills) | `2c5958ecac7cee2b583967a2c4981d0f4a75c579` | 2026-11-06 | 18 скиллов | Apache-2.0, у каждого свой `LICENSE.txt` |
| [`ClickHouse/agent-skills`](https://github.com/ClickHouse/agent-skills) | `d3b2b5ba43a8b80c2d08858b68d53edc701b5ace` | 2026-11-02 | 11 скиллов | Apache-2.0, корневой `LICENSE` репозитория |
| [`NousResearch/hermes-agent`](https://github.com/NousResearch/hermes-agent) | `b3746e35ddd32079697728e2df57a9d78f1e9e32` | 2026-11-10 | 1 скилл (`skills/creative/popular-web-designs`) | MIT, корневой `LICENSE` репозитория |
| [`obra/superpowers`](https://github.com/obra/superpowers) | `22f0b463e7a5e579904dd6211a520321035526f7` | 2026-11-03 | 15 скиллов (`skills/`) | MIT, корневой `LICENSE` репозитория |
| [`Cocoon-AI/architecture-diagram-generator`](https://github.com/Cocoon-AI/architecture-diagram-generator) | `4b9087d55268c79a935105439dbcd37b630fc3f3` | 2026-05-13 | 1 скилл (`architecture-diagram/`) | MIT, корневой `LICENSE` репозитория |
| [`blader/humanizer`](https://github.com/blader/humanizer) | `e97c2c49ce0eb2990b83277da22a0c07a242b679` | 2026-11-10 | 1 скилл (репозиторий целиком) | MIT, файл `LICENSE` самого скилла |

Дата импорта — 2026-11-10. Итого 51 скилл, ≈16 МБ.

## anthropics/skills — импортировано

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

## ClickHouse/agent-skills — импортировано

| Скилл | Файлов | КБ | Лицензия |
|---|---|---|---|
| `chdb-datastore` | 8 | 47 | Apache-2.0 |
| `chdb-sql` | 9 | 51 | Apache-2.0 |
| `clickhouse-architecture-advisor` | 16 | 39 | Apache-2.0 |
| `clickhouse-best-practices` | 38 | 150 | Apache-2.0 |
| `clickhouse-js-node-coding` | 14 | 93 | Apache-2.0 |
| `clickhouse-js-node-rowbinary` | 194 | 690 | Apache-2.0 |
| `clickhouse-js-node-troubleshooting` | 11 | 44 | Apache-2.0 |
| `clickhouse-managed-postgres-rca` | 14 | 80 | Apache-2.0 |
| `clickstack-otel-collector` | 3 | 50 | Apache-2.0 |
| `infra-clickhouse` | 6 | 28 | Apache-2.0 |
| `infra-postgres` | 7 | 35 | Apache-2.0 |

Импортированы все 11 каталогов `skills/`. Каталог `packages/` (сборочные скрипты best-practices)
не импортируется: это инструмент сборки апстрима, а не скилл. У каждого скилла `LICENSE.txt` —
копия корневого Apache-2.0 апстрима (в апстриме лицензия одна на репозиторий), поэтому
отдельно установленный скилл приезжает вместе с лицензией.

## NousResearch/hermes-agent — импортировано

| Скилл | Файлов | КБ | Лицензия |
|---|---|---|---|
| `popular-web-designs` | 56 | 856 | MIT |

Импортирован один каталог (`skills/creative/popular-web-designs`), а не весь `skills/creative`:
соседние каталоги — те же скиллы Anthropic, они уже приезжают из своего апстрима, дубли не нужны.
Скрипт умеет режим «один каталог = один скилл»: если в каталоге манифеста есть `SKILL.md`, он
импортируется как один элемент.

**Атрибуция внутри элемента:** во frontmatter скилла прямо указано
`author: Hermes Agent + Teknium (design systems sourced from VoltAgent/awesome-design-md)` — сами
54 дизайн-системы пришли из [`VoltAgent/awesome-design-md`](https://github.com/VoltAgent/awesome-design-md)
(MIT). Скилл берём у того, кто сохранил атрибуцию, а не у переупаковщика без неё.

## obra/superpowers — импортировано

| Скилл | Файлов | КБ | Лицензия |
|---|---|---|---|
| `brainstorming` | 9 | 79 | MIT |
| `diagnosing-superpowers` | 21 | 42 | MIT |
| `dispatching-parallel-agents` | 2 | 7 | MIT |
| `executing-plans` | 4 | 22 | MIT |
| `finishing-a-development-branch` | 2 | 9 | MIT |
| `receiving-code-review` | 2 | 7 | MIT |
| `requesting-code-review` | 3 | 10 | MIT |
| `subagent-driven-development` | 16 | 65 | MIT |
| `systematic-debugging` | 7 | 29 | MIT |
| `test-driven-development` | 3 | 18 | MIT |
| `using-git-worktrees` | 2 | 8 | MIT |
| `using-superpowers` | 9 | 21 | MIT |
| `verification-before-completion` | 2 | 5 | MIT |
| `writing-plans` | 2 | 11 | MIT |
| `writing-skills` | 11 | 108 | MIT |

Импортирован весь каталог `skills/` — набор процесса разработки целиком (15 скиллов): брейншторм и
планы, TDD, системная отладка, работа через субагентов, ревью, закрытие ветки, проверка перед «готово».
Каталог — то, что агент подхватывает по описанию; вызовы агентов и хуки (`hooks/`, `scripts/`,
плагин-манифесты) не импортируются: это механика апстрима, а не скиллы.

## Отдельные скиллы (по одному апстриму)

| Апстрим | Скилл | Файлов | КБ | Лицензия |
|---|---|---|---|---|
| `Cocoon-AI/architecture-diagram-generator` (`architecture-diagram/`) | `architecture-diagram` | 3 | 26 | MIT, © 2025 Cocoon AI |
| `blader/humanizer` (корень репозитория) | `humanizer` | 7 | 62 | MIT, © 2025 Siqi Chen |
| `NousResearch/hermes-agent` (`optional-skills/creative/excalidraw`) | `excalidraw` | 6 | 30 | MIT, © 2025 Nous Research |

| `NousResearch/hermes-agent` (`skills/creative/claude-design`) | `claude-design` | 2 | 26 |
| `NousResearch/hermes-agent` (`optional-skills/creative/design-md`) | `design-md` | 3 | 12 |
| `NousResearch/hermes-agent` (`skills/creative/p5js`) | `p5js` | 18 | 163 |

Два режима импорта, которые они потребовали:
- **каталог = один скилл** (`architecture-diagram/`, `optional-skills/creative/excalidraw`): берётся только
  этот каталог, соседи по `skills/` не приезжают;
- **репозиторий целиком** (`skills_dir = .` у `humanizer`): копируется корень скилла, инфраструктура
  апстрима (`.github`, плагин-манифесты, `package.json`) не тащится. `humanizer` приносит свой `LICENSE`
  (© 2025 Siqi Chen) — он приоритетнее репозиторного и нормализуется в `LICENSE.txt`.

### Авторство скиллов из hermes-agent

`popular-web-designs`, `excalidraw` — собственные скиллы Hermes; `claude-design` и `p5js` опубликованы
Nous Research под MIT, но во frontmatter указаны авторы (`author: BadTechBandit`, `author: SHL0MS,
Hermes Agent`). Отдельных публичных репозиториев с этими скиллами нет — единственный публичный источник
под открытой лицензией — `hermes-agent`, поэтому импорт оттуда, а авторы остаются указанными в файле.
`design-md` — скилл Hermes про формат DESIGN.md от `google-labs-code/design.md` (Apache-2.0): сам формат
в репозитории Google, скилл-обёртка — MIT от Nous Research.

## Что исключено и почему

| Апстрим | Каталог | Причина |
|---|---|---|
| `anthropics/skills` | `doc-coauthoring` | **нет `LICENSE.txt`** (в апстриме файла нет, у репозитория нет корневой лицензии) — права на перераспространение не заявлены. Не публикуем и не переимпортируем, пока лицензия не появится |

## Лицензионный разбор (2026-11-10)

**anthropics/skills.** `LICENSE.txt` есть у 18 из 19 каталогов `skills/` и встречается в трёх
вариантах текста — все три являются **Apache License 2.0**, различаются только оформлением:

| Вариант | md5 | Где | Отличие |
|---|---|---|---|
| A | `0ee6429f…` | 15 скиллов | Apache-2.0, appendix с `Copyright 2026 Anthropic, PBC.` |
| B | `17579251…` | `docx`, `pdf`, `pptx`, `xlsx` | Apache-2.0, appendix с плейсхолдерами |
| C | `2ee41112…` | `frontend-design` | Apache-2.0 без appendix |

`diff` любого файла против канонического текста Apache-2.0 даёт только строку копирайта/appendix —
ограничительных дополнений (запрет на commercial use, source-available оговорок) нет.
Шрифты `canvas-design/canvas-fonts/*.ttf` сопровождаются `*-OFL.txt` (SIL OFL 1.1).

**ClickHouse/agent-skills.** Лицензия одна на репозиторий — **Apache-2.0** (корневой `LICENSE`,
`license.spdx_id = Apache-2.0` по API GitHub), отдельных `LICENSE.txt` в каталогах скиллов нет.
Корневой `NOTICE` содержит атрибуцию Vercel, Inc. (MIT) для `packages/clickhouse-best-practices-build/src/`
— этот каталог не импортируется, но NOTICE скопирован дословно целиком (`notices/clickhouse-agent-skills.md`),
чтобы атрибуция не терялась.

**NousResearch/hermes-agent.** Лицензия одна на репозиторий — **MIT** (`Copyright (c) 2025 Nous Research`),
скопирована в каталог скилла. Файла notices у апстрима нет; атрибуция датасета (VoltAgent, MIT)
прописана в frontmatter самого скилла и повторена в `NOTICE`.

**obra/superpowers.** Лицензия одна на репозиторий — **MIT** (`Copyright (c) 2025 Jesse Vincent`),
скопирована в каталог каждого скилла; файла notices нет.

**Cocoon-AI/architecture-diagram-generator, blader/humanizer.** MIT на репозиторий; у `humanizer`
лицензия лежит внутри самого скилла (`© 2025 Siqi Chen`) и она главнее — импорт её и сохраняет.

**Политика лицензий.** В каталог попадают только элементы под открытой лицензией (Apache-2.0, MIT,
BSD-2/3-Clause, ISC, MPL-2.0, OFL-1.1, CC0-1.0, CC-BY-4.0, Unlicense). Неизвестная или проприетарная
лицензия — не исключение «на усмотрение», а красный гейт: `scripts/check-catalog.py` распознаёт текст
лицензии по маркерам и падает на любом незнакомом.

Notices апстримов лежат в `notices/` дословно и перезаписываются скриптом при каждом
переимпорте; сводная атрибуция — `NOTICE`.

## Обновление пина

1. Правка строки в `upstreams.tsv` (repo, новый коммит, каталог, notices, исключения).
2. `scripts/sync-upstream.sh [repo]` — переимпорт; локальные правки импортированных каталогов
   при этом теряются (их и не должно быть).
3. `scripts/check-catalog.py` — гейт: SKILL.md/description/лицензия у каждого скилла, пины
   40-hex, README = факт.
4. Обновить таблицы в этом файле и строки в `README.md`, если состав изменился. В репозитории
   `msklv/demo-ai-lab` — ничего: ADR-0010 фиксирует механизм, состав каталога держится здесь.
