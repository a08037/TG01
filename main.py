import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN, WEATHER_API_KEY
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/weather")

@dp.message(F.text == "что такое ИИ?")
async def aitext(message: Message):
    await message.answer(
        'Искусственный интеллект — это свойство искусственных интеллектуальных систем выполнять творческие функции, которые традиционно считаются прерогативой человека; наука и технология создания интеллектуальных машин, особенно интеллектуальных компьютерных программ'
    )

@dp.message(F.photo)
async def react_photo(message: Message):
    responses = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(responses)
    await message.answer(rand_answ)

@dp.message(Command('photo'))
async def photo(message: Message):
    photos = [
        "https://img.freepik.com/free-vector/cartoon-style-robot-vectorart_78370-4103.jpg",
        "https://img.freepik.com/free-vector/robot-ai-technology-character-icon_169507926.htm"
    ]
    rand_photo = random.choice(photos)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

# Функция для получения прогноза погоды
def get_weather():
    city = "Moscow"  # Можно заменить на любой город
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Погода в {city}: {temp}°C, {description.capitalize()}"
    else:
        return "Не удалось получить прогноз погоды."

# Команда для прогноза погоды
@dp.message(Command("weather"))
async def weather(message: Message):
    weather_info = get_weather()
    await message.answer(weather_info)

async def main():
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("Бот был остановлен вручную.")

if __name__ == "__main__":
    asyncio.run(main())
