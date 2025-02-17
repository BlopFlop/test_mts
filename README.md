# test_mts

## О проекте
API на FastAPI с возможностью загрузки данных в excel

## [Структура бд и запросы](https://miro.com/welcomeonboard/MmljVWx2NGNMakNDelpQSXZ0ZVBvTmtJejJlYXBLb2dDQ0dMdTAyYi9jUUZNTkRBWExsUHBtdllKY1IvcnN6SnVDNVVVRy9BTUtmUEliRmN5ZmVSa2I0RTZTMU1ldk41amlCRFVzc3JkRnVjUGowbWJCMGd5K2puSEhybG5NZ0tzVXVvMm53MW9OWFg5bkJoVXZxdFhRPT0hdjE=?share_link_id=957773900600)
- Выбрал таку архитектуру потому что считаю что она достаточно универсальна, и подходит под любую структуру компани.
- 2) Вывод списка сотрудников получающих зп больше чем у руководителя
```
SELECT *
FROM employee AS E1
WHERE salary > (
  SELECT salary 
  FROM employee AS E2 
  WHERE E2.id = E1.manager_id
  LIMIT 1) 
AND E1.is_staff

SELECT *
FROM employee AS E1
WHERE salary > (
  SELECT salary 
  FROM employee AS E2 
  WHERE E2.id = E1.manager_id
  LIMIT 1) 
AND ((
	E1.termination_date IS null OR E1.termination_date > '2024-07-01') 
	AND E1.hire_date < '2024-07-01'
)
```
- 3) Вывод списка сотрудников получающих максимальную зп в своем отделе
```
SELECT *
FROM employee AS E1
JOIN (
    SELECT
        division_id,
        MAX(E2.salary) AS max_salary
    FROM employee AS E2
    GROUP BY
        division_id
) dept_max ON E1.division_id = dept_max.division_id
    AND E1.salary = dept_max.max_salary
WHERE E1.is_staff;

SELECT *
FROM employee AS E1
JOIN (
    SELECT
        division_id,
        MAX(E2.salary) AS max_salary
    FROM employee AS E2
    GROUP BY
        division_id
) dept_max ON E1.division_id = dept_max.division_id
    AND E1.salary = dept_max.max_salary
WHERE (E1.termination_date IS null OR E1.termination_date > '2024-07-01')
	AND E1.hire_date < '2024-07-01';
```
- 4) Вывод списка отделов количеством штатных сотрудников
```
SELECT division.name, (
	SELECT COUNT(*)
	FROM employee
	WHERE employee.division_id = division.id
	AND employee.is_staff
)
FROM division

SELECT division.name, (
	SELECT COUNT(*)
	FROM employee
	WHERE employee.division_id = division.id
	AND (employee.termination_date IS null OR employee.termination_date > '2024-07-01')
	AND employee.hire_date < '2024-07-01')
FROM division
```
- 5) Вывод списка отделов с максимальной суммарной зп у сотрудников
```
SELECT division.name, (
	SELECT SUM(employee.salary)
	FROM employee
	WHERE employee.division_id = division.id
	AND employee.is_staff
)
FROM division

SELECT division.name, (
	SELECT SUM(employee.salary)
	FROM employee
	WHERE employee.division_id = division.id
	AND (employee.termination_date IS null OR employee.termination_date > '2024-07-01')
	AND employee.hire_date < '2024-07-01')
FROM division
```

**Цели:** 
Основные функции:

- **Получение данных о товаре по артиклю с помощью API**
- **Добавление товара по артикулу в задачу с постоянным обновлением этого товара через каждые 30 минут**

**Эндпоитны:**
- GET docs - Документация API.
 
## Стек
- Python 3.11.2
- FastAPI
- Aiogram
- PostgreSQL

## Настройка

### Настройка после клонирования репозитория

После клонирования репозиторий имеет следующую структуру:

```
test_mts
│
├── infta/     # Каталог с файлами инфраструктуры
│   ├── env.example     # Пример конфигурационного файла
│   ├── dev-docker-compose.yml      # Настройки для docker compose
│   └── Dockerfile      # Настройки для Docker
│
├───src/
│   ├───company/     # Сущности компании
│   │   ├───endpoints # Энпоинты
│   │   ├───repository # Репозитории
│   │   ├───schemas # Схемы
│   │   ├── routers.py # Роутеры
│   │   ├── models.py # Модели
│   │   ├── validators.py # Валидаторы
│   │   └── __init__.py
│   │
│   ├───database/ # работа с бд
│   │   ├───alembic/     # Миграции для основной бд
│   │   ├───alembic_test/    # Миграции для тестовой бд
│   │   ├── core.py      # Настройка бд
│   │   └── __init__.py
│   │
│   ├───loader/ # загрузчик данных из excel
│   │   ├── constants.py      # константы для файла
│   │   ├── utils.py      # логика
│   │   └── __init__.py
│   │
│   ├── alembic.ini     # Скрипт миграций
│   ├── alembic_test.ini     # Скрипт миграций для тестовой бд
│   ├── api.py     # Базовый файл api
│   ├── main.py     # Точка входа в приложение
│   ├── manage.py     # Мэнеджмент команды
│   ├── logging_.py     # Конфиг логгирования
│   ├── repository.py     # Базовый репо
│   ├── schemas.py     # Схемы
│
├── tests/      # Тестирование
|   │   conftest.py     # Тестовые компоненты
│   └───fixtures/      # Фикстуры
│
│   pytest.ini       # настройки pytest
└── README.md       # Этот файл
```
**Устанавливаем и активируем виртуальное окружение**
```
Добавить папку src в рабочую директорию
```
```
Перейти в папку src
```
cd src
```
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
```
#  application
NAME_APP="Test application"

#  database
DB="habrdb"
DB_USER="postgress"  # Заменить
DB_PASSWORD="test"  # Заменить
DB_SERVER="localhost" # Изменить на название контейнера с БД в Docker Compose
DB_PORT="5434"

#  test database
TEST_DB="testdb"
TEST_DB_USER="postgress"  # Заменить
TEST_DB_PASSWORD="test"  # Заменить
TEST_DB_SERVER="localhost"  # Изменить на название контейнера развернутой тестовой бд
TEST_DB_PORT="5435"

```
Применить миграции
```
alembic upgrade head
```
Запустить проект через терминал командой
```
python main.py
```
Для развертывания проектка в докере перейдите в папку infra
```
cd ..
cd infra
```
Запустите docker compose
```
docker compose up
```
Загрузка данных из excel(*файл должен быть в корне проекта)
```
python manage.py -n <Имя файла> -s <Имя листа excel>
```
