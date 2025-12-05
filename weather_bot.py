import os
import requests
import telebot
from telebot import types
from dotenv import load_dotenv
import time
import logging

# Завантажуємо змінні оточення з .env файлу
load_dotenv()

# Отримання токенів та ключів
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

# --- Налаштування логування ---
LOG_FILE = 'app.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
# --- Кінець Налаштування Логування ---

# Ініціалізація бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Конфігурація
AVAILABLE_CITIES = ["Kyiv", "Dnipro", "Lviv", "Uzhhorod", "Berlin"]
OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- Реалізація Кешування ---
WEATHER_CACHE = {}
CACHE_DURATION = 10 * 60  # 10 хвилин у секундах


# --- Кінець Реалізації Кешування ---


def get_weather_data(city: str) -> dict or None:
    """
    Отримує дані про погоду для вказаного міста, використовуючи кешування.
    """
    if city in WEATHER_CACHE:
        cache_entry = WEATHER_CACHE[city]
        if (time.time() - cache_entry['timestamp']) < CACHE_DURATION:
            logger.info(f"CACHE HIT: Погода для {city} отримана з кешу.")
            return cache_entry['data']
        else:
            logger.info(f"CACHE EXPIRED: Погода для {city} застарів. Запит до API.")

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ua'
    }

    try:
        start_time = time.time()
        response = requests.get(OPENWEATHERMAP_URL, params=params)
        end_time = time.time()
        duration = end_time - start_time
        if response.status_code == 200:
            data = response.json()
            WEATHER_CACHE[city] = {'timestamp': time.time(), 'data': data}
            logger.info(f"API SUCCESS: Погода для {city} (час виконання: {duration:.2f}секунд. Дані оновлено в кеші.")
            return data
        else:
            logger.error(f"API FAILURE: Помилка API для {city}: Статус {response.status_code}.")
            return None
    except requests.exceptions.RequestException as error:
        print(f"Помилка з'єднання: {error}")
        return None


def format_weather_message(data: dict) -> str:
    """
    Форматує сирі дані про погоду в читабельне повідомлення.
    """
    if not data:
        return "Не вдалося отримати дані про погоду."

    city_name = data.get('name', 'Невідоме місто')
    temp = round(data['main']['temp'])
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']

    message = (
        f"📍 Погода в місті {city_name}:\n"
        f"🌡️ Температура: {temp}°C\n"
        f"💧 Вологість: {humidity}%\n"
        f"☁️ Опис: {description.capitalize()}"
    )

    return message


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Обробляє команду /start. Створює кнопки міст
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for city in AVAILABLE_CITIES:
        markup.add(types.KeyboardButton(city))

    bot.send_message(
        message.chat.id,
        "👋 Привіт! Я бот-синоптик. Обери місто зі списку нижче, щоб отримати актуальний прогноз погоди:\n\n"
        "Спробуй команду /help, щоб дізнатися більше про мене.",
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    """
    Обробляє команду /help. Надсилає довідкову інформацію.
    """
    help_message = (
        "📖 *Доступні команди:*\n\n"
        "/start - Розпочати роботу з ботом та показати кнопки вибору міст.\n"
        "/help - Показати цей список команд.\n\n"
        "*Вибір міста:*\n"
        "Просто оберіть одне з міст, доступних на кнопках: "
        f"*{', '.join(AVAILABLE_CITIES)}*. Я покажу актуальну погоду, використовуючи кешовані дані (оновлюються кожні 10 хвилин)."
    )
    bot.send_message(
        message.chat.id,
        help_message,
        parse_mode='Markdown',
    )


@bot.message_handler(content_types=['text'])
def handle_city_request(message):
    """
    Обробляє текстові повідомлення користувача (вибір міста).
    """
    city_name = message.text.strip()

    if city_name in AVAILABLE_CITIES:
        weather_data = get_weather_data(city_name)
        weather_report = format_weather_message(weather_data)
        bot.send_message(message.chat.id, weather_report, parse_mode='Markdown')

    else:
        bot.send_message(
            message.chat.id,
            "Будь ласка, обери місто зі списку, використовуючи кнопки нижче, або скористайся командою /start."
        )


if __name__ == '__main__':
    logger.info("Бот запущено. Для зупинки натисніть Ctrl+C.")
    try:
        bot.polling(none_stop=True)
    except Exception as ex:
        logger.critical(f"Критична помилка під час роботи бота: {ex}")
