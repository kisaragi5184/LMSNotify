import requests
import datetime
from icalendar import Calendar
import pytz
import os
import json

ICS_URL = os.environ['ICS_URL']
DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK']
CACHE_FILE = 'notified.json'

JST = pytz.timezone('Asia/Tokyo')
now = datetime.datetime.now(JST)
later = now + datetime.timedelta(hours=24)

def fetch_events():
    res = requests.get(ICS_URL)
    cal = Calendar.from_ical(res.content)
    events = []

    for component in cal.walk():
        if component.name == "VEVENT":
            summary = str(component.get('summary'))
            dtstart = component.get('dtstart').dt
            if not isinstance(dtstart, datetime.datetime):
                continue
            dtstart = dtstart.astimezone(JST)
            if now <= dtstart <= later:
                events.append((summary, dtstart))

    return events

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(list(cache), f)

def notify(summary, dt):
    message = f"⚠️【締切24時間以内】「{summary}」は {dt.strftime('%Y-%m-%d %H:%M')} に締切です！"
    requests.post(DISCORD_WEBHOOK, json={"content": message})
    print("通知:", message)

def main():
    notified = load_cache()
    events = fetch_events()
    for summary, dt in events:
        key = f"{summary}_{dt.isoformat()}"
        if key not in notified:
            notify(summary, dt)
            notified.add(key)
    save_cache(notified)

if __name__ == "__main__":
    main()

