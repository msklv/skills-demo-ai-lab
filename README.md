# skills-demo-ai-lab — каталог агентских скиллов стенда demo-ai-lab

Публичный git-репозиторий скиллов в формате **SKILL.md** (Agent Skills): набор инструкций и
ассетов, который агент (Hermes, Claude Code, Codex, любой другой клиент этого формата) читает
по требованию — когда задача совпала с `description` скилла.

Каталог = дерево каталогов. Ни сервера, ни БД, ни рендерера: ставится клонированием или
копированием каталога. Решение и его обоснование — ADR-0010 в репозитории `msklv/demo-ai-lab`
(`adr/adr-0010-skills-collection-git-repo.md`).

## Структура

```
skills-demo-ai-lab/
├── skills/<имя-скилла>/       # один каталог = один скилл (SKILL.md + ассеты + его LICENSE.txt)
├── upstreams.tsv              # апстримы (3): repo, пин-коммит, каталог скиллов, notices, исключения
├── scripts/sync-upstream.sh   # переимпорт всех апстримов по пинам
├── scripts/check-catalog.py   # гейт: SKILL.md/description/лицензия, README = факт, пины валидны
├── UPSTREAM.md                # что, откуда и на каком коммите импортировано; что исключено
├── NOTICE                     # атрибуция апстримов (© Anthropic PBC, © ClickHouse Inc.), шрифты
├── notices/                   # дословные notices апстримов (THIRD_PARTY_NOTICES, NOTICE)
└── LICENSE                    # Apache-2.0 (обвязка репозитория)
```

Правила: скилл живёт **одним каталогом** (`skills/<name>/SKILL.md`, frontmatter `name` +
`description` обязателен); имя каталога = `name`; у каждого импортированного скилла лежит
`LICENSE.txt` дословно из апстрима (если у апстрима лицензия одна на репозиторий — она
копируется в каталог скилла: установленный отдельно скилл должен приезжать вместе с лицензией);
ассеты — внутри каталога скилла, никаких общих папок, иначе установка одного скилла тянет чужие
файлы.

## Каталог

60 скиллов из трёх апстримов, все — под открытыми лицензиями: **Apache-2.0** (© Anthropic PBC,
© ClickHouse, Inc.) и **MIT** (© QM contributors). Скиллов с неоткрытой лицензией в каталоге нет —
это проверяет гейт (`scripts/check-catalog.py`, белый список лицензий).

