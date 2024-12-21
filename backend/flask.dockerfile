FROM python:3.6-slim-buster
## app - папка, работающая внутри контейнера flask
WORKDIR /app  

COPY requirements.txt ./

RUN pip install -r requirements.txt

## копируем остальные файлы из текущей директори backend
COPY . .

# открываем порт 4000
EXPOSE 4000

## с помощью команд запускаем flask на хосте 0.0.0.0 с портом 4000
CMD [ "flask", "run", "--host=0.0.0.0", "--port=4000"]