FROM docker.io/telegraf:1.38

RUN apt-get -q -y update \
  && DEBIAN_FRONTEND=noninteractive apt-get -q -y upgrade \
  && DEBIAN_FRONTEND=noninteractive apt-get -q -y install \
  python3 \
  python3-requests \
  python3-pip \
  python3-dotenv \
  incron \
  && DEBIAN_FRONTEND=noninteractive apt-get -q clean \
  && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --break-system-packages "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70"
RUN pip install --no-cache-dir sentry-sdk --break-system-packages

ADD ./send_http_req_GA.py /telegraf/send_http_req_GA.py

# Configure trigger for restarting app on log rotation
RUN rm /etc/incron.allow
ADD incron.conf /telegraf/telegraf_incron.conf
RUN incrontab /telegraf/telegraf_incron.conf

COPY entrypoint-extended.sh /
RUN chmod +x /entrypoint-extended.sh

ENTRYPOINT ["/entrypoint-extended.sh"]

CMD ["telegraf"]
