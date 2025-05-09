# Django-Web-App-for-SweBench-Evaluation

Private API to evaluate your LLM with SWEBench.

```
py -m venv django_venv
.\django_venv\Scripts\activate
pip install Django
pip install djangorestframework djangorestframework-api-key
pip install python-decouple
django-admin startproject django_project .
python manage.py startapp swe_api
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
