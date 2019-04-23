FROM python:3.7-alpine
RUN apk add --no-cache build-base linux-headers

WORKDIR /usr/src/app

COPY app/requirements.txt app/dat-a-dog.py ./
COPY app/templates/dat-a-dog.html ./templates/dat-a-dog.html

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./dat-a-dog.py" ]
