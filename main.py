import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("8142263044:AAE2IdeM6psQJzPvFY0G3KpZzSQV1j8pGPg")
CHAT_ID = os.getenv("5755871976")

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="America/New_York")

messages = [
    ("18:00", "1H Left for Asia Killzone"),
    ("19:00", "Asia Killzone Begins"),
    ("00:00", "Asia Ends & 1H Left for London Killzone"),
    ("01:00", "London Killzone Begins"),
    ("05:00", "London Ends"),
    ("06:00", "1H Left for NY AM Killzone"),
    ("07:00", "NY AM Killzone Begins"),
    ("10:00", "NY AM Ends"),
    ("13:00", "1H Left for NY PM Killzone"),
    ("14:00", "NY PM Killzone Begins"),
    ("15:00", "NY PM Ends"),
]

async def send_msg(text):
    await bot.send_message(CHAT_ID, text)

def schedule_jobs():
    for t, msg in messages:
        hour, minute = map(int, t.split(":"))
        scheduler.add_job(
            send_msg,
            "cron",
            hour=hour,
            minute=minute,
            day_of_week="mon-fri",  # excludes Saturday & Sunday
            args=[msg]
        )

async def main():
    print("Assistant_Bot Running...")
    schedule_jobs()
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
