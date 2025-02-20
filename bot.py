from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.executor import start_polling
import requests

TOKEN = '7658310147:AAHYOOKsZBF4LVVe7ssUxOPOxGSXQnF_gGU'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Функция для отправки длинных сообщений
async def send_long_message(chat_id, text):
    max_length = 8192  # Telegram ограничение на длину сообщения
    for i in range(0, len(text), max_length):
        await bot.send_message(chat_id, text[i:i+max_length], parse_mode="Markdown")

# 🔹 Главное меню (Оставляем "Отчет за период" и "Итоговый отчет")
def create_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("📅 Отчет за период")
    btn2 = KeyboardButton("📊 Итоговый отчёт")
    markup.add(btn1, btn2)
    return markup

# 🔹 Клавиатура для "Отчет за период" (оставляем день, неделю, месяц)
def create_period_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("📆 День")
    btn2 = KeyboardButton("🗓 Неделя")
    btn3 = KeyboardButton("📅 Месяц")
    btn4 = KeyboardButton("🔙 Назад")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

# 🔹 Клавиатура для "Итогового отчета" (оставляем только "Выбрать диапазон дат")
def create_total_report_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("📅 Выбрать диапазон дат")
    btn2 = KeyboardButton("🔙 Назад")
    markup.add(btn1, btn2)
    return markup

# 🔹 Команда /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=create_main_menu())

# 🔹 Обработка кнопки "📅 Отчет за период"
@dp.message_handler(lambda message: message.text == "📅 Отчет за период")
async def report_period(message: types.Message):
    await message.answer("Выберите период:", reply_markup=create_period_keyboard())

# 🔹 Обработка кнопки "📊 Итоговый отчёт"
@dp.message_handler(lambda message: message.text == "📊 Итоговый отчёт")
async def select_total_report_period(message: types.Message):
    await message.answer("Выберите диапазон дат для итогового отчёта:", reply_markup=create_total_report_keyboard())

# 🔹 Генерация отчета по периоду (без кассира)
@dp.message_handler(lambda message: message.text in ["📆 День", "🗓 Неделя", "📅 Месяц"])
async def report_generate_period(message: types.Message):
    period_map = {
        "📆 День": "day",
        "🗓 Неделя": "week",
        "📅 Месяц": "month"
    }
    period = period_map[message.text]

    url = f'http://127.0.0.1:5000/generate_report_by_period/{period}'
    response = requests.get(url)

    await send_long_message(message.chat.id, response.text)

# 🔹 Обработчик выбора диапазона дат для итогового отчета
@dp.message_handler(lambda message: message.text == "📅 Выбрать диапазон дат")
async def ask_date_range(message: types.Message):
    await message.answer("Введите даты в формате: `YYYY-MM-DD - YYYY-MM-DD`", parse_mode="Markdown")

# 🔹 Генерация итогового отчёта за произвольный период
@dp.message_handler(lambda message: " - " in message.text)
async def send_custom_total_report(message: types.Message):
    try:
        start_date, end_date = message.text.split(" - ")
        url = f'http://127.0.0.1:5000/generate_total_report?start_date={start_date}&end_date={end_date}'
        response = requests.get(url)

        await send_long_message(message.chat.id, response.text)

    except ValueError:
        await message.answer("Ошибка! Введите даты в формате `YYYY-MM-DD - YYYY-MM-DD`.", parse_mode="Markdown")

# 🔹 Обработчик кнопки "🔙 Назад"
@dp.message_handler(lambda message: message.text == "🔙 Назад")
async def go_back_to_main_menu(message: types.Message):
    await message.answer("🔙 Возвращаемся в главное меню...", reply_markup=create_main_menu())

# 🔹 Запуск бота
if __name__ == '__main__':
    start_polling(dp, skip_updates=True)