| Скилл | Что делает | Категория | Источник |
|---|---|---|---|
| [academy-guide](skills/academy-guide/) | перед ответом про использование Claude и продуктов — сверка с официальными курсами/докой, предложение обучения | обучение | anthropics |
| [admin](skills/admin/) | админ-API платформы: каталог скоупов, конфиг и SOUL, память, транскрипты, роли, аудит | платформа | qm |
| [algorithmic-art](skills/algorithmic-art/) | генеративное искусство на p5.js: seeded-случайность, интерактивные параметры | визуал | anthropics |
| [brand-guidelines](skills/brand-guidelines/) | фирменные цвета и типографика Anthropic для артефактов | визуал | anthropics |
| [browse](skills/browse/) | управление настоящим stealth-браузером из шелла: действия на сайтах, персональные сохранённые входы | браузер | qm |
| [canvas-design](skills/canvas-design/) | постеры и визуальный дизайн в `.png`/`.pdf`; 40+ шрифтов (OFL) внутри каталога | визуал | anthropics |
| [chdb-datastore](skills/chdb-datastore/) | табличные данные (pandas, parquet, csv, Arrow, json): фильтры, агрегаты, join, ускорение медленного pandas | данные | clickhouse |
| [chdb-sql](skills/chdb-sql/) | аналитический SQL по локальным файлам, URL, S3-путям и внешним БД (Postgres, MySQL) через chDB | данные | clickhouse |
| [claude-api](skills/claude-api/) | справочник по Claude API/SDK: модели, цены, стриминг, tool use, кэш, MCP, миграции моделей | инженерия | anthropics |
| [clickhouse-architecture-advisor](skills/clickhouse-architecture-advisor/) | проектирование архитектуры ClickHouse: схемы ingestion, моделирование, сопоставление best practices с нагрузкой | данные | clickhouse |
| [clickhouse-best-practices](skills/clickhouse-best-practices/) | 31 правило проверки схем, запросов и конфигураций ClickHouse перед выдачей рекомендаций | данные | clickhouse |
| [clickhouse-js-node-coding](skills/clickhouse-js-node-coding/) | идиоматичный код на Node.js-клиенте `@clickhouse/client` | данные | clickhouse |
| [clickhouse-js-node-rowbinary](skills/clickhouse-js-node-rowbinary/) | RowBinary: чтение/запись потоков для всех типов ClickHouse HTTP | данные | clickhouse |
| [clickhouse-js-node-troubleshooting](skills/clickhouse-js-node-troubleshooting/) | разбор ошибок Node.js-клиента: TLS, компрессия, параметры запроса, socket hangup, format clause | данные | clickhouse |
| [clickhouse-managed-postgres-rca](skills/clickhouse-managed-postgres-rca/) | RCA производительности ClickHouse-managed Postgres: сбор доказательств через Prometheus/логи | данные | clickhouse |
| [clickstack-otel-collector](skills/clickstack-otel-collector/) | подключение OpenTelemetry-коллектора к Managed ClickStack в ClickHouse Cloud | наблюдаемость | clickhouse |
| [cloud-cli](skills/cloud-cli/) | вход в CLI облачного провайдера (AWS/GCP/Azure) device-code потоком и запуск команд от лица владельца | доступ | qm |
| [composio](skills/composio/) | выбор и подключение SaaS-приложений через бэкенд Composio (consent, каталог приложений) | интеграции | qm |
| [connect-apps](skills/connect-apps/) | подключение Slack и админ-включённых SaaS одной OAuth-ссылкой | интеграции | qm |
| [define-loop](skills/define-loop/) | Loop: долговременный контур с очередью повторяющихся задач, cron, памятью и гейтом ревью | платформа | qm |
| [discernment-nudge](skills/discernment-nudge/) | пауза перед «уверенным» советом: проверка допущений и границ применимости | качество | anthropics |
| [docx](skills/docx/) | Word: создание, чтение, правка, отслеживаемые изменения, OOXML-схемы | документы | anthropics |
| [dropbox](skills/dropbox/) | Dropbox: просмотр, поиск, чтение, загрузка, шаринг — включая командные папки | интеграции | qm |
| [email-draft-in-voice](skills/email-draft-in-voice/) | черновики писем в голосе владельца из профиля голоса (только черновики, отправляет человек) | коммуникации | qm |
| [email-voice-profile](skills/email-voice-profile/) | профиль того, как владелец пишет письма, по его отправленным — вход для черновиков в своём голосе | коммуникации | qm |
| [frontend-design](skills/frontend-design/) | дизайн-гайд для нового UI и переделки существующего | визуал | anthropics |
| [github-gitlab](skills/github-gitlab/) | работа с GitHub/GitLab через резидентные `gh`/`glab`/git-авторизацию на машине агента | инженерия | qm |
| [google-drive-sheets](skills/google-drive-sheets/) | Google Drive/Docs/Sheets/Slides: поиск, чтение, экспорт, правка | интеграции | qm |
| [google-workspace](skills/google-workspace/) | Gmail, Google Calendar и Tasks через персональное подключение | интеграции | qm |
| [hand-off](skills/hand-off/) | передать работу, которой нужны чужие логины/файлы/память: решить, делать самому или просить человека | платформа | qm |
| [infra-clickhouse](skills/infra-clickhouse/) | ClickHouse через CLI `clickhousectl`: локальный сервер для разработки, managed-кластеры, доступы | инфраструктура | clickhouse |
| [infra-postgres](skills/infra-postgres/) | Postgres через CLI `clickhousectl`: локальный Docker-инстанс, managed Postgres, доступы и правила | инфраструктура | clickhouse |
| [interactive-login](skills/interactive-login/) | вход в CLI браузерным/device-code потоком (`aws sso`, `gh`, `glab`, `gcloud`) с сохранением в keychain | доступ | qm |
| [internal-comms](skills/internal-comms/) | внутренние коммуникации в форматах компании (апдейты, статусы, разборы) | коммуникации | anthropics |
| [linear](skills/linear/) | Linear: поиск, чтение, создание и обновление issues, проектов, комментариев | интеграции | qm |
| [mcp-builder](skills/mcp-builder/) | как писать качественные MCP-серверы (Python/TypeScript), чек-лист ревью | инженерия | anthropics |
| [memory](skills/memory/) | осознанная работа с долговременной памятью: поиск, добавление, курирование через инструмент памяти | платформа | qm |
| [miniapp](skills/miniapp/) | крошечный self-contained HTML-плейграунд, когда просят показать или «покрутить» механизм | визуал | qm |
| [morning-digest](skills/morning-digest/) | утренний дайджест по подключённым источникам: что изменилось за ночь и что это значит для дня | коммуникации | qm |
| [onboarding](skills/onboarding/) | онбординг нового пользователя: подключение аккаунтов, знакомство с реальной работой, голос, первые задачи | платформа | qm |
| [pdf](skills/pdf/) | всё про PDF: извлечение текста, формы, слияние/разделение, OCR | документы | anthropics |
| [persona-fork](skills/persona-fork/) | форк персоны: копия инструкций, иконки и набора скиллов в новую персону со своими кредами | платформа | qm |
| [popular-web-designs](skills/popular-web-designs/) | 54 реальные дизайн-системы (Stripe, Linear, Vercel, Notion, Apple…) как готовый HTML/CSS | визуал | qm |
| [pptx](skills/pptx/) | PowerPoint: создание, правка, шаблоны, форматирование | документы | anthropics |
| [publish](skills/publish/) | публикация долгоживущего внутреннего веб-приложения/дашборда: версии, доступ по скоупу | платформа | qm |
| [request-access](skills/request-access/) | запрос доступа к чужому хранимому кредалу с карточкой одобрения в диалоге | доступ | qm |
| [secret-drop](skills/secret-drop/) | запрос кредала одноразовой ссылкой вместо пересылки секрета в чате | доступ | qm |
| [send](skills/send/) | PR → ожидание CI с ретраями → обязательные ревью → merge только при зелёных гейтах | инженерия | qm |
| [skill-creator](skills/skill-creator/) | создание и улучшение скиллов, оценка их качества, eval-viewer | инженерия | anthropics |
| [slack-drafts](skills/slack-drafts/) | черновики сообщений Slack от лица владельца через его OAuth (только черновики) | коммуникации | qm |
| [slack-gif-creator](skills/slack-gif-creator/) | анимированные GIF под лимиты Slack (imageio/ffmpeg) | визуал | anthropics |
| [taste-skill](skills/taste-skill/) | дизайн-вкус и процесс для всего, что смотрят в браузере: лендинг, дашборд, прототип, дек | визуал | qm |
| [theme-factory](skills/theme-factory/) | темы оформления артефактов: слайды, доки, отчёты, HTML-страницы | визуал | anthropics |
| [ui-canvas](skills/ui-canvas/) | собственный HTML/CSS/JS оверлеем поверх веб-UI: дашборд, форма, визуализация, контролы | визуал | qm |
| [ui-state](skills/ui-state/) | снимок текущего состояния веб-UI: разметка страницы, JSON состояния, CSS/скриншот | платформа | qm |
| [use-shared-credential](skills/use-shared-credential/) | вызов сервиса общим (org) кредалом через прокси платформы | доступ | qm |
| [web-artifacts-builder](skills/web-artifacts-builder/) | многокомпонентные HTML-артефакты на современном фронтенд-стеке | визуал | anthropics |
| [webapp-testing](skills/webapp-testing/) | Playwright-проверка локальных веб-приложений: сценарии, скриншоты, консоль | инженерия | anthropics |
| [xlsx](skills/xlsx/) | Excel: создание, правка, формулы, форматирование, большие таблицы | документы | anthropics |
| [zoom](skills/zoom/) | Zoom: поиск, создание, перенос и отмена встреч владельца | интеграции | qm |

