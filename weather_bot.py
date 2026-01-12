import os
import requests
import telebot
from telebot import types
from dotenv import load_dotenv
import time
import logging

# Loading environment variables from the .env file
load_dotenv()

# Getting tokens and keys
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
API_KEY = os.getenv('API_KEY')

# --- Logging settings ---
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
# --- End of Logging Settings ---

# Bot initialization
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Configuration
AVAILABLE_CITIES = ["Kyiv", "Dnipro", "Lviv", "Uzhhorod", "Berlin"]
OPENWEATHERMAP_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- Caching Implementation ---
WEATHER_CACHE = {}
CACHE_DURATION = 10 * 60  # 10 minutes in seconds


# --- End of Caching Implementation ---


def get_weather_data(city: str) -> dict or None:
    """
    Gets weather data for the specified city using caching.
    """
    if city in WEATHER_CACHE:
        cache_entry = WEATHER_CACHE[city]
        if (time.time() - cache_entry['timestamp']) < CACHE_DURATION:
            logger.info(f"CACHE HIT: Weather for {city} retrieved from cache.")
            return cache_entry['data']
        else:
            logger.info(f"CACHE EXPIRED: Weather for {city} is out of date. Request to API.")

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
            logger.info(f"API SUCCESS: Weather for {city} (run time: {duration:.2f} seconds. Data refreshed in cache.")
            return data
        else:
            logger.error(f"API FAILURE: API error for {city}: Status {response.status_code}.")
            return None
    except requests.exceptions.RequestException as error:
        print(f"Connection error: {error}")
        return None


def format_weather_message(data: dict) -> str:
    """
    Formats raw weather data into a readable message.
    """
    if not data:
        return "Failed to retrieve weather data."

    city_name = data.get('name', 'Unknown city')
    temp = round(data['main']['temp'])
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']

    message = (
        f"📍 Weather in city {city_name}:\n"
        f"🌡️ Temperature: {temp}°C\n"
        f"💧 Humidity: {humidity}%\n"
        f"☁️ Describe: {description.capitalize()}"
    )

    return message


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Processes the /start command. Creates cities buttons
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for city in AVAILABLE_CITIES:
        markup.add(types.KeyboardButton(city))

    bot.send_message(
        message.chat.id,
        "👋Hello! I'm a weather bot. Select a city from the list below to get the latest weather forecast:\n\n"
                "Try the /help command to learn more about me.",
        reply_markup=markup
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    """ Processes the /help command. Sends help information. """
    help_message = (
        "📖 *Available commands:*\n\n"
        "/start - Start the bot and show the city selection buttons.\n"
        "/help - Show this list of commands.\n\n"
        "*City selection:*\n"
        "Simply choose one of the cities available on the buttons: "
        f"*{', '.join(AVAILABLE_CITIES)}*. I will show the current weather using cached data (updated every 10 minutes)."
    )
    bot.send_message(
        message.chat.id,
        help_message,
        parse_mode='Markdown',
    )


@bot.message_handler(content_types=['text'])
def handle_city_request(message):
    """
    Processes user text messages (city selection).
    """
    city_name = message.text.strip()

    if city_name in AVAILABLE_CITIES:
        weather_data = get_weather_data(city_name)
        weather_report = format_weather_message(weather_data)
        bot.send_message(message.chat.id, weather_report, parse_mode='Markdown')

    else:
        bot.send_message(
            message.chat.id,
            "Please select a city from the list using the buttons below, or use the /start command."
        )


if __name__ == '__main__':
    logger.info("Bot is running. Press Ctrl+C to stop.")
    try:
        bot.polling(none_stop=True)
    except Exception as ex:
        logger.critical(f"Critical error while running the bot: {ex}")
