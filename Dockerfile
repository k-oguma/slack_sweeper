FROM python:3.8-alpine
#ARG SLACK_TOKEN
COPY ./requirements.txt /root/requirements.txt
COPY --chown=0 ./sweeper.py /root/sweeper.py
COPY ./.envrc /root/.envrc
WORKDIR /root/

RUN apk add gcc musl-dev && \
  pip install -r /root/requirements.txt

CMD ["/root/sweeper.py"]
