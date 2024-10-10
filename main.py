import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TELEGRAM_API_TOKEN, OPENWEATHER_API_KEY1

API_TOKEN = TELEGRAM_API_TOKEN  # замените на токен вашего бота
OPENWEATHER_API_KEY = OPENWEATHER_API_KEY1  # замените на ваш API-ключ OpenWeather
CITY_NAME = 'Izhevsk'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={OPENWEATHER_API_KEY}&units=metric&lang=ru'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот, который показывает погоду в городе Ижевск. Просто напиши '/weather', чтобы узнать текущие погодные условия.")

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Я просто показываю текущую погоду в городе Ижевск. Просто напиши '/weather', чтобы узнать текущие погодные условия.")

@dp.message(Command('weather'))
async def get_weather(message: Message):
    try:
        response = requests.get(WEATHER_URL, timeout=10)  # Добавлен тайм-аут в 10 секунд
        data = response.json()

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            weather_info = (
                f"Погода в {CITY_NAME}:\n"
                f"Описание: {weather_description}\n"
                f"Температура: {temperature}°C\n"
                f"Влажность: {humidity}%\n"
                f"Скорость ветра: {wind_speed} м/с"
            )
        else:
            weather_info = "Не удалось получить данные о погоде. Попробуйте позже."

    except requests.exceptions.Timeout:
        weather_info = "Сервер не отвечает. Попробуйте позже."
    except requests.exceptions.RequestException as e:
        weather_info = f"Произошла ошибка: {e}"

    await message.reply(weather_info)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":  # Исправлено здесь
    asyncio.run(main())