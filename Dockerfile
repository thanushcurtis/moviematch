FROM python:3.9


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app


COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt && \
    chmod -R 777 /usr/local/lib/python3.9/site-packages


COPY . /app/


EXPOSE 8080


CMD ["gunicorn", "--timeout", "400", "-b", "0.0.0.0:8080", "app:app"]