Исключён осознанно: `doc-coauthoring` (`anthropics/skills`) — у него в апстриме **нет файла
лицензии**, права на распространение не заявлены. Остальные каталоги апстримов идут под
Apache-2.0 и MIT (разбор по каждому — `UPSTREAM.md`).

В каталог попадают **только публичные апстримы целиком** — никаких локальных адаптаций: если скилл
правится под конкретный контур (адреса, внутренние интеграции, зеркала), это отдельный приватный
каталог, а не строка здесь.

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

## Обновление из апстримов

Апстримы перечислены в `upstreams.tsv` (repo, пин-коммит, каталог скиллов, файл notices,
исключения) — пин по коммиту, не по ветке: переимпорт должен быть воспроизводимым.

```bash
scripts/sync-upstream.sh                        # все апстримы по пинам
scripts/sync-upstream.sh ClickHouse/agent-skills # один апстрим
UPSTREAM_REF=<sha> scripts/sync-upstream.sh anthropics/skills  # пробный ref
scripts/check-catalog.py                        # гейт каталога (перед коммитом)
```

Импорт — копирование каталогов без правок содержимого: любые локальные изменения в
`skills/<name>/` затрудняют следующий re-import, поэтому свои скиллы живут **отдельными**
каталогами, а не правками импортированных. Новый апстрим = строка в `upstreams.tsv` + прогон
скрипта + таблицы в `UPSTREAM.md`/`NOTICE`.

