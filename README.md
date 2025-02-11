# BIM Projects APP

## О проекте
Проект предназначен для управления и анализа BIM Проектов.

**Цели:** 
Основные функции:

- **Создание BIM проектов**
- **Админка для суперпользователя и BIM Специалистов для управления BIM проектами**
- **Задачи: Архивация, бэкап, и отправка Revit/Navis/IFC моделей заказчику в виде задач в фоновом режиме, если происходит какая либо выгрузка для одного проекта, необходимо блокировать другие задачи для этого проекта**
- **Фронт для остальных пользователей предоставляющий доступ к информации об информационной наполненности всех моделей/Графики/Время выгрузки, Количество моделей и их пути на сервере, возможность сформировать архив со всеми моделями проекта, а так же выгрузить модели в формат navisworks.**

## [DataModel](https://miro.com/welcomeonboard/MmljVWx2NGNMakNDelpQSXZ0ZVBvTmtJejJlYXBLb2dDQ0dMdTAyYi9jUUZNTkRBWExsUHBtdllKY1IvcnN6SnVDNVVVRy9BTUtmUEliRmN5ZmVSa2I0RTZTMU1ldk41amlCRFVzc3JkRnR0NW5nS0tBZjRVQVVGMkF6RGxlMXlBd044SHFHaVlWYWk0d3NxeHNmeG9BPT0hdjE=?share_link_id=161117476898)

## Стек :)
- Python 3.11.2
- FastAPI
- rpws
- Выбрать Брокера сообщенй
- PostgreSQL

## Настройка

### Репозиторий
- Базовая рабочая ветка - develop. Здесь располагается "чистый" основной рабочий код после ревью. Все остальные ветки создаем только от нее
**Все объединения проводятся исключительно через Pull requests**
- ‼️ Ветка `master` - ветка для чистого кода, подготовленного к деплою на сервер.
- Правила именования веток:
  - `feature/<краткое описание>` - для веток, реализующих основной и дополнительный функционал ТЗ
  - `fix/<краткое описание>` - для веток, исправляющих или дополняющие уже реализованный функционал


### Настройка после клонирования репозитория

После клонирования репозиторий имеет следующую структуру:

```
bim_projects_app
│
├── docker/     # Каталог с файлами инфраструктуры
│   ├── env.example     # Пример конфигурационного файла
│   ├── dev-docker-compose.yml      # Настройки для docker compose
│   └── Dockerfile      # Настройки для Docker
│
├── src/      # Базовый каталог проекта
│   ├── api.py      # Глобавльные роуты API
│   ├── config.py     # Глобавльный конфиг проекта
│   ├── constants.py      # Глобальные константы
│   ├── exceptions.py      # Глобальные ошибки
│   ├── logging.py      # Конфиг логгирования
│   ├── main.py       # Точка входа в приложение FastAPI
│   ├── repository.py      # Глобальный репозиторий для управления 
│   ├── rpws_.py      # Конфигурация для библиотеки rpws для поиска моделей на RevitServer
│   ├── __init__.py
│   │
│   ├───admin/      # Админка
│   │   ├── models.py     # Модели бд
│   │   ├── schemas.py      # Pydantic cхемы
│   │   ├── views.py      # Вьюхи
│   │   └── __init__.py
│   │
│   ├───auth/       # Аунтефикация
│   │   ├──models.py
│   │   ├──views.py
│   │   └──__init__.py
│   │
│   ├───database/       # База данных
│   │   ├── core.py       # Конфигурация базы данных
│   │   └── __init__.py
│   │
│   ├───project/       # BIM Проект
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── schemas.py
│   │   ├── views.py
│   │   └── __init__.py
│   │
│   ├───task/       # Задачи
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── schemas.py
│   │   ├── views.py
│   │   └── __init__.py
│   │
│   └───users/       # Пользователи
│       ├── core.py
│       ├── models.py
│       ├── schemas.py
│       ├── utils.py      # Вспомогательный пакет
│       ├── views.py
│       └── __init__.py
│   
├── tests/                              Тестирование
|   └── conftest.py                     Тестовые компоненты
│
├── .gitignore                          Что игнорировать в Git
├── requirements.txt                    Основные зависимости проекта
├── requirements_style.txt              Зависимости для стилизации кода
├── .pre-commit-config.yaml             Настройки для проверок перед комитом
├── style.cfg                           Настройки для isort и flake8
├── black.cfg                           Настройки для black
└── README.md                           Этот файл
```

**Устанавливаем и активируем виртуальное окружение**

```shell
python3.11 -m venv .venv
source .venv/bin/activate
```

Устанавливаем зависимости
```shell
pip install -r requirements.txt
pip install -r requirements_style.txt
```

Настраиваем `pre-commit`

```shell
pre-commit install
```

Проверяем, что `pre-commit` работает корректно

```shell
pre-commit run --all-files
```

Возможно потребуется запуск несколько раз. В итоге должен получиться примерно такой вывод:

```shell
trim trailing whitespace............Passed
fix end of files....................Passed
check yaml..........................Passed
check for added large files.........Passed
check for merge conflicts...........Passed
isort...............................Passed
flake8..............................Passed
black...............................Passed
```
#Запуск проекта
Пример .env
POSTGRES_USER=your_db_username # Заменить
POSTGRES_PASSWORD=your_db_password # Заменить
POSTGRES_DB=bim_projects_app
POSTGRES_SERVER=localhost # Изменить на название контейнера с БД в Docker Compose
POSTGRES_PORT=5432
```
Добавить папку src в рабочую директорию
```
```
Перейти в папку src
```
cd src
```
Запустить проект через терминал командой
```
python main.py
```
Для развертывания проетка локально на своем пк перейдите в папку infra
```
cd ..
cd infra
```
Запустите docker compose
```
docker compose up
```
Для развертывания на сервере необходимо запушить изменеия в ветку main и он автоматически развернется
