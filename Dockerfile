FROM ubuntu:latest

RUN apt update && apt upgrade -y

RUN apt install git build-essential python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info fontconfig -y

COPY requirements/common.txt requirements/common.txt
RUN pip install -U pip && pip install -r requirements/common.txt

COPY ./api /app/api
COPY ./bin /app/bin
COPY ./jinja /app/jinja
COPY ./includes /app/includes
COPY wsgi.py /app/wsgi.py
WORKDIR /app

RUN useradd demo
USER demo

#ENV OSFONTDIR=/usr/share/fonts
#RUN fc-cache --really-force --verbose


EXPOSE 8080

ENTRYPOINT ["bash", "/app/bin/run.sh"]