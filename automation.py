
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import tkinter as tk
from tkinter import Label
from datetime import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.now().hour)
    if 8 <= hour < 12:
        speak("Good Morning my dear friend")
    elif 12 <= hour < 18:
        speak("Good Afternoon my dear friend")
    elif 18 <= hour < 22:
        speak("Good Evening my dear friend")
    speak("Say 'assistant' to activate me.")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening for the keyword...")
        root.update()
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in').lower()
            if "assistant" in query:
                status_label.config(text="Keyword detected, now listening...")
                root.update()
                speak("Yes, I am listening")
                audio = r.listen(source)
                query = r.recognize_google(audio, language='en-in')
                status_label.config(text=f"You said: {query}")
                root.update()
                return query.lower()
            else:
                return "None"
        except Exception as e:
            return "None"

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("jviraj666@gmail.com", "tampsnwwyxfimhki")
        server.sendmail("jviraj666@gmail.com", to, content)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(e)
        speak('Sorry, I am unable to send this email')

def perform_task(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    elif 'open notepad' in query:
        os.startfile("C:\\Windows\\System32\\notepad.exe")
    elif 'open calculator' in query:
        os.startfile("calc.exe")
    elif 'open command prompt' in query:
        os.system("start cmd")
    elif 'open file explorer' in query:
        os.system("explorer")
    elif 'shutdown system' in query:
        os.system("shutdown /s /t 1")
    elif 'restart system' in query:
        os.system("shutdown /r /t 1")
    elif 'lock system' in query:
        os.system("rundll32.exe user32.dll,LockWorkStation")
    elif 'play music' in query:
        music_dir = "C:\\Users\\Public\\Music"
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com/")
    elif 'open google' in query:
        webbrowser.open("https://www.google.com/")
    elif 'search google' in query:
        speak("What should I search for?")
        search_query = takecommand()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    elif 'tell me the time' in query:
        speak(f"The time is {datetime.now().strftime('%H:%M:%S')}")
    elif 'send email' in query:
        try:
            speak("Who should I send the email to?")
            to = takecommand()
            to = to.replace(" at ", "@").replace(" dot ", ".")  # Convert spoken email format
            speak("What is the message?")
            content = takecommand()
            sendEmail(to, content)
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't send the email.")
    elif 'exit' in query or 'stop' in query:
        speak("Goodbye my friend!")
        root.quit()
    else:
        speak("I didn't understand. Can you please repeat?")

def assistant_loop():
    while True:
        query = takecommand()
        if query != "None":
            perform_task(query)

# Creating UI
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("400x300")

label = Label(root, text="Voice Assistant", font=("Arial", 16))
label.pack(pady=20)

status_label = Label(root, text="Waiting for activation...", font=("Arial", 12))
status_label.pack(pady=10)

wishme()

# Run assistant loop continuously
root.after(1000, assistant_loop)

root.mainloop()

