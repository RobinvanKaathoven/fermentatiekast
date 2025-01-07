FROM python:3.9-slim-buster

WORKDIR /opt/pihome

RUN apt update && apt install -y nmap
COPY ["./application/", "./"]
RUN pip install -r requirements.txt

CMD python api.py