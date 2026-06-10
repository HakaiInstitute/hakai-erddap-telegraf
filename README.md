# hakai-erddap-telegraf
telegraf log wrangling to scrape apache or nginx logs for erddap related requests and sent to plausible or google analytics event api's
see https://www.influxdata.com/time-series-platform/telegraf/ for more details on teleraf

# Quick Start

create env file
```
cp .env.sample .env
```

edit .env values. This to check are
  - LOG_FILE - this should point to the nginx or apache log folder. not directly to a file.
  - HOST_URL - hostname to report in plausible with protocol
  - DOMAINS - keys used by plausible to route events see https://plausible.io/docs/events-api#request-body-json-parameters
  - PLAUSIBLE_URL - url to plausible instance 
  - SENTRY_DSN - url to sentry project for monitering up time

review telegraf/telegraf.conf. the most important one being
  - `files` under [[inputs.tail]]

find the group that has read access to the log files
```
stat -c '%g' /var/log/apache2
```

use the resulting number to set the group in the telegraf container by editing the docker compose and adding
```
user: telegraf:4
```
where `4` is the gid of the group


Start the container
```
sudo docker-compose up -d
```

# TODO
- log file name is hard coded i.e. catalogue-ssl-access.log. it would be nice to make it based on an environment variable.