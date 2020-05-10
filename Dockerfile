FROM python:alpine

WORKDIR code/

COPY app/ app/
COPY config.py  ./
COPY entrypoint.sh  ./
COPY requirements.txt  ./

RUN pip3 install -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]
