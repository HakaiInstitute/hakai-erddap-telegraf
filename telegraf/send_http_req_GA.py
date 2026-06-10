import sys
import requests
import json
import os
import sentry_sdk
from sentry_sdk.crons import monitor

sentry_sdk.init(
    send_default_pii=True,
)

@monitor(monitor_slug='hakai-erddap-telegraf-checkin')
def main():
    url = os.environ.get(
        'GA_URL', 'http://www.google-analytics.com/mp/collect')
    secret = os.environ.get(
        'GA_API_SECRET')
    id = os.environ.get(
        'GA_MEASUREMENT_ID')

    full_url = f"{url}?api_secret={secret}&measurement_id={id}"

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

if __name__ == "__main__":
    main()
    sentry_sdk.flush()
