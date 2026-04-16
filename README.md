## Тестовое задание python-разработчик 
### Как запустить проект:

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

Для доступа к админке создать супервользователя:

```
python3 manage.py createsuperuser
```

Запустить проект:

```
python3 manage.py runserver
```
Автор: К.Гурашкин