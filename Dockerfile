FROM python:3.6


RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ['gunicorn Darts.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3']