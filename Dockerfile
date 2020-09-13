FROM python:3.9.0rc1-alpine3.12

ENV JWT_SECRET_KEY=secret

WORKDIR /items-app-api

RUN pip install -r requirements.txt \ 
    && apk del git 

EXPOSE 5000

CMD [ "python", "app.py" ]