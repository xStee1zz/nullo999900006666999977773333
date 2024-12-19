import asyncio
import logging
from datetime import datetime, timedelta
import pytz
import random

from aiogram import Bot, Dispatcher, F, types
import aiohttp

logging.basicConfig(level=logging.INFO)

months = {
    "January": "января",
    "February": "февраля",
    "March": "марта",
    "April": "апреля",
    "May": "мая",
    "June": "июня",
    "July": "июля",
    "August": "августа",
    "September": "сентября",
    "October": "октября",
    "November": "ноября",
    "December": "декабря"
}

bot = Bot(token="7804030886:AAFmqYAPW08gRlS6N6ASwqp5GXNPyifcS64")
dp = Dispatcher()

@dp.message(F.chat.id == -1002258024710, F.text)
async def handler(message: types.Message) -> None:
    if message.text.lower() == "мут":
        if (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status in ["administrator", "creator"]:
            if message.reply_to_message:
                if (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)).status in ["administrator", "creator"]:
                    await message.reply("Невозможно выдать мут администратору чата.")
                else:
                    if (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)).status == "restricted":
                        await message.reply("Этот пользователь уже находится в муте.")
                    else:
                        end_time = datetime.now(pytz.timezone("Europe/Moscow")) + timedelta(hours=24)
                        end_time_timestamp = int(end_time.timestamp())
                        formatted_end_time = f"{end_time.day} {months[end_time.strftime('%B')]} {end_time.hour}:{end_time.strftime('%M')}"
                        await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, permissions=types.ChatPermissions(), until_date=end_time_timestamp)
                        await message.answer(f"<a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.full_name}</a> в муте до {formatted_end_time} по московскому времени.\nАдминистратор: <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>", parse_mode="HTML")
    if message.text.lower() == "размут":
        if (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)).status in ["administrator", "creator"]:
            if message.reply_to_message:
                if (await bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)).status == "restricted":
                    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, permissions=types.ChatPermissions(can_send_messages=True, can_send_media_messages=True), until_date=None)
                    await bot.promote_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
                    await message.answer(f"<a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.full_name}</a> размучен администратором <a href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a>", parse_mode="HTML")
                else:
                    await message.reply("Этот пользователь не находится в муте.")

    if message.text.startswith("."):
        text: str = message.text.lstrip(". ")

        if not text:
            return

        async with aiohttp.ClientSession() as session:
            key = random.choice([
                "AIzaSyCnBELxslQ9TZ2iJQqSo260w4zaqbjUZHc",
                "AIzaSyDbdc0DM9DxRTiSsBocwrSO719NHfs19IA"
            ])

            data = {
              "system_instruction": {
                "parts": {
                  "text": ""
                }
              },
              "contents": {
                "parts": {
                  "text": text
                }
              }
            }

            async with session.post(f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={key}", json=data) as response:
                try:
                    await message.reply((await response.json())["candidates"][0]["content"]["parts"][0]["text"], parse_mode="Markdown")
                except Exception as e:
                    await message.reply(f"Ошибка: {e}")

    if message.text.lower() == "!подрочить" and message.reply_to_message:
        text: str = random.choice([
            "и кончил на лицо",
            "и кончил в рот",
            "и кончил на живот",
            "и кончил внутрь"
        ])
        await message.answer(f"href='tg://user?id={message.from_user.id}'>{message.from_user.full_name}</a> выебал <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.full_name}</a> {text}", parse_mode="HTML")


asyncio.run(dp.start_polling(bot))
