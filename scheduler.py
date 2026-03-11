from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime,timedelta
import sqlite3
from aiogram import Bot
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)

scheduler = AsyncIOScheduler()

async def check_reminders():

    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    now = datetime.now()

    notes = cur.execute("SELECT id,user_id,text,file_id,file_type,date FROM notes WHERE done=0").fetchall()

    for n in notes:

        date = datetime.fromisoformat(n[5])

        if date - timedelta(hours=6) <= now <= date - timedelta(hours=5,minutes=50):

            user_id = n[1]

            text = f"Reminder ⏰\n\n{n[2]}"

            if n[3]:
                await bot.send_photo(user_id,n[3],caption=text)
            else:
                await bot.send_message(user_id,text)

scheduler.add_job(check_reminders,"interval",minutes=5)
