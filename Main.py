import speech_recognition as sr # type: ignore 
import webbrowser
import pyttsx3 # type: ignore
import Musiclibrary
import requests # type: ignore
#from openai import OpenAi
from gtts import gTTS # type: ignore

import os 
import pygame # type: ignore
# Initialize recognizer and text-to-speech engine

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "Use api key"
def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_new(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load your MP3 file
    pygame.mixer.music.load("temp.mp3")

    # Play the music
    pygame.mixer.music.play()

    # Keep the program running until the music stops
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    os.remove("temp.mp3")


# def aiprocess(command):
#     client = OpenAI(
#         api_key="use api key",
#     )
#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
#             {"role": "user", "content": command}
#         ]
#     )

#    return completion.choices[0].message.content

def process_command(c):
    command = c.lower()
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play") : 
        song = c.lower().split(" ")[1]
        link = Musiclibrary.Music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r= requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=use your api key here ")
        if r.status_code == 200:
            # Parse the JSON response
            news_data = r.json()

            # Extract the articles from the response
            articles = news_data.get('articles', [])

            for article in articles:
                speak(article['title'])

    else :
        # let OpenAi handle the request 
        # output = aiprocess(c)
        # speak(output)
        pass


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    while True:
        try:
            # Listen for the wake word "Jarvis"
            with sr.Microphone() as source:
                print("Listening ...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            command = recognizer.recognize_google(audio)
            if "jarvis" in command.lower():
                speak("Yes?")
                
                # Listen for the command after the wake word
                with sr.Microphone() as source:
                    print("Jarvis is active .... ")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                # Recognize and process the command
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")
                process_command(command)
        
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase.")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")