## Тестовое задание python-разработчик 
### Как запустить проект:

Используется Python 3.9.10, 
Basic Auth (username, password)

#### Разворачивание проекта:

Клонировать репозиторий и перейти в него:

```
git clone git@github.com:CrockoMan/absolut_pos.git
cd absolut_pos
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
source env/bin/activate
```

Установить зависимости из requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

При необходимости, заполнить .env:

Указать тип используемой БД postgres или sqlite
```
DATABASE_TYPE=sqlite или postgres
```
Для Postgres указать параметры подключения
```
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=librarius
DB_HOST=localhost
DB_PORT=5432
```

Для доступа к админке создать суперпользователя:

```
python3 manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```

URLS:
```
/api/v1/surveys/ (GET, POST, PUT)
/api/v1/surveys_response/id_опроса/
```

Вопросы и ответы к ним:
/api/v1/surveys/ (GET, POST, PUT)

GET:
```
{
    "id": 9,
    "author": 2,
    "name": "Овощи",
    "survey_date": "2026-04-17",
    "questions": [
        {
            "id": 34,
            "text": "Любите томаты?",
            "order": 0,
            "questions": [
                {
                    "id": 100,
                    "text": "Нет",
                    "order": 1
                },
                {
                    "id": 101,
                    "text": "Да",
                    "order": 2
                },
                {
                    "id": 102,
                    "text": "Не знаю",
                    "order": 3
                }
            ]
        },
        {
            "id": 35,
            "text": "Любите помидоры2?",
            "order": 0,
            "questions": [
                {
                    "id": 103,
                    "text": "Не люблю",
                    "order": 0
                },
                {
                    "id": 104,
                    "text": "Люблю",
                    "order": 0
                },
                {
                    "id": 105,
                    "text": "Затрудняюсь ответить",
                    "order": 0
                }
            ]
        }
    ]
}
```
POST
```
{
    "author": 2,
    "name": "Овощи",
    "questions": [
        {
            "text": "Любите томаты?",
            "order": 0,
            "questions": [
                {
                    "text": "Нет",
                    "order": 1
                },
                {
                    "text": "Да",
                    "order": 2
                },
                {
                    "text": "Не знаю",
                    "order": 3
                }
            ]
        },
        {
            "text": "Любите помидоры2?",
            "order": 0,
            "questions": [
                {
                    "text": "Не люблю",
                    "order": 0
                },
                {
                    "text": "Люблю",
                    "order": 0
                },
                {
                    "text": "Затрудняюсь ответить",
                    "order": 0
                }
            ]
        }
    ]
}
```
Получить вопрос и ответить на него:
/api/v1/surveys_response/id_опроса/ (GET, POST)

GET
```
{
    "survey_id": 9,
    "response_id": 2,
    "survey_name": "Овощи",
    "current_question": {
        "id": 35,
        "text": "Любите помидоры2?",
        "items": [
            {
                "id": 103,
                "text": "Не люблю"
            },
            {
                "id": 104,
                "text": "Люблю"
            },
            {
                "id": 105,
                "text": "Затрудняюсь ответить"
            }
        ]
    }
}
```
Формат ответа на вопрос:

POST
```
{
    "current_question_id": 35,
    "answer_id": 103
}
```

Реализована админка
В админке, в разделе "Опросы" реализована выгрузка отчёта со статистикой в формате csv, xls

Для запуска тестов использовать:
```
python manage.py test --noinput  --keepdb core.tests.views.api.v1.test_survey
```

Автор: К.Гурашкин