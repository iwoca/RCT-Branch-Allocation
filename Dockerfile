FROM python:3.11


RUN pip install Flask==3.0.0 flask_wtf==1.2.1 gunicorn==21.2.0


WORKDIR /app
COPY app /app/

EXPOSE 80

CMD ["gunicorn", "app:app", "-b", "0.0.0.0"]
