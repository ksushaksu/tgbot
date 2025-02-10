import os
import logging
import asyncio
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils.executor import start_polling

TOKEN = "8035059939:AAF0A1MK-88s7qE6B5l-XwOOXvcJLEj-5Kc"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HOLIDAYS = {
    "2025-02-02": "День «Ы»",
    "2025-02-03": "Всемирный день борьбы с ненормативной лексикой",
    "2025-02-04": "День рождения резиновых калош",
    "2025-02-05": "День разукрашивания планов на будущее",
    "2025-02-05": "День снегопада",
    "2025-02-07": "День варенья",
    "2025-02-08": "День подбрасывания монетки",
    "2025-02-09": "День пиццы",
    "2025-02-10": "День домового",
    "2025-02-10": "День рассматривания лиц",
    "2025-02-15": "День завязывания узелков на счастье",
    "2025-02-16": "День валенок",
    "2025-02-18": "День пельменей",
    "2025-02-20": "День леденцовых петушков",
    "2025-02-20": "День профессионального алкоголика",
    "2025-02-22": "День приманивания хорошего настроения",
    "2025-02-23": "День сражений подушками",
    "2025-02-24": "День прогулки по зимнему лесу",
    "2025-02-26": "День неторопливости",
    "2025-02-26": "День поиска норы спящего лета",
    "2025-02-27": "День оптимиста",
    "2025-02-27": "Всемирный день полярного медведя"
}

# Список пользователей
users = set()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    users.add(message.chat.id)
    await message.reply("Привет! Я буду присылать тебе уведомления о праздниках в 9 утра.")

async def send_holiday():
    while True:
        now = datetime.datetime.now()
        if now.hour == 9 and now.minute == 0:
            today = now.strftime("%Y-%m-%d")
            if today in HOLIDAYS:
                holiday_text = HOLIDAYS[today]
                image_path = f"images/{today}.jpg"  # Ожидаем, что изображения названы по дате праздника
                for user_id in users:
                    if os.path.exists(image_path):
                        with open(image_path, "rb") as photo:
                            await bot.send_photo(user_id, photo, caption=holiday_text)
                    else:
                        await bot.send_message(user_id, holiday_text)
        await asyncio.sleep(60)  # Проверять каждую минуту

async def main():
    asyncio.create_task(send_holiday())
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
