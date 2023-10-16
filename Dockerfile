FROM python:3.11

WORKDIR /app

COPY . /app/

RUN pip install Flask
RUN pip install flask_wtf

EXPOSE 80

CMD ["python", "app.py"]
