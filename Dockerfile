FROM python:3.12
LABEL authors="arian.ott"

COPY . .
RUN pip3 install -r requirements.txt
RUN python3 main2.py

