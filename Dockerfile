FROM python:3.8-alpine

RUN apk update
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev
RUN mkdir -p /var/www/mednote
WORKDIR /var/www/mednote

COPY ./ .

RUN pip3 install -r ./requirements.txt
RUN apk add --update --no-cache bind-tools

CMD [ "python", "./main.py" ]
EXPOSE 8080
EXPOSE 27017
