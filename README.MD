# 🌦️ Telegram Weather Bot

A Telegram bot that provides weather information for specified cities using the OpenWeatherMap API. It caches weather data to minimize API calls and presents the information in a user-friendly format. This bot allows users to quickly get current weather conditions for a list of predefined cities directly in Telegram.

## 📝Table of Contents

1. [🚀 Key Features](#-key-features)
2. [🛠️ Technology Stack](#-technology-stack)
3. [📦 Getting Started](#-getting-started)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Local Launch](#local-launch)
4. [💻 Usage](#-usage)
5. [📂 Project Structure](#-project-structure)

## 🚀 Key Features

- **Getting Weather Data:** Loads real-time weather data from the OpenWeatherMap API.
- **Caching Mechanism:** Implements a caching system to reduce API calls and improve response time. Weather data is stored for a specified amount of time (```CACHE_DURATION```).
- **User-friendly Interface:** Provides a simple and intuitive Telegram interface with command-based interaction.
- **Inline Keyboard:** Uses the inline keyboard for easy city selection.
- **Error Handling:** Robust error handling for API requests and connection issues.
- **Logging:** Comprehensive logging of application events and errors for monitoring and debugging.
- **Configuration Via Environment Variables:** Uses environment variables for sensitive information such as API keys and bot tokens.
- **Available Cities:** A predefined list of cities for which weather information can be retrieved.

## 🛠️ Technology Stack

- **Programming Language:** Python
- **Telegram Bot API:** `telebot` (pyTelegramBotAPI)
- **HTTP Requests:** `requests`
- **Environment Variables:** `dotenv`
- **Operating System:** Platform Independent
- **API:** OpenWeatherMap API
- **Logging:** `logging` Module
- **Other:** `os`, `time`

## 📦 Getting Started

### Prerequisites

- Python 3.6 or higher
- Telegram account
- OpenWeatherMap API Key (You can get it for free at [OpenWeatherMap](https://openweathermap.org/))
- Telegram Bot Token (You can create a bot and get a token at [BotFather](https://t.me/botfather) in Telegram)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Freelancerm/homework29.git
cd homework29
```

2. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate # On Linux/macOS
venv\Scripts\activate # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your API key and bot token:

```
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
API_KEY=YOUR_OPENWEATHERMAP_API_KEY
```

Replace `YOUR_TELEGRAM_BOT_TOKEN` and `YOUR_OPENWEATHERMAP_API_KEY` with your actual tokens.

### Local Launch

1. Start the bot:

```bash
python weather_bot.py
```

2. Start the bot in Telegram by sending the command `/start`.

## 💻 Usage

1. Send the command `/start` to the bot to receive a welcome message.
2. Send the command `/help` to see a list of available commands.
3. Select a city from the built-in keyboard to get weather information.

## 📂 Project Structure

```
├── weather_bot.py # The main script for the Telegram weather bot
├── requirements.txt # Python dependency list
├── .env # Environment variables (API keys, tokens)
├── app.log # Log file for application events and errors
└── README.md # Project documentation (this file)
```