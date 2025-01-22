FROM dtcooper/raspberrypi-os:bookworm
WORKDIR /application



RUN set -xe \ 
    && apt update \
    && apt install -y nmap \
    && apt install -y python3  python3-pip
COPY ["./application/", "./"]
RUN pip install -r requirements.txt --break-system-packages

CMD python3 api.py
