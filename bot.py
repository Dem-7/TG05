import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import WEATHER_API_KEY, CAT_API_KEY, BOT_TOKEN, WEATHER_URL, CAT_URL

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Я ваш помощник. Вот что я могу:\n"
        "/weather <город> — узнать погоду в указанном городе.\n"
        "/cat — получить случайное изображение кота."
    )

# Команда /weather
@dp.message(Command("weather"))
async def weather(message: Message):
    # Разбиваем текст сообщения на команду и аргументы
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Пожалуйста, укажите город.")
        return

    city = args[1]  # Город из сообщения пользователя
    params = {
        'q': city,
        'appid': WEATHER_API_KEY,
        'units': 'metric',  # Температура в градусах Цельсия
        'lang': 'ru'        # Названия на русском языке
    }

    try:
        response = requests.get(WEATHER_URL, params=params)
        data = response.json()

        if data['cod'] != 200:
            await message.answer("Город не найден. Попробуйте снова.")
            return

        # Парсим данные о погоде
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        message_text = (
            f"Погода в {city.capitalize()}:\n"
            f"Описание: {weather_description}\n"
            f"Температура: {temperature}°C\n"
            f"Влажность: {humidity}%\n"
            f"Скорость ветра: {wind_speed} м/с"
        )
        await message.answer(message_text)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

# Команда /cat
@dp.message(Command("cat"))
async def cat(message: Message):
    headers = {
        'x-api-key': CAT_API_KEY
    }

    try:
        response = requests.get(CAT_URL, headers=headers)
        data = response.json()

        if not data:
            await message.answer("Не удалось получить изображение кота. Попробуйте снова.")
            return

        cat_image_url = data[0]['url']
        await bot.send_photo(chat_id=message.chat.id, photo=cat_image_url)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

# Обработка неизвестных команд
@dp.message()
async def unknown(message: Message):
    await message.answer("Извините, я не понимаю эту команду.")

# Запуск бота
if __name__ == '__main__':
    dp.run_polling(bot)