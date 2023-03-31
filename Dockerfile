FROM python:3.11-slim-buster

# ffmpeg and crontab install
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg && apt-get install -y cron

# subdirectory creation and files creation
RUN mkdir -p /app/media
COPY media/* /app/media/
RUN mkdir -p /app/settings
COPY settings/* /app/settings/
COPY bot.py /app/
COPY requirements.txt /app/

WORKDIR /app

# scheduling a garbage collection defined in garb-coll
RUN chmod 0644 settings/garb-coll.sh
RUN crontab settings/garb-coll.sh

RUN pip3 install -r requirements.txt --upgrade

CMD cron && python3 bot.py