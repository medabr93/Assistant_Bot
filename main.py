import os
import asyncio
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiohttp import web
import pytz

# Environment variables from Railway
BOT_TOKEN = os.getenv("8142263044:AAE2IdeM6psQJzPvFY0G3KpZzSQV1j8pGPg")
CHAT_ID = os.getenv("5755871976")

bot = Bot(token=BOT_TOKEN)
scheduler = AsyncIOScheduler(timezone="America/New_York")

# Killzone messages: (HH:MM, message text)
killzone_messages = [
    ("18:00", "1H Left for Asia Killzone"),
    ("19:00", "Asia Killzone Begins"),
    ("00:00", "Asia Ends & 1H Left for London Killzone"),
    ("01:00", "London Killzones Begins"),
    ("05:00", "London Ends"),
    ("06:00", "1H Left for NY AM Killzone"),
    ("07:00", "NY AM Killzones Begins"),
    ("10:00", "NY AM Ends"),
    ("13:00", "1H Left for NY PM Killzone"),
    ("14:00", "NY PM Killzones Begins"),
    ("15:00", "NY PM Ends")
]

async def send_msg(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)

def schedule_jobs():
    for time_str, msg in killzone_messages:
        hour, minute = map(int, time_str.split(":"))
        scheduler.add_job(send_msg, 'cron', day_of_week='mon-fri', hour=hour, minute=minute, args=[msg])

# Optional: small web server for uptime pings (keep Railway free instance awake)
async def handle_health(request):
    return web.Response(text="OK")

async def start_webserver():
    app = web.Application()
    app.router.add_get("/health", handle_health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", 8000)))
    await site.start()

async def main():
    schedule_jobs()
    scheduler.start()
    await start_webserver()
    print("🤖 Forex Killzone Bot Started Successfully")
    # Keep the bot alive (long polling)
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
