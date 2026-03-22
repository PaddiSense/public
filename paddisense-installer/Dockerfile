ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.11-alpine3.18
FROM ${BUILD_FROM}

COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY installer/ /app/installer/
COPY run.sh /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
