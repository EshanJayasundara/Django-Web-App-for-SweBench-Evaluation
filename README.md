# Django-Web-App-for-SweBench-Evaluation

Private API to evaluate your LLM with SWEBench.

Creation:

```bash
py -m venv .venv
.\.venv\Scripts\activate
pip install Django djangorestframework djangorestframework-api-key python-decouple
django-admin startproject django_project .
python manage.py startapp swe_api
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Setup:

```bash
git clone https://github.com/EshanJayasundara/Django-Web-App-for-SweBench-Evaluation
cd Django-Web-App-for-SweBench-Evaluation
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
echo -e "DJANGO_SECRET_KEY=<your-secret>\nDEBUG=True" > .env
python manage.py migrate
python manage.py createsuperuser
```

Run:

```bash
python manage.py runserver
```
