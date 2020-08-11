FROM ubuntu:18.04

RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

RUN adduser recommender

WORKDIR /home/alex/Documents/fyp/

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

COPY app app
COPY migrations migrations
COPY recommender.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP recommender.py

RUN chown -R recommender:recommender ./
USER recommender

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]