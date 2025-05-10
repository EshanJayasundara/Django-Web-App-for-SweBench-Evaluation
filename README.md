# Django-Web-App-for-SweBench-Evaluation

Private API to evaluate your LLM with SWEBench.

Creation:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install Django djangorestframework djangorestframework-api-key python-decouple
django-admin startproject django_project .
python3 manage.py startapp swe_api
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

Setup:

```bash
git clone https://github.com/EshanJayasundara/Django-Web-App-for-SweBench-Evaluation
cd Django-Web-App-for-SweBench-Evaluation
python3 -m venv .venv
source .venv/bin/activate
pip3 install -e .
echo -e "DJANGO_SECRET_KEY=<your-secret>\nDEBUG=True" > .env
python3 manage.py migrate
python3 manage.py createsuperuser
```

Run:

```bash
python3 manage.py runserver
```
