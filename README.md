# QA Automation: SauceDemo (UI) + Restful Booker (API)

[![Tests](https://github.com/zarhci/qa-automation/actions/workflows/test.yml/badge.svg)](https://github.com/zarhci/qa-automation/actions/workflows/test.yml)

Пет-проект по автоматизации тестирования на Python. Два тестируемых сервиса, один фреймворк:

- **UI**: интернет-магазин [SauceDemo](https://www.saucedemo.com): вход, корзина, оформление заказа (Selenium, паттерн Page Object).
- **API**: сервис бронирования [Restful Booker](https://restful-booker.herokuapp.com): авторизация, создание, получение, обновление и удаление брони (requests).

Всего **21 автотест** (14 API + 7 UI), ручная тестовая документация в Excel и CI на GitHub Actions с публикацией отчётов.

## Что посмотреть в первую очередь

| Что | Где |
|---|---|
| Онлайн-отчёты последнего прогона CI | https://zarhci.github.io/qa-automation/ |
| Код API-тестов | [`tests/api/`](tests/api) и HTTP-клиент [`api/booker_client.py`](api/booker_client.py) |
| Код UI-тестов и Page Object | [`tests/ui/`](tests/ui) и [`pages/`](pages) |
| Тестовая документация | [`docs/`](docs) (чек-листы, тест-кейсы, наборы, отчёт) |
| Конфигурация CI | [`.github/workflows/test.yml`](.github/workflows/test.yml) |

## Стек

- Python 3.12
- pytest 9, маркеры `smoke` / `critical_path` / `extended` / `regression`
- Selenium 4 (Chrome) + паттерн Page Object
- requests (API-клиент)
- pytest-html: HTML-отчёты, allure-pytest: сбор результатов Allure
- GitHub Actions + GitHub Pages
- Docker, Makefile

## Структура проекта

```
qa-automation/
├── .github/workflows/test.yml     # CI: smoke, API, UI regression, публикация отчётов
├── api/
│   └── booker_client.py           # BookerClient и booking_payload
├── pages/                         # Page Object для SauceDemo
│   ├── base_page.py               # явные ожидания, общие методы
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── api/
│   │   ├── conftest.py            # фикстуры client, token, booking, cleanup
│   │   ├── test_auth.py
│   │   ├── test_booking.py
│   │   └── test_booker_additional.py   # PUT и DELETE
│   └── ui/
│       ├── conftest.py            # фикстура driver (режим headless)
│       ├── test_login.py
│       ├── test_cart.py
│       └── test_checkout.py
├── docs/
│   ├── restful-booker/            # документация по API
│   └── saucedemo/                 # документация по UI
├── conftest.py                    # адрес UI-стенда (BASE_URL)
├── pytest.ini                     # маркеры и общие опции pytest
├── requirements.txt
├── Makefile
├── Dockerfile
└── .dockerignore
```

## Покрытие тестами

| Набор | API | UI | Всего | Что входит |
|---|---:|---:|---:|---|
| `smoke` | 2 | 3 | 5 | быстрая проверка главного: авторизация, создание брони, вход, корзина, оформление заказа |
| `critical_path` | 6 | — | 6 | основные позитивные сценарии API |
| `extended` | 6 | — | 6 | негативные и расширенные проверки API |
| `regression` | — | 4 | 4 | негативные проверки UI: ошибки входа и оформления заказа |
| **Всего** | **14** | **7** | **21** | |

Маркеры у API и UI разные: API размечен по типам проверок (`smoke`, `critical_path`, `extended`), UI по составу набора (`smoke`, `regression`).

### API: Restful Booker (14 проверок)

| ID | Эндпоинт и сценарий | Набор | Ожидаемый результат |
|---|---|---|---|
| API-TC-01 | `POST /auth`: доступность сервиса | Smoke | 200 |
| API-TC-02 | `POST /auth`: валидные данные, непустой токен | Critical Path | 200 + `token` |
| API-TC-03 | `POST /auth`: неверный пароль | Extended | 200 + `reason`, без `token` |
| API-TC-04 | `GET /booking`: список ID | Critical Path | 200, у первого элемента есть `bookingid` |
| API-TC-05 | `POST /booking`: минимальная бронь (без `additionalneeds`) | Smoke | 200 + `bookingid` |
| API-TC-06 | `POST /booking`: полный набор данных | Critical Path | 200, совпадают имя, фамилия, цена, `additionalneeds` |
| API-TC-07 | `POST /booking`: пустое тело | Extended | 500, бронь не создана |
| API-TC-08 | `POST /booking`: без `firstname` | Extended | 500, бронь не создана |
| API-TC-09 | `GET /booking/{id}`: существующая бронь | Critical Path | 200, совпадают имя и фамилия |
| API-TC-10 | `GET /booking/{id}`: несуществующий ID | Extended | 404 |
| API-TC-11 | `PUT /booking/{id}`: обновление с токеном | Critical Path | 200, в ответе новые имя, фамилия, цена |
| API-TC-12 | `PUT /booking/{id}`: обновление без токена | Extended | 403, бронь не изменилась |
| API-TC-13 | `DELETE /booking/{id}`: удаление с токеном | Critical Path | 201 `Created`, затем `GET` даёт 404 |
| API-TC-14 | `DELETE /booking/{id}`: удаление без токена | Extended | 403, бронь на месте |

### UI: SauceDemo (7 автотестов)

Каждый автотест соответствует ручному тест-кейсу из `docs/saucedemo/`:

| Ручной кейс | Автотест | Набор |
|---|---|---|
| ID.1 Успешный вход под `standard_user` | `test_login_with_valid_credentials` | smoke |
| ID.2 Добавление Sauce Labs Backpack в корзину | `test_add_backpack_to_cart` | smoke |
| ID.3 Оформление заказа до экрана Thank you | `test_checkout_completes_order` | smoke |
| ID.4–ID.6 Ошибки входа: `locked_out_user`, неверный пароль, пустой логин | `test_login_shows_error` (3 параметра) | regression |
| ID.7 Checkout без имени | `test_checkout_requires_first_name` | regression |

## Тестовая документация

Написана вручную в Excel, лежит в папке [`docs/`](docs).

**Restful Booker** (`docs/restful-booker/`)

| Файл | Содержимое |
|---|---|
| `RB_CheckList.xlsx` | Чек-лист на 14 проверок: тип, наименование, результат, статус автоматизации |
| `RB_test_cases.xlsx` | 14 тест-кейсов `API-TC-01…14` (предусловия, шаги, ожидаемый результат) и лист с тестовыми данными |
| `RB_test_suites.xlsx` | Тестовые наборы Smoke, Critical Path, Extended, Full с командами запуска |

**SauceDemo** (`docs/saucedemo/`)

| Файл | Содержимое |
|---|---|
| `Saucedemo_CheckList.xlsx` | Чек-лист на 7 проверок |
| `SauceDemo_Test_Cases_and_Suites.xlsx` | Тест-кейсы `ID.1–ID.7` и тестовый набор |
| `saucedemo_test_report.xlsx` | Отчёт о ручном прогоне: 7 из 7 Passed, дефектов нет |

## Запуск

### Что понадобится

- Python 3.12
- Google Chrome (для UI-тестов; драйвер Selenium подбирает сам)
- Интернет: тесты обращаются к публичным стендам

### Установка

```bash
git clone https://github.com/zarhci/qa-automation.git
cd qa-automation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Запуск тестов

```bash
pytest                       # все 21 тест
pytest tests/api             # только API (14)
pytest tests/ui              # только UI (7), с окном браузера
HEADLESS=true pytest tests/ui   # UI без окна браузера
pytest -m smoke              # smoke: API + UI (5)
pytest tests/api -m critical_path
pytest tests/api -m extended
pytest tests/ui -m regression
```

То же через Makefile:

```bash
make install       # установить зависимости
make smoke         # smoke-тесты
make api           # API-тесты
make ui            # UI-тесты
make ui-headless   # UI-тесты без окна браузера
make test          # все тесты
make report        # все тесты + HTML-отчёт docs/report.html
```

### Переменные окружения

| Переменная | По умолчанию | Назначение |
|---|---|---|
| `HEADLESS` | `false` | `true` запускает Chrome без окна (так тесты идут в CI) |
| `BASE_URL` | `https://www.saucedemo.com` | адрес UI-стенда |

### Docker

```bash
docker build -t qa-automation .
docker run --rm qa-automation
```

Контейнер запускает **API-тесты** (`pytest tests/api`). UI-тесты в образ не входят, так как требуют браузера: их запускают локально или в CI.

## CI: GitHub Actions

Workflow [`test.yml`](.github/workflows/test.yml) запускается на каждый push и pull request в `main`, а также вручную (кнопка **Run workflow** во вкладке Actions).

| Задача | Команда | Что даёт |
|---|---|---|
| Smoke (API + UI) | `pytest -m smoke` | быстрая проверка за один заход |
| Full (API) | `pytest tests/api` | все 14 API-тестов |
| Regression (UI) | `pytest tests/ui -m regression` | негативные UI-проверки в headless-режиме |
| Publish report | публикация на GitHub Pages | страница с отчётами; только для пушей в `main` |

Задачи идут параллельно, и каждая сохраняет свой HTML-отчёт, даже если тесты упали. Для pull request отчёты доступны как артефакты запуска, на Pages они не публикуются.

## Отчёты

- **Онлайн:** https://zarhci.github.io/qa-automation/ (страница со ссылками на отчёты Smoke, Full API и Regression UI; обновляется после каждого пуша в `main`).
- **Локально:** `make report` создаёт `docs/report.html`, это один файл без дополнительных зависимостей.
- **Allure (опционально):** при каждом запуске результаты записываются в `allure-results/`. Чтобы открыть отчёт, нужен установленный Allure CLI: `allure serve allure-results`.

## Особенности и принятые решения

**Restful Booker.** Тесты учитывают, как ведёт себя сервис:
- Токен для `PUT` и `DELETE` передаётся только через заголовок `Cookie: token=...`.
- Неверный пароль не даёт ошибку: сервис отвечает `200` с полем `reason`.
- Успешный `DELETE` возвращает `201 Created`.
- Пустое тело и отсутствие `firstname` приводят к `500`. Это текущее поведение сервиса, оно зафиксировано в тестах и в тест-кейсах как есть.
- Сервис общий для всех пользователей, поэтому тесты не опираются на чужие брони: каждый тест создаёт свою и удаляет её после себя (фикстуры `booking` и `cleanup`).

**UI.**
- Page Object: локаторы и действия живут в `pages/`, в тестах только сценарии.
- Только явные ожидания (`WebDriverWait`), неявные отключены (`implicitly_wait(0)`), `time.sleep` не используется.
- Проверки на странице идут перед проверкой URL, чтобы тест не зависел от скорости перехода.

При проектировании автотестов для пользовательского интерфейса (UI) были применены лучшие практики автоматизации, обеспечивающие высокую скорость выполнения и стабильность:

* **Архитектурный паттерн Page Object:** Локаторы элементов и низкоуровневые действия инкапсулированы внутри классов в директории `pages/`. В самих файлах тестов пишутся только чистые высокоуровневые бизнес-сценарии. Это позволяет легко поддерживать тесты: при изменении верстки сайта достаточно поправить локатор в одном месте.
* **Стратегия ожиданий (Explicit Waits):** В проекте полностью отключены неявные ожидания (`implicitly_wait(0)`) и категорически запрещены «жесткие» паузы (`time.sleep()`). Вместо них используются только явные ожидания (`WebDriverWait`). Тест ждет элемент ровно столько, сколько нужно системе для рендеринга, что ускоряет прохождение сьюта.
* **Оптимизация проверок при переходах:** Проверки состояния элементов на новой странице выполняются **строго до** проверки изменения текущего URL. Это гарантирует, что тест дождется асинхронной загрузки интерфейса и не упадет из-за того, что браузер физически не успел обновить адресную строку в момент клика.

### Почему API-тесты фиксируют текущее поведение, а не используют xfail

В продакшене известные баги обычно помечают `@pytest.mark.xfail` со ссылкой на тикет: разработчики исправляют дефект, и тест начинает проходить. В этом проекте выбран другой подход: текущее поведение сервиса («как есть») фиксируется прямо в проверках.

- Restful Booker — публичный учебный сервис без команды разработки: исправлений в рамках проекта ждать не от кого, поэтому у `xfail` нет смысла.
- Отчёты остаются читаемыми: проверки с ответом `500` (пустое тело и запрос без `firstname`, 2 из 14 API-тестов) не превращаются в постоянные «xfailed».
- Тесты работают как контроль регрессии: если поведение сервиса изменится, соответствующий тест упадёт.

Это же отражено в тест-кейсах `API-TC-07` и `API-TC-08`: «текущее поведение сервиса; ожидаемый статус уточнить по REQ1».

Таким образом, тесты проверяют реальное, фактически задокументированное в рамках этого проекта поведение системы, а не идеальный REST API.

## Автор

Р. А. Чибиев, [@zarhci](https://github.com/zarhci)
