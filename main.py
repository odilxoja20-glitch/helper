import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from groq import Groq

# Твои данные
BOT_TOKEN = "8554534529:AAEGPnmyG88UWmXaMMDVLJXrteuMdP3NHwg"
GROQ_API = "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"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = Groq(api_key=GROQ_API)

# Чтение системного промпта из файла
def load_system_prompt():
    try:
        with open("prompt.system", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "Ты — продвинутый AI-ассистент."

# Хранилище истории
user_history = {}

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Я готов к работе. Приветствую вас, я автоответчик Odilxoja!")

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    
    # Инициализация истории с загруженным промптом
    if user_id not in user_history:
        user_history[user_id] = [{"role": "system", "content": load_system_prompt()}]
        is_first_message = True
    else:
        is_first_message = False
    
    user_history[user_id].append({"role": "user", "content": message.text})
    
    try:
        chat_completion = client.chat.completions.create(
            messages=user_history[user_id],
            model="llama-3.1-8b-instant",
        )
        response = chat_completion.choices[0].message.content
        
        user_history[user_id].append({"role": "assistant", "content": response})
        
        if is_first_message:
            final_response = (
                "Я ИИ помощник Odilxoja. Отвечу на ваши вопросы, "
                "пока Odilxoja занят.\n\n" + response
            )
        else:
            final_response = response
            
        await message.answer(final_response)
        
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
