FROM python:3.11.6-slim@sha256:55a4707a91d43b6397215a57b818d2822e66c27fd973bb82eb71b7512c15a4da


RUN pip install Flask==3.0.0 flask_wtf==1.2.1 gunicorn==21.2.0


WORKDIR /app
COPY app /app/

EXPOSE 80

CMD ["gunicorn", "app:app", "-b", "0.0.0.0"]
