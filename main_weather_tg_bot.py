import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды.")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        temp = data["main"]["temp"]

        weather_desk = data["weather"][0]["main"]
        if weather_desk in code_to_smile:
            wd = code_to_smile[weather_desk]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!!!"

        humidity = data["main"]["humidity"]
        speed = data["wind"]["speed"]
        pressure = data["main"]["pressure"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        await message.reply(f"*** {datetime.datetime.now().strftime('%H:%M %d-%m-%Y')} ***\n"
              f"Погода в городе: {city}\nТемпература: {temp} C°{wd}\n"
              f"Влажность: {humidity} %\nСкорость ветра: {speed} м\с\n"
              f"Давление: {pressure} мм.рт.ст.\nВремя восхода: {sunrise_timestamp}\n"
              f"Время заката: {sunset_timestamp}\n*** Хорошего дня!!! ***"
              )

    except:
        await message.reply("\U00002620 Проверьте название города! \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)

