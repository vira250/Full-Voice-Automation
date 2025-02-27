
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import re  # For email validation
import tkinter as tk
from tkinter import Label
from datetime import datetime
import random

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

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
    speak("Say ' hey sage' to activate me.")

def update_wave():
    if canvas.winfo_exists():
        canvas.delete("all")
        for i in range(10):
            height = random.randint(5, 30)
            canvas.create_rectangle(i * 20 + 10, 40 - height, i * 20 + 25, 40 + height, fill='blue')
        root.update_idletasks()
        root.after(100, update_wave)

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        root.update()
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            # Recognize in both English and Marathi
            query_en = r.recognize_google(audio, language='en-IN').lower()
            query_mr = r.recognize_google(audio, language='mr-IN').lower()
            print(f"My dear friend you said: {query_en}\n")
            # Return the most confident result
            return query_en if query_en else query_mr

        except sr.UnknownValueError:
            return "None"
        except sr.RequestError:
            speak("Sorry, I couldn't connect to Google services.")
            return "None"

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("jviraj666@gmail.com", "whhjhqatxyaejbrc")  # Avoid hardcoding credentials in real applications
        server.sendmail("jviraj666@gmail.com", to, content)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(e)
        speak('Sorry, I am unable to send this email.')

def get_email_from_voice():
    while True:
        speak("Who should I send the email to?")
        email_input = takecommand()

        if email_input == "None" or email_input.strip() == "":
            speak("I couldn't hear you properly. Please repeat.")
            continue

        email_corrected = (
            email_input.replace(" at ", "@")
            .replace(" dot ", ".")
            .replace(" underscore ", "_")
            .replace(" hyphen ", "-")
            .replace(" space ", "")
            .replace(" ", "")
        )

        if re.match(r"[^@]+@[^@]+\.[^@]+", email_corrected):
            return email_corrected
        else:
            speak("The email ID was not recognized correctly. Please try again.")

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
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
        else:
            speak("No music files found.")

    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com/")

    elif 'open google' in query:
        webbrowser.open("https://www.google.com/")

    elif 'search google' in query:
        speak("What should I search for?")
        search_query = takecommand()

        if search_query == "None" or search_query.strip() == "":
            speak("I didn't hear that properly. Please try again.")
            search_query = takecommand()

        if search_query and search_query != "None":
            url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            webbrowser.open(url)
            speak(f"Searching Google for {search_query}")
        else:
            speak("Sorry, I couldn't capture your search query.")

    elif 'tell me the time' in query:
        speak(f"The time is {datetime.now().strftime('%H:%M:%S')}")

    elif 'send email' in query:
        try:
            to = get_email_from_voice()
            speak("What is the message?")
            content = takecommand()

            if content == "None" or content.strip() == "":
                speak("I couldn't hear the message. Please repeat.")
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
        if query != "None" and " hey sage" in query or " hey sayj" in query or " hey saaj" in query or "passage" in query:
            speak("Yes, I am listening")
            command = takecommand()
            if command != "None":
                perform_task(command)

# Creating UI
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("400x300")

label = Label(root, text="Voice Assistant", font=("Arial", 16))
label.pack(pady=20)

status_label = Label(root, text="Waiting for activation...", font=("Arial", 12))
status_label.pack(pady=10)

canvas = tk.Canvas(root, width=200, height=80, bg="white")
canvas.pack(pady=10)
update_wave()

wishme()

# Run assistant loop continuously
root.after(1000, assistant_loop)

root.mainloop()
