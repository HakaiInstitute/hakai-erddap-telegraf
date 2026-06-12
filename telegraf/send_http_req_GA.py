import sys
import requests
import json
import os
import time

SENTRY_MONITOR_SLUG = "hakai-erddap-telegraf-checkin"
SENTRY_INGEST = "https://o56764.ingest.us.sentry.io"
SENTRY_CRONS = (
    SENTRY_INGEST
    + "/api/4507091651526656/cron/"
    + SENTRY_MONITOR_SLUG
    + "/145d7992e3df09af3614048708523550/"
)

url = os.environ.get(
    'GA_URL', 'http://www.google-analytics.com/mp/collect')
secret = os.environ.get(
    'GA_API_SECRET')
id = os.environ.get(
    'GA_MEASUREMENT_ID')

full_url = f"{url}?api_secret={secret}&measurement_id={id}"

SENTRY_CHECKIN_INTERVAL = 300  # seconds
last_sentry_checkin = 0

for line in sys.stdin:
    sys.stdout.write(line)
    json_obj = json.loads(line)
    headers = {
    # "User-Agent": json_obj['agent'],
    # "X-Forwarded-For": json_obj['host'],
    "Content-Type": "application/json"
    }
    x = requests.post(full_url, json=json_obj, headers=headers)
    sys.stdout.write(x.text)

    now = time.monotonic()
    if now - last_sentry_checkin >= SENTRY_CHECKIN_INTERVAL:
        sentry_headers = {"Content-Type": "application/json"}
        sentry_body = {"environment": os.environ.get("SENTRY_ENVIRONMENT"), "status": "ok"}
        x = requests.post(SENTRY_CRONS, json=sentry_body, headers=sentry_headers)
        sys.stdout.write(x.text)
        last_sentry_checkin = now
