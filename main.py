from aiogram import Bot,Dispatcher,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command
import sqlite3
from config import BOT_TOKEN,ADMIN_ID
from keyboards import calendar,done_button,categories
from scheduler import scheduler
import asyncio

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

conn = sqlite3.connect("bot.db")
cur = conn.cursor()

temp_notes = {}

@dp.message(Command("start"))
async def start(m:Message):

    cur.execute("INSERT OR IGNORE INTO users(telegram_id,name) VALUES(?,?)",
    (m.from_user.id,m.from_user.full_name))
    conn.commit()

    await m.answer("Note yuboring")

@dp.message()
async def new_note(m:Message):

    temp_notes[m.from_user.id] = {}

    if m.text:
        temp_notes[m.from_user.id]["text"] = m.text

    if m.photo:
        temp_notes[m.from_user.id]["file_id"] = m.photo[-1].file_id
        temp_notes[m.from_user.id]["type"] = "photo"

    await m.answer("Sana tanlang",reply_markup=calendar())

@dp.callback_query(F.data.startswith("date_"))
async def select_date(c:CallbackQuery):

    date = c.data.split("_")[1]

    temp_notes[c.from_user.id]["date"] = date

    await c.message.edit_text("Bo'lim tanlang",reply_markup=categories())

@dp.callback_query(F.data.startswith("cat_"))
async def select_cat(c:CallbackQuery):

    cat = c.data.split("_")[1]

    data = temp_notes[c.from_user.id]

    cur.execute("""
    INSERT INTO notes(user_id,text,file_id,file_type,category_id,date)
    VALUES(?,?,?,?,?,?)
    """,
    (
    c.from_user.id,
    data.get("text"),
    data.get("file_id"),
    data.get("type"),
    cat,
    data["date"]
    ))

    conn.commit()

    await c.message.edit_text("Note saqlandi")

@dp.callback_query(F.data.startswith("done_"))
async def done(c:CallbackQuery):

    note_id = c.data.split("_")[1]

    cur.execute("UPDATE notes SET done=1 WHERE id=?",(note_id,))
    conn.commit()

    await c.message.delete()

@dp.message(Command("search"))
async def search(m:Message):

    await m.answer("Sana tanlang",reply_markup=calendar())

@dp.callback_query(F.data.startswith("date_"))
async def search_date(c:CallbackQuery):

    date = c.data.split("_")[1]

    notes = cur.execute("SELECT id,text FROM notes WHERE date=? AND done=0",(date,)).fetchall()

    if not notes:
        await c.message.edit_text("Note yoq")
        return

    for n in notes:

        await bot.send_message(
        c.from_user.id,
        n[1],
        reply_markup=done_button(n[0])
        )

@dp.message(Command("admin"))
async def admin(m:Message):

    if m.from_user.id != ADMIN_ID:
        return

    await m.answer("Yangi bo'lim nomini yuboring")

@dp.message()
async def add_cat(m:Message):

    if m.from_user.id != ADMIN_ID:
        return

    cur.execute("INSERT INTO categories(name) VALUES(?)",(m.text,))
    conn.commit()

    await m.answer("Bo'lim qo'shildi")

async def main():

    scheduler.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
