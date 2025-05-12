## Create virtual environment

`python -m venv venv`

## window activated

`source ./venv/Scripts/activate`

## Install django and rest

```
python -m pip install Django
pip install django djangorestframework
```

## Create root app or folder or configure folder

`django-admin startproject config .`

## Create a Apps folder

`mkdir -p apps/{users,products,orders,inventory}`
`touch apps/__init__.py`

```
python manage.py startapp inventory apps/inventory
python manage.py startapp products apps/products
python manage.py startapp orders apps/orders
python manage.py startapp users apps/users
```

## Add migration

```
docker compose exec web python manage.py makemigrations products
docker compose exec web python manage.py migrate
```

## Get DB

```
docker exec -t pos_api-db-1 pg_dump -U postgres -d online > db_dump.sql
```
