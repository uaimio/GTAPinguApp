FROM python:3-slim

# ffmpeg and crontab install
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg && apt-get install -y cron

# subdirectory creation and files creation
RUN mkdir -p /app/media
COPY media/* /app/media/

RUN mkdir -p /app/settings
COPY settings/* /app/settings/

RUN mkdir -p /app/logs

COPY planned_activities_docker/garbage_collector_dockerized.sh /app/garbage_collector.sh
COPY planned_activities_docker/planned_activities_dockerized.sh /app/planned_activities.sh
COPY bot.py /app/bot.py
COPY requirements.txt /app/requirements.txt
COPY bot_start.sh /app/bot_start.sh

WORKDIR /app

# scheduling the planned activities
RUN chmod 0644 garbage_collector.sh
RUN chmod 0644 planned_activities.sh
RUN chmod 0744 bot_start.sh
RUN crontab planned_activities.sh

RUN pip3 install -r requirements.txt

CMD ["sh", "-c", "./bot_start.sh"]