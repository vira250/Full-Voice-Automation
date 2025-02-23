import pyttsx3
import speech_recognition as sr
from datetime import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyaudio
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.now().hour)
    """
    12:00 - noon
    1:00 pm - morning/13.00 - afternoon
    18:00 - evening
    """
    if hour>=8 and hour<12:
        speak("Good Morning my dear friend")
    elif hour>=12 and hour<18:
        speak("Good Afternoon my dear friend")
    elif hour>=18 and hour<22:
        speak("Good Evening my dear friend")

    speak("Let me know how can I help you today, what are you looking for?")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening to you my friend...")
        r.pause_threshold = 1
        audio = r.listen(source)


        try:
            print("Recognizing your voice...")
            query = r.recognize_google(audio, language='en-in')
            print(f"My dear friend you said: {query}\n")

        except Exception as e:
            print("can you say that again please...")
            return "None"
        return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("jviraj666@gmail.com", "tampsnwwyxfimhki")
    server.sendmail("jadhavviraj112@gmail.com", to, content)
    server.close()

if __name__ == "__main__":
    wishme()

    while True:
        query = takecommand().lower()

        if 'open wikipedia' in query:
            speak("Opening Wikipedia for you my friend...")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        

        if 'open notepad' in query:
            npath= "C:\\Windows\\System32\\notepad.exe"
            os.startfile(npath)
            speak("Notepad is open my friend...")

        elif 'open paint' in query:
            npath = "C:\\Users\\viraj\\AppData\\Local\\Microsoft\\WindowsApps\\mspaint.exe"
            os.startfile(npath)
            speak("Paint is open my friend...")

        elif 'open youtube' in query:
            webbrowser.open('https://www.youtube.com/')
            speak("Opening YouTube for you my friend...")

        elif 'open google' in query:
            webbrowser.open('www.google.com')
            speak("Opening Google for you my friend...")

        elif 'tell me the time' in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'email to other friend' in query:
            try:
                speak("What should I send?")
                content = takecommand()
                to = "jadhavviraj112@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent successfully!")

            except Exception as e:
                print(e)
                speak('My dear friend... i am unable to send this email')