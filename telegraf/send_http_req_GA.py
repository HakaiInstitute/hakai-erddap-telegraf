import sys
import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv
import sentry_sdk
# from sentry_sdk.crons import monitor
from sentry_sdk.crons import capture_checkin
from sentry_sdk.crons.consts import MonitorStatus

load_dotenv(Path(__file__).parent / ".env", override=False)
load_dotenv(override=False)



# @monitor(monitor_slug='hakai-erddap-telegraf-checkin')
def main():
    sentry_sdk.init(
        debug=True,
        send_default_pii=True,
    )
    capture_checkin(
        monitor_slug="hakai-erddap-telegraf-checkin",
        status=MonitorStatus.OK,
    )
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
    
    sentry_sdk.flush()

if __name__ == "__main__":
    main()
