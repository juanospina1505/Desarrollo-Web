FROM python:3.15-rc-slim

WORKDIR /app

COPY . /app/

EXPOSE 8000

ENV MONGO_HOST='mongodb+srv://juanCa15:PORT34erySADF@cluster0.fgze7ac.mongodb.net/videogames_django?retryWrites=true&w=majority'
ENV MONGO_DB='videogames_django'

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "manage.py", "runserver","0.0.0.0:8000"]