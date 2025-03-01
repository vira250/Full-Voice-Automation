
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import re  # For email validation
import tkinter as tk
from tkinter import *
from datetime import datetime
import random
import time
import pywhatkit as kit
import pyautogui
import fnmatch

print(time.strftime("%H:%M:%S"))
# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

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

def get_user_name():
    global user_name
    speak("What should I call you?")
    name = takecommand()
    if name and name != "None":
        user_name = name.capitalize()
        speak(f"Alright, I will call you {user_name}.")


def wishme():
    hour = int(datetime.now().hour)
    if 0 <= hour < 12:
        speak(f"Good Morning {user_name}")
    elif 12 <= hour < 18:
        speak(f"Good Afternoon {user_name}")
    elif 18 <= hour < 23:
        speak(f"Good Evening {user_name}")
    else:
        speak(f"Hello {user_name}")

    speak("Say Nova to activate me.")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        root.update()
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
            query = r.recognize_google(audio, language='en-IN').lower()
            chat_box.insert(END, f"You: {query}\n", "user")
            # smooth_scroll()  # 🔥 Call smooth scrolling
            return query
    except sr.UnknownValueError:
            return "None"
    except sr.RequestError:
            speak("Sorry, I couldn't connect to Google services.")
            return "None"
# def smooth_scroll():
#     chat_box.yview_moveto(1.0)  # Move to the bottom gradually
#     root.update_idletasks()
#     root.after(10, smooth_scroll)  # Keep running every 10ms
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

def send_whatsapp_message():
    speak("Please say the recipient's phone number with country code.")
    phone_number = takecommand().replace(" ", "")  # Removing spaces

    if not phone_number.isdigit() or len(phone_number) < 10:
        speak("Invalid phone number. Please try again.")
        return

    speak("What message would you like to send?")
    message = takecommand()

    if message == "None" or message.strip() == "":
        speak("I couldn't hear your message properly. Please repeat.")
        message = takecommand()

    try:
        kit.sendwhatmsg_instantly(f"+{phone_number}", message)
        time.sleep(5)  # Wait for WhatsApp to open and type the message
        pyautogui.press("enter")  # Press Enter to send the message
        speak("Your message has been sent on WhatsApp.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the WhatsApp message.")

def play_youtube_song():
    speak("Which song would you like to play?")
    song_name = takecommand()

    if song_name == "None" or song_name.strip() == "":
        speak("I didn't hear that properly. Please repeat.")
        song_name = takecommand()

    if song_name and song_name != "None":
        speak(f"Playing {song_name} on YouTube.")
        kit.playonyt(song_name)  # Opens YouTube and plays the song
    else:
        speak("Sorry, I couldn't understand the song name.")

def find_and_open_file():
    speak("Which file do you want to search for?")
    
    while True:
        file_name = takecommand().lower().strip()
        
        if file_name == "none" or file_name == "":
            speak("I didn't catch that. Please say the file name again.")
            continue  # Ask again if input is invalid
        
        print(f"🔍 Searching for: {file_name}")  # Debugging print statement
        
        #Detect OneDrive Desktop path
        user_home = os.path.expanduser("~")
        desktop_path = os.path.join(user_home, "OneDrive", "Desktop")  # OneDrive Desktop
        documents_path = os.path.join(user_home, "OneDrive", "Documents")  # OneDrive Documents
        downloads_path = os.path.join(user_home, "Downloads")  # Normal Downloads
        
        #Limit search to OneDrive/Desktop, OneDrive/Documents, and Downloads
        search_directories = [desktop_path, documents_path, downloads_path]

        found_files = []
        file_extension = None

        #Check if user mentioned a file extension (like ".pdf" or ".txt")
        if "." in file_name:
            file_name, file_extension = file_name.split(".", 1)
            file_extension = "." + file_extension  # Add back the dot
        
        # Search in defined directories
        for directory in search_directories:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file_name in file.lower():
                            if file_extension:
                                if file.lower().endswith(file_extension):  # Match extension
                                    found_files.append(os.path.join(root, file))
                            else:
                                found_files.append(os.path.join(root, file))

        #Open the best match
        if found_files:
            print(f"Found: {found_files[0]}")  # Debugging output
            os.startfile(found_files[0])  # Open the first found file
            speak(f"Opening {file_name}")
            break  # Exit loop after opening file
        else:
            print("❌ File not found.")  # Debugging output
            speak("I couldn't find the file. Please try again.")
            break  # Exit if no file is found

def perform_task(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=30)
        speak("According to Wikipedia")
        speak(results)

    elif 'open notepad' in query:
        os.startfile("C:\\Windows\\System32\\notepad.exe")
        speak("opening notepad")

    elif 'open calculator' in query:
        os.startfile("calc.exe")
        speak("opening calculator")

    elif 'open command prompt' in query:
        os.system("start cmd")
        speak(" opening command prompt")
    elif 'open file explorer' in query:
        os.system("explorer")
        speak("opening file explorer")
    elif 'shutdown system' in query:
        os.system("shutdown /s /t 1")
        speak("shutting down the system")
    elif 'restart system' in query:
        os.system("shutdown /r /t 1")
        speak("restarting the system")

    elif 'lock system' in query:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        speak("locking the system")
    
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com/")
        speak("opening youtube")

    elif 'open google' in query:
        webbrowser.open("https://www.google.com/")
        speak("opening google")

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
            speak("opening search results in browser")
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

    elif 'send whatsapp message' in query:
        send_whatsapp_message()

    elif 'play song' in query or 'play song on youtube' in query:
        play_youtube_song()
    
    elif 'find file' in query:
        find_and_open_file()

    elif 'exit' in query or 'stop' in query:
        speak(f"Goodbye {user_name}")
        os._exit(0)
        root.quit()
    else:
        speak("I didn't understand. Can you please repeat?")
    ask_for_more()


def ask_for_more():
    speak("Do you need anything else?")  # ✅ This already prints in `chat_box`

    response = takecommand().strip().lower()
    if any(word in response for word in [ "yeah", "sure", "okay", "yup", "of course" , "yes" , "yes please" ]):
        speak("Okay, what do you need?")
        command = takecommand()
        if command != "None":
            perform_task(command)
    else:
        speak("Okay, I'll be here when you need me. Just say 'Nova'.")
        listen_for_activation()
    

def listen_for_activation():
    while True:
        query = takecommand()
        if any(word in query for word in ["nova"]):
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

def assistant_loop():
    get_user_name()
    wishme()
    listen_for_activation()

# Run assistant loop continuously
root.after(1000, assistant_loop)
root.mainloop()
