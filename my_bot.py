import datetime
import telebot
from telebot import types
import random
import requests
import json

# ========== ТОКЕНЫ ==========
TOKEN = '7970948638:AAHGjFGdDHm1bb3TNut5s2WOfpXuBbZ3mgI'
WEATHER_API_KEY = '1a29c4a0251face4e3c04056d33751ee'  # Вставьте сюда ключ!

bot = telebot.TeleBot(TOKEN)

# ========== ФУНКЦИЯ ДЛЯ ПОГОДЫ ==========

def get_weather(city):
    """Получает погоду для указанного города"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            city_name = data['name']
            
            return (
                f"🌍 Город: {city_name}\n"
                f"🌡️ Температура: {temp:.1f}°C (ощущается как {feels_like:.1f}°C)\n"
                f"💧 Влажность: {humidity}%\n"
                f"🌤️ Описание: {description.capitalize()}\n"
                f"💨 Ветер: {wind_speed:.1f} м/с"
            )
        elif response.status_code == 404:
            return f"❌ Город '{city}' не найден. Проверьте название."
        else:
            return f"❌ Ошибка API: {data.get('message', 'Неизвестная ошибка')}"
            
    except requests.exceptions.Timeout:
        return "⏰ Превышено время ожидания. Попробуйте позже."
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

# ========== КОМАНДЫ ==========

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я бот с кнопками и погодой!\n"
        "Нажми /menu, чтобы увидеть меню."
    )
    show_menu(message)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(
        message,
        "📌 Доступные команды:\n"
        "/start - Приветствие\n"
        "/help - Помощь\n"
        "/menu - Показать меню с кнопками\n"
        "/time - Текущее время\n"
        "/date - Текущая дата\n"
        "/info - Информация о боте\n"
        "/weather <город> - Погода в городе\n"
        "Пример: /weather Москва"
    )

@bot.message_handler(commands=['time'])
def send_time(message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    bot.reply_to(message, f"🕒 Сейчас: {now}")

@bot.message_handler(commands=['date'])
def send_date(message):
    now = datetime.datetime.now().strftime("%d.%m.%Y")
    bot.reply_to(message, f"📅 Сегодня: {now}")

@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(
        message,
        "🤖 Я бот с погодой и кнопками\n"
        "📅 Создан: 2026 год\n"
        "💻 Технологии: Python, pyTelegramBotAPI, OpenWeatherMap API\n"
        "⚡ Быстро и стабильно!"
    )

# ========== ПОГОДА (команда) ==========

@bot.message_handler(commands=['weather'])
def handle_weather_command(message):
    # Разбираем команду: /weather Москва
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        bot.reply_to(
            message,
            "❓ Укажите город!\n"
            "Пример: /weather Москва\n"
            "Или нажмите кнопку '🌤️ Погода' и введите город."
        )
        return
    
    city = args[1]
    bot.send_chat_action(message.chat.id, 'typing')  # Показываем статус "печатает"
    
    weather_info = get_weather(city)
    bot.reply_to(message, weather_info)

# ========== МЕНЮ С КНОПКАМИ ==========

@bot.message_handler(commands=['menu'])
def show_menu(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn_time = types.KeyboardButton('🕒 Время')
    btn_date = types.KeyboardButton('📅 Дата')
    btn_info = types.KeyboardButton('ℹ️ Информация')
    btn_help = types.KeyboardButton('❓ Помощь')
    btn_good = types.KeyboardButton('😊 Комплимент')
    btn_weather = types.KeyboardButton('🌤️ Погода')
    
    keyboard.add(btn_time, btn_date, btn_info, btn_help, btn_good, btn_weather)
    
    bot.reply_to(
        message,
        "📋 Выберите действие:",
        reply_markup=keyboard
    )

# ========== ОБРАБОТКА КНОПОК ==========

@bot.message_handler(func=lambda message: message.text == '🕒 Время')
def handle_time(message):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    bot.reply_to(message, f"🕒 Текущее время: {now}")

@bot.message_handler(func=lambda message: message.text == '📅 Дата')
def handle_date(message):
    now = datetime.datetime.now().strftime("%d.%m.%Y")
    bot.reply_to(message, f"📅 Сегодня: {now}")

@bot.message_handler(func=lambda message: message.text == 'ℹ️ Информация')
def handle_info(message):
    bot.reply_to(
        message,
        "🤖 Бот с погодой и кнопками\n"
        "⚡ Быстро и стабильно\n"
        "🌤️ Нажми 'Погода', чтобы узнать прогноз"
    )

@bot.message_handler(func=lambda message: message.text == '❓ Помощь')
def handle_help(message):
    bot.reply_to(
        message,
        "📌 Команды:\n"
        "/start, /help, /menu, /time, /date, /info\n"
        "/weather <город> - погода"
    )

@bot.message_handler(func=lambda message: message.text == '😊 Комплимент')
def handle_compliment(message):
    compliments = [
        "Ты — молодец! 🌟",
        "У тебя всё получится! 💪",
        "Ты классный программист! 🚀",
        "Сегодня отличный день! ☀️",
        "Верь в себя! 😊",
        "Ты делаешь успехи! 📈",
        "Ты справишься с любой задачей! 🎯",
        "Твой код — это искусство! 🎨"
    ]
    bot.reply_to(message, random.choice(compliments))

# ========== ОБРАБОТКА ПОГОДЫ ЧЕРЕЗ КНОПКУ ==========

@bot.message_handler(func=lambda message: message.text == '🌤️ Погода')
def handle_weather_button(message):
    bot.reply_to(
        message,
        "🌤️ Введите название города, чтобы узнать погоду.\n"
        "Например: Москва, Санкт-Петербург, Лондон"
    )
    # Устанавливаем обработчик следующего сообщения
    bot.register_next_step_handler(message, process_weather_step)

def process_weather_step(message):
    city = message.text.strip()
    bot.send_chat_action(message.chat.id, 'typing')
    weather_info = get_weather(city)
    bot.reply_to(message, weather_info)

# ========== ОБРАБОТКА ОСТАЛЬНЫХ СООБЩЕНИЙ ==========

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    if message.text:
        # Игнорируем текст, который является названием кнопки
        if message.text in ['🕒 Время', '📅 Дата', 'ℹ️ Информация', '❓ Помощь', '😊 Комплимент', '🌤️ Погода']:
            return
        bot.reply_to(
            message, 
            f"Вы написали: {message.text}\n\n"
            "Нажми /menu, чтобы увидеть доступные команды и кнопки.\n"
            "Или /weather <город> для прогноза погоды."
        )
    else:
        bot.reply_to(message, "Я понимаю только текст 😅")

# ========== ЗАПУСК ==========

if __name__ == '__main__':
    print("=" * 40)
    print("🚀 Бот с погодой запущен!")
    print("📌 Токен:", TOKEN[:10] + "...")
    print("🌤️ Погода: включена")
    print("📋 Нажмите /menu в боте, чтобы увидеть кнопки")
    print("=" * 40)
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Ошибка: {e}")