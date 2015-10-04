FROM debian:jessie

RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y

WORKDIR /src
ADD requirements.txt /src/requirements.txt
RUN pip3 install -r requirements.txt
