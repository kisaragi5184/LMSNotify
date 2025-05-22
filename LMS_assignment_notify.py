import datetime
from zoneinfo import ZoneInfo  # Python 3.9以降

import icalendar
import requests

# Discord Webhook URL（書き換えてください）
DISCORD_WEBHOOK_URL = "https://discordapp.com/api/webhooks/xxxxxxxxxxx"

# カレンダーURL
ICS_URL = "https://lms.s.isct.ac.jp/2025/calendar/xxxxxxxxxx"

# 日本時間に設定
JST = ZoneInfo("Asia/Tokyo")


def send_discord_notify(message):
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)


def get_upcoming_events():
    res = requests.get(ICS_URL)
    cal = icalendar.Calendar.from_ical(res.content)

    upcoming = []
    now = datetime.datetime.now(tz=JST)  # 現在時刻をJSTで取得

    for component in cal.walk():
        if component.name == "VEVENT":
            summary = str(component.get("summary"))
            dtstart = component.get("dtstart").dt

            # 時刻をdatetimeに変換してJSTに
            if isinstance(dtstart, datetime.date) and not isinstance(
                dtstart, datetime.datetime
            ):
                dtstart = datetime.datetime.combine(dtstart, datetime.time(0, 0))
            if isinstance(dtstart, datetime.datetime):
                if dtstart.tzinfo is None:
                    dtstart = dtstart.replace(tzinfo=datetime.timezone.utc)
                dtstart = dtstart.astimezone(JST)

            delta_minutes = int((dtstart - now).total_seconds() / 60)

            upcoming.append((summary, dtstart, delta_minutes))

    return upcoming


def check_and_notify():
    events = get_upcoming_events()
    for summary, dt, delta_minutes in events:
        if 1430 <= delta_minutes <= 1450:  # 約24時間前
            send_discord_notify(
                f"⏰ **明日締切の課題があります！**\n📄 {summary}\n🕒 期限: {dt.strftime('%Y-%m-%d %H:%M')}"
            )
        elif 50 <= delta_minutes <= 70:  # 約1時間前
            send_discord_notify(
                f"⚠️ **あと1時間で締切の課題！**\n📄 {summary}\n🕒 期限: {dt.strftime('%Y-%m-%d %H:%M')}"
            )
        elif 0 <= delta_minutes <= 5:
            send_discord_notify(
                f"🚨 **まもなく締切です！**\n📄 {summary}\n🕒 期限: {dt.strftime('%Y-%m-%d %H:%M')}"
            )


def check():
    events = get_upcoming_events()
    send_discord_notify(f"--課題一覧--")

    for summary, dt, delta_minutes in events:
        if 0 <= delta_minutes <= 1440:  # 約24時間前
            send_discord_notify(
                f"⏰ **締切が近い課題があります！**\n📄 {summary}\n🕒 期限: {dt.strftime('%Y-%m-%d %H:%M')}"
            )


check()
check_and_notify()
