FROM python:3.12-slim

ENV host "localhost"
ENV port_hub "5555"
ENV port_web "4000"

WORKDIR /app

COPY ./requirements.txt .
COPY ./scripts/entrypoint.sh .
COPY ./app /app

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN python -m pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

EXPOSE 4000
EXPOSE 5555

ENTRYPOINT [ "./entrypoint.sh" ]