import datetime
import speech_recognition as sr
import os
import webbrowser
import requests
import time
import pywhatkit
import google.generativeai as gpt

gpt.configure(api_key="enter your api key for gpt config google api key")
model = gpt.GenerativeModel("gemini-1.5-flash")
weather_api_key = "enter your api key"
news_api_key = "enter your api key"

import pyttsx3

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        say("Good Morning! Sir")
    elif 12 <= hour < 18:
        say("Good Afternoon! Sir")
    else:
        say("Good Evening! Sir")
    say("Please tell me how I may help you.")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            say("Sorry, I could not understand the audio. Please try again.")
            return takeCommand()
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return "There was an issue connecting to the speech service."
        except Exception as e:
            print(f"An error occurred: {e}")
            return "An error occurred. Please try again."



def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        if weather_data.get("cod") != "404":
            main = weather_data.get("main", {})
            temperature = main.get("temp", "N/A")
            pressure = main.get("pressure", "N/A")
            humidity = main.get("humidity", "N/A")
            weather = weather_data.get("weather", [{}])[0].get("description", "N/A")
            say(f"Temperature in {city} is {temperature:.2f} degrees Celsius.")
            say(f"Pressure is {pressure} hPa.")
            say(f"Weather is {weather}.")
        else:
            say("City not found.")
    except requests.exceptions.RequestException as e:
        say(f"Error fetching weather information: {str(e)}")


def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        if news_data.get("status") == "ok":
            articles = news_data.get("articles", [])
            if articles:
                say("Here are the top news headlines:")
                for i, article in enumerate(articles[:2]):
                    title = article.get("title", "No title available")
                    description = article.get("description", "No description available")
                    say(f"Headline {i + 1}: {title}")
                    say(f"Description: {description}")
                    time.sleep(1)
            else:
                say("No news articles found.")
        else:
            say("Error fetching news. Please check your API key or try again later.")
    except requests.exceptions.RequestException as e:
        say(f"Error fetching news: {str(e)}")


def process_command_with_gemini(query):
    if "weather" in query.lower():
        say("Please tell me the city name.")
        city = takeCommand()
        if city:
            get_weather(city)
        return
    elif "news" in query.lower():
        get_news()
        return
    elif "play" in query.lower():
        song = query.replace('play', '').strip()
        say(f'Playing {song} on YouTube.')
        pywhatkit.playonyt(song)
        return
    elif "time" in query.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"The time is {current_time}")
        return
    response = model.generate_content(f"{query}")
    gemini_response = response.text.strip()
    print(gemini_response)
    say(gemini_response)

if __name__ == "__main__":
    print("Initializing your Personal Assistant.")
    wishme()

    while True:
        query = takeCommand()
        if "exit" in query.lower() or "stop" in query.lower():
            say("Goodbye!")
            print("Exiting the assistant.")
            break
        process_command_with_gemini(query)
