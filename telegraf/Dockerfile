FROM docker.io/telegraf:latest

RUN apt-get -q -y update \
  && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade \
  && DEBIAN_FRONTEND=noninteractive apt-get -q -y install \
  python3 \
  python3-requests \
  python3-pip \
  incron \
  && DEBIAN_FRONTEND=noninteractive apt-get -q clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade sentry-sdk

ADD ./send_http_req_GA.py /telegraf/send_http_req_GA.py

# Configure trigger for restarting app on log rotation
RUN rm /etc/incron.allow
ADD incron.conf /telegraf/telegraf_incron.conf
RUN incrontab /telegraf/telegraf_incron.conf

COPY entrypoint-extended.sh /
RUN chmod +x /entrypoint-extended.sh

ENTRYPOINT ["/entrypoint-extended.sh"]

CMD ["telegraf"]
