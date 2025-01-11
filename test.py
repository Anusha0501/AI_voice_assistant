import os
import datetime
import random
import speech_recognition as sr
import pvporcupine
from pvrecorder import PvRecorder
import requests
import time
import pywhatkit
import vlc
from threading import Thread

weather_api_key = "enter your api_key"
news_api_key = "enter your api_key"
ACCESS_KEY = "+TozAJkNJYIzoB5O7Xgz5K2NuYpJhEu62tN5xhsi4kx3E+sDf5kKeQ=="
KEYWORD_PATH = "Worcestershire_en_mac_v3_0_0.ppn"

current_player = None
current_track_index = 0
music_files = []

def say(text):
    os.system(f"say '{text}'")


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
        print("Listening for your command...")
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": weather_api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        if weather_data.get("cod") != "404":
            main = weather_data.get("main", {})
            temperature = main.get("temp", "N/A")
            pressure = main.get("pressure", "N/A")
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
                    say(f"Headline {i + 1}: {title}")
                    time.sleep(1)
            else:
                say("No news articles found.")
        else:
            say("Error fetching news. Please check your API key or try again later.")
    except requests.exceptions.RequestException as e:
        say(f"Error fetching news: {str(e)}")


def play_music(music_path):
    global current_player, current_track_index, music_files

    def _play():
        global current_player, current_track_index, music_files
        try:
            music_files = [f for f in os.listdir(music_path) if f.endswith(('.mp3', '.wav', '.flac'))]
            if not music_files:
                say("No music files found in the directory.")
                return

            if current_track_index >= len(music_files):
                current_track_index = 0  # Reset to first track if index is out of bounds

            music_file = music_files[current_track_index]
            full_path = os.path.join(music_path, music_file)
            say(f"Playing {music_file}")
            current_player = vlc.MediaPlayer(full_path)
            current_player.play()
            time.sleep(2)
            while current_player.is_playing():
                time.sleep(1)
        except Exception as e:
            say(f"Error playing music: {str(e)}")

    music_thread = Thread(target=_play, daemon=True)
    music_thread.start()

def pause_music():
    global current_player
    if current_player:
        state = current_player.get_state()  # Get the current state of the player
        print(f"Current player state: {state}")  # Debugging log
        if state == vlc.State.Playing:  # Check if the player is playing
            current_player.pause()
            say("Music paused.")
        elif state == vlc.State.Paused:  # Handle case where music is already paused
            say("Music is already paused.")
        else:  # Handle other states like Stopped or Ended
            say("No music is currently playing.")
    else:
        say("No music is currently playing.")


def resume_music():
    global current_player
    if current_player and not current_player.is_playing():
        current_player.play()
        say("Resuming music.")
    else:
        say("No music is currently paused.")


def next_track():
    global current_track_index, current_player, music_files

    if not music_files:
        say("No music files found in the directory.")
        return

    # Stop the current track if playing
    if current_player:
        state = current_player.get_state()
        print(f"Current player state before next track: {state}")  # Debugging log
        if state in [vlc.State.Playing, vlc.State.Paused]:
            current_player.stop()
            say("Stopping current track.")

    # Move to the next track
    current_track_index += 1
    if current_track_index >= len(music_files):
        current_track_index = 0  # Loop back to the first track

    # Play the next track
    next_music_path = "/Users/anantupadhiyay/Documents/music"
    say(f"Playing next track: {music_files[current_track_index]}")
    play_music(next_music_path)


def process_command(query):
    global current_player
    if current_player and current_player.is_playing():
        current_player.stop()
        say("Stopping current music.")

    query_lower = query.lower()
    apps = [["WhatsApp", "WhatsApp.app"], ["Excel", "Microsoft Excel.app"], ["Browser", "Microsoft Edge.app"]]

    for app in apps:
        if f"open {app[0].lower()}" in query_lower:
            say(f"Opening {app[0]}. Please wait a moment.")
            os.system(f"open -a '/Applications/{app[1]}'")
            return

    if "weather" in query_lower:
        say("Please tell me the city name.")
        city = takeCommand()
        if city:
            get_weather(city)
    elif "news" in query_lower:
        get_news()
    elif "play music" in query_lower:
        music_path = "/Users/anantupadhiyay/Documents/music"
        play_music(music_path)
    elif "pause music" in query_lower:
        pause_music()
    elif "resume music" in query_lower:
        resume_music()
    elif "next music" in query_lower or "next song" in query_lower:
        next_track()
    elif "time" in query_lower:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"The time is {current_time}")
    elif "play video" in query_lower:
        song = query.replace('play', '').strip()
        say(f'Playing {song} on YouTube.')
        pywhatkit.playonyt(song)
    else:
        say("Sorry, I couldn't process that request.")


def hotword_listener():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD_PATH]
    )
    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
    recorder.start()
    print("Listening for the wake word 'assistant'...")

    try:
        while True:
            pcm = recorder.read()
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected!")
                say("How may I assist you?")

                query = takeCommand()
                if query:
                    if "exit" in query.lower() or "stop now" in query.lower():
                        say("Goodbye!")
                        break
                    process_command(query)
    except KeyboardInterrupt:
        print("Assistant stopped by user.")
    finally:
        recorder.stop()
        recorder.delete()
        porcupine.delete()


if __name__ == "__main__":
    print("Initializing your Personal Assistant.")
    wishme()
    hotword_listener()
