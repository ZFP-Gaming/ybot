FROM python:latest

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
  ffmpeg

WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
