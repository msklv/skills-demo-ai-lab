# skills-demo-ai-lab — каталог агентских скиллов стенда demo-ai-lab

Публичный git-репозиторий скиллов в формате **SKILL.md** (Agent Skills): набор инструкций и
ассетов, который агент (Hermes, Claude Code, Codex, любой другой клиент этого формата) читает
по требованию — когда задача совпала с `description` скилла.

Каталог = дерево каталогов. Ни сервера, ни БД, ни рендерера: ставится клонированием или
копированием каталога. Решение и его обоснование — `adr/adr-0010-skills-collection-git-repo.md`
в репозитории `msklv/demo-ai-lab`.

## Структура

```
skills-demo-ai-lab/
├── skills/<имя-скилла>/       # один каталог = один скилл (SKILL.md + ассеты + его LICENSE.txt)
├── scripts/sync-upstream.sh   # заново импортировать апстрим по пину (UPSTREAM.md)
├── scripts/check-catalog.py   # гейт: SKILL.md/description/LICENSE на месте, README = факт
├── UPSTREAM.md                # что, откуда и на каком коммите импортировано; что исключено
├── NOTICE                     # атрибуция © Anthropic PBC (Apache-2.0) и шрифтов (OFL)
├── THIRD_PARTY_NOTICES.md     # дословно из апстрима: imageio, FFmpeg и пр.
└── LICENSE                    # Apache-2.0 (обвязка репозитория)
```

Правила: скилл живёт **одним каталогом** (`skills/<name>/SKILL.md`, frontmatter `name` +
`description` обязателен); имя каталога = `name`; у каждого импортированного скилла сохраняется
его собственный `LICENSE.txt` дословно; ассеты — внутри каталога скилла (никаких общих папок,
иначе установка одного скилла тянет чужие файлы).

## Каталог

18 скиллов, все — **Apache-2.0** (© Anthropic PBC), кроме собственных добавлений репозитория.

| Скилл | Что делает | Категория |
|---|---|---|
| [academy-guide](skills/academy-guide/) | перед ответом про использование Claude и продуктов — сверка с официальными курсами/докой, предложение обучения | обучение |
| [algorithmic-art](skills/algorithmic-art/) | генеративное искусство на p5.js: seeded-случайность, интерактивные параметры | визуал |
| [brand-guidelines](skills/brand-guidelines/) | фирменные цвета и типографика Anthropic для артефактов | визуал |
| [canvas-design](skills/canvas-design/) | постеры и визуальный дизайн в `.png`/`.pdf`; 40+ шрифтов (OFL) внутри каталога | визуал |
| [claude-api](skills/claude-api/) | справочник по Claude API/SDK: модели, цены, стриминг, tool use, кэш, MCP, миграции моделей | инженерия |
| [discernment-nudge](skills/discernment-nudge/) | пауза перед «уверенным» советом: проверка допущений и границ применимости | качество |
| [docx](skills/docx/) | Word: создание, чтение, правка, отслеживаемые изменения, OOXML-схемы | документы |
| [frontend-design](skills/frontend-design/) | дизайн-гайд для нового UI и переделки существующего | визуал |
| [internal-comms](skills/internal-comms/) | внутренние коммуникации в форматах компании (апдейты, статусы, разборы) | коммуникации |
| [mcp-builder](skills/mcp-builder/) | как писать качественные MCP-серверы (Python/TypeScript), чек-лист ревью | инженерия |
| [pdf](skills/pdf/) | всё про PDF: извлечение текста, формы, слияние/разделение, OCR | документы |
| [pptx](skills/pptx/) | PowerPoint: создание, правка, шаблоны, форматирование | документы |
| [skill-creator](skills/skill-creator/) | создание и улучшение скиллов, оценка их качества, eval-viewer | инженерия |
| [slack-gif-creator](skills/slack-gif-creator/) | анимированные GIF под лимиты Slack (imageio/ffmpeg) | визуал |
| [theme-factory](skills/theme-factory/) | темы оформления артефактов: слайды, доки, отчёты, HTML-страницы | визуал |
| [web-artifacts-builder](skills/web-artifacts-builder/) | многокомпонентные HTML-артефакты на современном фронтенд-стеке | визуал |
| [webapp-testing](skills/webapp-testing/) | Playwright-проверка локальных веб-приложений: сценарии, скриншоты, консоль | инженерия |
| [xlsx](skills/xlsx/) | Excel: создание, правка, формулы, форматирование, большие таблицы | документы |

Исключён осознанно: `doc-coauthoring` — в апстриме у него **нет `LICENSE.txt`**, права на
распространение не заявлены; остальные 18 каталогов апстрима — Apache-2.0 (разбор — `UPSTREAM.md`).

## Как поставить скилл в агента

**Hermes** (каталог скиллов профиля, `$HERMES_HOME/skills/`):

```bash
git clone https://github.com/msklv/skills-demo-ai-lab.git ~/git/skills-demo-ai-lab
cp -R ~/git/skills-demo-ai-lab/skills/docx "$HOME/.hermes/skills/"
hermes skills list | grep -i docx        # скилл виден агенту
```

**Claude Code / прочие клиенты формата SKILL.md**: скопировать `skills/<name>/` в свой каталог
скиллов (`.claude/skills/`, `~/.agents/skills/` и т.п.) — формат переносится как есть, конверсии нет.

Обновление: `git pull`. Скилл — инструкция и скрипты, которые агент запускает **у себя**:
репозиторий ничего не исполняет и не вызывает.

## Обновление из апстрима

Источник — `https://github.com/anthropics/skills`, пин по коммиту (см. `UPSTREAM.md`).

```bash
scripts/sync-upstream.sh                 # переимпорт по пину из UPSTREAM.md
scripts/sync-upstream.sh <commit-sha>    # новый пин: импорт + правка UPSTREAM.md вручную
scripts/check-catalog.py                 # гейт каталога (перед коммитом)
```

Импорт — копирование каталогов без правок содержимого: любые локальные изменения в
`skills/<name>/` затрудняют следующий re-import, поэтому свои скиллы живут **отдельными**
каталогами, а не правками импортированных.

## Свои скиллы

1. `skills/<name>/SKILL.md` — frontmatter `name`, `description` (одна строка, «когда применять»),
   тело — процедура.
2. Лицензия: для собственных скиллов — `LICENSE.txt` в каталоге (по умолчанию Apache-2.0).
3. Строка в таблице «Каталог» этого README (гейт `check-catalog.py` сверяет таблицу с фактом).
4. Приватных данных в скиллах нет: каталог публичный — ни паролей, ни токенов, ни внутренних
   адресов, ни персональных данных; те же правила, что в `msklv/demo-ai-lab` (AGENTS.md).

## Лицензии

- Импортированные скиллы — **Apache-2.0**, © Anthropic PBC: текст лицензии лежит внутри
  каждого каталога (`skills/<name>/LICENSE.txt`) дословно; сводная атрибуция — `NOTICE`.
- Шрифты в `skills/canvas-design/canvas-fonts/` — **SIL OFL 1.1**, текст рядом (`*-OFL.txt`).
- Сторонние runtime-зависимости, которые тянут скиллы (imageio, FFmpeg) — `THIRD_PARTY_NOTICES.md`.
- Обвязка репозитория (README, скрипты, каталог) — Apache-2.0 (`LICENSE`).
