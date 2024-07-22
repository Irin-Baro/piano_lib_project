FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

CMD ["sh", "-c", "manage.py collectstatic --noinput && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]