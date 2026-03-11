from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import sqlite3

def calendar():
    today = datetime.now()
    buttons = []

    for i in range(20):
        d = today + timedelta(days=i)

        buttons.append(
            InlineKeyboardButton(
                text=d.strftime("%d %a"),
                callback_data=f"date_{d.strftime('%Y-%m-%d')}"
            )
        )

    rows = [buttons[i:i+4] for i in range(0,len(buttons),4)]

    return InlineKeyboardMarkup(inline_keyboard=rows)

def done_button(note_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="O'qib bo'ldim",callback_data=f"done_{note_id}")]
        ]
    )

def categories():
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    cats = cur.execute("SELECT id,name FROM categories").fetchall()

    rows = []
    for c in cats:
        rows.append(
            [InlineKeyboardButton(text=c[1],callback_data=f"cat_{c[0]}")]
        )

    return InlineKeyboardMarkup(inline_keyboard=rows)
