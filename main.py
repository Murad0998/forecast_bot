from aiogram import Bot, Dispatcher, executor, types
from parsers import current_weather, week_weather
from parsers import url, url2
from aiogram.types import InputFile
import os


TOKEN = '6295284891:AAEboMpnbN9B6HhazHnu1FOMM5RDCkGvVO4'

headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
}

bot = Bot(TOKEN)
dp = Dispatcher(bot)

async def on_startup(_): # Бот запу..стился
    print('Я запустился =)')


# Начало работы
@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text="Погода сейчас", callback_data="cur_weather"),
               types.InlineKeyboardButton(text="Погода на 14 дней", callback_data="week_weath")]
    keyboard.add(*buttons)
    await message.answer("Нажмите на кнопку, чтобы узнать погоду.", reply_markup=keyboard)


# Погода сейчас
@dp.callback_query_handler(text="cur_weather")
async def send_weather(call: types.CallbackQuery):
    await call.message.answer((current_weather(url, headers)))


# Погода на 14 дней
@dp.callback_query_handler(text="week_weath")
async def send_week_weather(call: types.CallbackQuery):
    await call.message.answer("".join((week_weather(url2, headers))))
    photo = InputFile('image.png')
    await call.message.answer_photo(photo)
    os.remove('image.png')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=on_startup)