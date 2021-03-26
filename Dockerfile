FROM python:3.9-slim

COPY . /SmartHome-SolarMan
WORKDIR /SmartHome-SolarMan

RUN pip install -r requirements.txt
ENTRYPOINT ["sh"]