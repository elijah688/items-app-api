FROM python:3.9.0rc1-alpine3.12

ENV JWT_SECRET_KEY=secret

RUN apk update && apk upgrade \
    && apk add --no-cache git \
    && git clone --branch master --depth 1 https://gitlab.com/elijah688/items-app-api.git  \ 
    && cd items-app-api \
    && pip install -r requirements.txt \ 
    && apk del git 

WORKDIR /items-app-api

EXPOSE 5000

CMD [ "python", "app.py" ]