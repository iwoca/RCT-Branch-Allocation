FROM python:3.11

WORKDIR /app

COPY . /app/

RUN pip install Flask
RUN pip install flask_wtf
RUN pip install sqlalchemy

EXPOSE 5000

CMD ["python", "app.py"]