## Свои скиллы

1. `skills/<name>/SKILL.md` — frontmatter `name`, `description` (одна строка, «когда применять»),
   тело — процедура.
2. Лицензия: для собственных скиллов — `LICENSE.txt` в каталоге (по умолчанию Apache-2.0).
3. Строка в таблице «Каталог» этого README (гейт `check-catalog.py` сверяет таблицу с фактом).
4. Приватных данных в скиллах нет: каталог публичный — ни паролей, ни токенов, ни внутренних
   адресов, ни персональных данных; те же правила, что в `msklv/demo-ai-lab` (AGENTS.md).

## Лицензии

- Импортированные скиллы: **Apache-2.0** — © Anthropic PBC (`anthropics/skills`),
  © ClickHouse, Inc. (`ClickHouse/agent-skills`); **MIT** — © QM contributors (`yc-software/qm`).
  Текст лицензии лежит внутри каждого каталога (`skills/<name>/LICENSE.txt`) дословно; сводная
  атрибуция — `NOTICE`.
- Шрифты в `skills/canvas-design/canvas-fonts/` — **SIL OFL 1.1**, текст рядом (`*-OFL.txt`).
- Сторонние компоненты, которые тянут скиллы (imageio, FFmpeg; Vercel MIT — в `ClickHouse/agent-skills`) —
  дословные notices апстримов в `notices/`.
- Обвязка репозитория (README, скрипты, каталог) — Apache-2.0 (`LICENSE`).
- **Политика:** в каталоге только открытые лицензии (Apache-2.0, MIT, BSD-2/3, ISC, MPL-2.0, OFL-1.1,
  CC0-1.0, CC-BY-4.0, Unlicense). Неизвестная или проприетарная лицензия = гейт красный, элемент
  не публикуется.
