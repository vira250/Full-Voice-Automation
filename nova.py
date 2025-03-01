import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import re  
import tkinter as tk
from tkinter import Label, Text, Scrollbar, END, Frame, BOTH, Button, PhotoImage
from datetime import datetime
import time

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

user_name = "User"

# Speak function
def speak(audio):
    chat_box.insert(END, "NOVA: ", "nova")  # Start typing effect
    root.update()
    
    for letter in audio:
        chat_box.insert(END, letter, "nova")
        root.update()
        time.sleep(0.02)  # Adjust typing speed (lower = faster)
    
    chat_box.insert(END, "\n")  # Move to the next line
    chat_box.yview(END)
    
    engine.say(audio)
    engine.runAndWait()


# Take voice command
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...", fg="green")
        root.update()
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-IN').lower()
            chat_box.insert(END, f"You: {query}\n", "user")
            smooth_scroll()  # 🔥 Call smooth scrolling
            return query
        except sr.UnknownValueError:
            return "None"
        except sr.RequestError:
            speak("Sorry, I couldn't connect to Google services.")
            return "None"



def smooth_scroll():
    chat_box.yview_moveto(1.0)  # Move to the bottom gradually
    root.update_idletasks()
    root.after(10, smooth_scroll)  # Keep running every 10ms


# Ask for user's name
def get_user_name():
    global user_name
    speak("What should I call you?")
    name = takecommand()
    if name and name != "None":
        user_name = name.capitalize()
        speak(f"Alright, I will call you {user_name}.")
        #chat_box.insert(END, f"NOVA: Alright, I will call you {user_name}.\n", "nova")

# Wishing function
def wishme():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        speak(f"Good Morning {user_name}")
    elif 12 <= hour < 18:
        speak(f"Good Afternoon {user_name}")
    elif 18 <= hour < 24:
        speak(f"Good Evening {user_name}")
    speak("Say 'hey nova' to activate me.")

# Perform tasks based on command
def perform_task(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    elif 'open google' in query:
        webbrowser.open("https://www.google.com")
    elif 'play music' in query:
        music_dir = "C:\\Users\\Public\\Music"
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
    elif 'send email' in query:
        speak("Who should I send the email to?")
    else:
        speak("I'm not sure how to do that.")
    ask_for_more()

# Ask if user needs anything else
def ask_for_more():
    speak("Do you need anything else?")  # ✅ This already prints in `chat_box`
    
    response = takecommand().strip()
    if any(word in response for word in ["yes", "yeah", "sure", "okay", "yup", "of course"]):
        speak("Okay, what do you need?")
        command = takecommand()
        if command != "None":
            perform_task(command)
    else:
        speak("Okay, I'll be here when you need me. Just say 'Nova'.")
        listen_for_activation()


# Listen for activation command
def listen_for_activation():
    while True:
        query = takecommand()
        if any(word in query for word in ["hey nova", "hi nova", "yo nova", "nova", "sup nova"]):
            speak("Yes? How can I help?")  # ✅ No need to insert separately
            command = takecommand()
            if command != "None":
                perform_task(command)


# Toggle light/dark mode
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = "#2C2F33" if dark_mode else "white"
    text_color = "white" if dark_mode else "black"
    nova_color = "pink" if dark_mode else "green"

    root.configure(bg=bg_color)
    frame.configure(bg=bg_color)
    chat_box.configure(bg=bg_color, fg=text_color)
    chat_box.tag_config("nova", foreground=nova_color)
    chat_box.tag_config("user", foreground=text_color)  # ✅ Ensures user text matches theme
    status_label.configure(bg=bg_color, fg=text_color)
    theme_button.config(bg=bg_color, activebackground=bg_color)
    header_label.config(bg=bg_color, fg=text_color)  # ✅ Matches the background


# Create UI
root = tk.Tk()
root.title("NOVA - Voice Assistant")
root.geometry("700x550")

# Load icons
sun_icon = PhotoImage(file="sun.png")
moon_icon = PhotoImage(file="moon.png")

dark_mode = False  

# Header label with transparent background
header_label = Label(root, text="NOVA - Voice Assistant", font=("Arial", 14, "bold"), bd=0, highlightthickness=0)
header_label.pack(pady=5)

frame = Frame(root, bg="white")
frame.pack(padx=10, pady=5, fill=BOTH, expand=True)

chat_box = Text(frame, wrap="word", height=20, width=70, font=("Arial", 12), bg="white", fg="black")
scrollbar = Scrollbar(frame, command=chat_box.yview)
chat_box.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
chat_box.pack(side="left", fill="both", expand=True)
chat_box.tag_config("user", foreground="black")
chat_box.tag_config("nova", foreground="green") 
welcome_message = "Hey there! I'm NOVA, your personal assistant."
speak(welcome_message)


status_label = Label(root, text="Waiting for activation...", font=("Arial", 12), bg="white", fg="black")
status_label.pack(pady=10)

# Smaller and transparent toggle button
theme_button = Button(root, image=moon_icon, command=toggle_theme, bd=0, bg=root.cget("bg"), activebackground=root.cget("bg"))
theme_button.config(width=25, height=25)  # Adjust size
theme_button.place(relx=0.95, rely=0.02, anchor="ne")

# Main assistant loop
def assistant_loop():
    get_user_name()
    wishme()
    listen_for_activation()


root.after(1000, assistant_loop)
root.mainloop()
