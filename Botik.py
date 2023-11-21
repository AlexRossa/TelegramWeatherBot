import requests
import telebot
from datetime import datetime
import config

#Replace with your Telegram bot token
bot = telebot.TeleBot(config.TELEGRAM_API_KEY)
gacci = int

#OpenWeatherMap API key
api_key = config.WEATHER_API_KEY

#Emojis for the description of the weather
weather_emojis = {
    'clear sky': '☀️',
    'few clouds': '🌤️',
    'scattered clouds': '⛅',
    'broken clouds': '☁️',
    'overcast clouds': '☁',
    'shower rain': '🌦️',
    'rain': '🌧️',
    'thunderstorm': '⛈️',
    'snow': '❄️',
    'mist': '🌫️'
}

#Function to fetch weather data from OpenWeatherMap API
def get_weather_data(city_name):
    #Construct API URL
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

    #Send GET request to API
    response = requests.get(url)

    #Check if request was successful
    if response.status_code == 200:
        #Parse JSON data
        data = response.json()
        #Extract weather information
        weather_data = {
            'temperature': data['main']['temp'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'time': datetime.now().strftime('%H:%M')
        }
        return weather_data
    else:
        return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Type /weather <city> to get the current weather.")

#Handle incoming messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    #Check if message is a command
    if message.text.startswith('/weather'):
        #Extract city name from command
        city_name = message.text.split()[1]
        #Retrieve weather data for the city
        weather_data = get_weather_data(city_name)
        
        #Check if weather data was retrieved successfully
        if weather_data:
            emoji = weather_emojis.get(weather_data['description'])
            #Format weather message
            weather_message = f"Current weather in {city_name}:\n\n" \
                f"{emoji} Description: {weather_data['description']}\n" \
                f"🌡 Temperature: {weather_data['temperature']}°C\n" \
                f"💨 Wind speed: {weather_data['wind_speed']} m/s\n" \
                f"⏰ Time: {weather_data['time']}"
            #Reply to the message of user
            bot.reply_to(message, weather_message)
        else:
            #Send error message
            bot.reply_to(message, "Invalid city name. Please try again.")
bot.polling()
