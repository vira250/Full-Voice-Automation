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
import requests
import pywhatkit as kit
import pyautogui
import subprocess
import platform
import json
from PIL import Image, ImageTk

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Default user name
user_name = "User"
user_data_file = "nova_user_data.json"

API_KEY = "YOUR_API_KEY"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
NEWS_API_KEY = "YOUR_API_KEY"

# Colors for the modern UI
DARK_BG = "#1E1E2E"
LIGHT_BG = "#F5F5F7"
ACCENT_COLOR = "#7B68EE"  # Purple accent
TEXT_COLOR_DARK = "#FFFFFF"
TEXT_COLOR_LIGHT = "#333333"
NOVA_TEXT_COLOR = "#7B68EE"  # Purple for NOVA's messages
USER_TEXT_COLOR = "#4A90E2"  # Blue for user's messages
BUTTON_COLOR = "#7B68EE"
BUTTON_TEXT_COLOR = "#FFFFFF"

# Theme state
dark_mode = False

# Function to save user data to JSON file
def save_user_data():
    data = {
        "user_name": user_name
    }
    try:
        with open(user_data_file, 'w') as file:
            json.dump(data, file)
        print(f"User data saved: {user_name}")
    except Exception as e:
        print(f"Error saving user data: {e}")

# Function to load user data from JSON file
def load_user_data():
    global user_name
    try:
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r') as file:
                data = json.load(file)
                user_name = data.get("user_name", "User")
                print(f"User data loaded: {user_name}")
                return True
        return False
    except Exception as e:
        print(f"Error loading user data: {e}")
        return False

# Speak function
def speak(audio):
    chat_box.insert(END, "NOVA: ", "nova_tag") 
    root.update()
    
    for letter in audio:
        chat_box.insert(END, letter, "nova")
        root.update()
        time.sleep(0.01)  # Slightly faster typing speed
    
    chat_box.insert(END, "\n")  
    chat_box.yview(END)
    
    engine.say(audio)
    engine.runAndWait()

# Dictionary mapping system applications to their execution commands
apps = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "command prompt": "cmd.exe",
    "file explorer": "explorer.exe",
    "task manager": "taskmgr.exe",
    "paint": "mspaint.exe",
    "wordpad": "write.exe",
    "media player": "wmplayer.exe",
    "control panel": "control.exe",
    "device manager": "devmgmt.msc",
    "disk cleanup": "cleanmgr.exe",
    "disk management": "diskmgmt.msc",
    "event viewer": "eventvwr.msc",
    "power options": "powercfg.cpl",
    "registry editor": "regedit.exe",
    "services": "services.msc",
    "system information": "msinfo32.exe",
    "task scheduler": "taskschd.msc",
    "windows security": "start windowsdefender:",
    "snipping tool": "snippingtool.exe",
    "settings": "start ms-settings:",
    "edge": "start msedge",
    "chrome": " start chrome",
    "firefox": "firefox.exe",
    "vlc": "vlc.exe",
}

def open_app(query):
    """Function to open system apps based on voice command"""
    for app in apps:
        if app in query:
            subprocess.run(apps[app], shell=True)
            return f"Opening {app}"
    return "Application not found!"

def get_definition(word):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            first_meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            return f"The definition of {word} is: {first_meaning}."
        else:
            return "Sorry, I couldn't find the definition for that word."
    except Exception as e:
        return "Something went wrong while fetching the definition."

def open_camera():
    try:
        system_os = platform.system()
        if system_os == "Windows":
            subprocess.run("start microsoft.windows.camera:", shell=True)  # Windows
        elif system_os == "Darwin":  # macOS
            subprocess.run(["open", "/System/Applications/Photo Booth.app"], check=True)
        elif system_os == "Linux":
            subprocess.run(["xdg-open", "cheese"], check=True)  # Opens Cheese on Linux
        else:
            speak("Unsupported operating system")
            return
    except Exception as e:
        print("Error opening camera:", str(e))
        speak("Error opening camera")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("YOUR_EMAIL_ID", "YOUR_APP_KEY")  # Avoid hardcoding credentials in real applications
        server.sendmail("YOUR_EMAIL_ID", to, content)
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
            print("File not found.")  # Debugging output
            speak("I couldn't find the file. Please try again.")
            break  # Exit if no file is found

def get_random_quote():
    try:
        url = "https://zenquotes.io/api/random"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            quote = data[0].get("q", "No quote found.")
            author = data[0].get("a", "Unknown")
            return f"Here's a quote: \"{quote}\" - {author}"
        else:
            return "Sorry, I couldn't fetch a quote right now."
    except Exception as e:
        return "Something went wrong while fetching a quote."

def calculate_math(expression):
    try:
        # Remove any unwanted characters for safety
        expression = re.sub(r'[^0-9+\-*/().]', '', expression)

        result = eval(expression)  # Simple calculation
        speak(f"The answer is {result}")
    except Exception as e:
        speak("Sorry, I couldn't calculate that.")

def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            condition = data["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp} degrees Celsius with {condition}.")
        else:
            speak("I couldn't find the weather for that location.")
    except Exception as e:
        print(f"Error: {e}")  # Debugging: Print the error
        speak("Sorry, I couldn't retrieve the weather data.")

def get_news():
    url_top_headlines = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    response = requests.get(url_top_headlines).json()

    if response["totalResults"] > 0:
        articles = response["articles"]
    else:
        url_everything = f"https://newsapi.org/v2/everything?q=india&apiKey={NEWS_API_KEY}"
        response = requests.get(url_everything).json()
        
        if response["totalResults"] > 0:
            articles = response["articles"]
        else:
            url_source = f"https://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey={NEWS_API_KEY}"
            response = requests.get(url_source).json()
            
            if response["totalResults"] > 0:
                articles = response["articles"]
            else:
                return "No news found."

    # Format the first few articles (limit to 3)
    news_list = []
    for i, article in enumerate(articles[:3]):
        news_list.append(f"{i+1}. {article['title']} - {article['source']['name']}")
    return "\n".join(news_list)

def take_screenshot():
    """Takes a screenshot and saves it in the OneDrive Screenshots folder"""

    # Define the correct OneDrive Screenshots folder path
    one_drive_screenshots_folder = os.path.join(os.path.expanduser("~"), "OneDrive", "Pictures", "Screenshots")

    # Ensure the folder exists
    os.makedirs(one_drive_screenshots_folder, exist_ok=True)

    # Generate a timestamped filename
    filename = f"screenshot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
    filepath = os.path.join(one_drive_screenshots_folder, filename)

    # Capture and save the screenshot
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

    # Print and speak the confirmation
    confirmation_text = f"📸 Screenshot saved at: {filepath}"
    print(confirmation_text)
    speak(confirmation_text)

    return filepath  # Return the file path for debugging

# Take voice command
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        update_status("Listening...", "green")
        r.pause_threshold = 1 
        audio = r.listen(source)

        try:
            update_status("Processing...", "#FFA500")  # Orange color for processing
            query = r.recognize_google(audio, language='en-US').lower()
            if query:
                chat_box.insert(END, f"You: ", "user_tag")
                chat_box.insert(END, f"{query}\n", "user")
                update_status("Ready", "#4CAF50")  # Green color for ready
                return query
        except sr.UnknownValueError:
            update_status("Ready", "#4CAF50")
            speak("Sorry, I didn't catch that. Can you repeat?")
            return ""  # Return empty string instead of "None"
        except sr.RequestError:
            update_status("Error", "#F44336")  # Red color for error
            speak("Sorry, I couldn't connect to Google services.")
            return ""

    return ""

def update_status(text, color):
    status_label.config(text=text, fg=color)
    root.update()

def smooth_scroll():
    chat_box.after(100, lambda: chat_box.yview_moveto(1.0)) 

# Ask for user's name
def get_user_name():
    global user_name
    
    # Check if we already have the user's name saved
    if load_user_data():
        speak(f"Welcome back, {user_name}!")
        return
    
    speak("What should I call you?")
    name = takecommand()
    if name and name != "None":
        user_name = name.capitalize()
        # speak(f"Nice to meet you, {user_name}")
        save_user_data()

def tell_joke():
    try:
        url = "https://icanhazdadjoke.com/"
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            joke = response.json()["joke"]
            speak(joke)
        else:
            speak("Sorry, I couldn't fetch a joke right now.")

    except Exception as e:
        speak("Something went wrong while fetching a joke.")

def get_date_info():
    today = datetime.today()
    day_name = today.strftime("%A")  # Full weekday name (e.g., Sunday)
    formatted_date = today.strftime("%B %d, %Y")  # Example: March 2, 2025
    return f"Today is {day_name}, {formatted_date}."

def get_day_info():
    today = datetime.today()
    return f"It's {today.strftime('%A')}."

def tell_fun_fact():
    try:
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)

        if response.status_code == 200:
            fact = response.json()["text"]
            speak(f"Here's a fun fact: {fact}")
        else:
            speak("Sorry, I couldn't fetch a fun fact right now.")

    except Exception as e:
        speak("Something went wrong while fetching a fun fact.")

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
    smooth_scroll()
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

    elif 'time' in query:
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

    elif 'send message' in query:
        send_whatsapp_message()

    elif 'play song' in query or 'play song on youtube' in query:
        play_youtube_song()
    
    elif 'find file' in query:
        find_and_open_file()

    elif 'exit' in query or 'stop' in query:
        speak(f"Goodbye {user_name}")
        os._exit(0)
        root.quit()
    elif 'joke' in query or 'tell me a joke' in query:
        tell_joke()
    elif 'fun fact' in query or 'tell me a fun fact' in query:
        tell_fun_fact()
    elif 'calculate' in query:
        expression = query.replace("calculate", "").strip()
        calculate_math(expression)
    elif 'weather' in query:
        speak("Which city?")
        city = takecommand()
        if city != "None":
            get_weather(city)
    elif "news" in query:
        speak("Fetching the latest news from India...")
        news = get_news()
        speak(news)
    elif "date" in query:
        speak(get_date_info())
    elif "day" in query:
        speak(get_day_info())
    elif "define" in query or "meaning of" in query:
        word = query.replace("define", "").replace("meaning of", "").strip()
        if word:
            speak(get_definition(word))
        else:
            speak("Which word would you like me to define?")
            word = takecommand()
            if word != "None":
                speak(get_definition(word))
    elif "quote" in query or "inspire me" in query:
        quote = get_random_quote()
        speak(quote)
    elif "screenshot" in query:
        take_screenshot()
        speak("screenshot saved successfully at pictures folder")
    elif "camera" in query:
        open_camera()
        speak("Camera opened")
    elif 'open' in query:
            response = open_app(query)
            speak(response)
    else:
        speak("I'm not sure how to do that.")
    ask_for_more()

# Ask if user needs anything else
def ask_for_more():
    speak("Do you need anything else?")  
    response = takecommand().strip().lower()

    # Check for positive responses
    positive_responses = ["yeah", "sure", "okay", "yup", "of course", "yes", "yep", "y", "ya", "yea"]
    # Check for negative responses
    negative_responses = ["no", "nope", "nah", "not now", "no thank you", "thanks", "n", "negative"]
    
    if any(word in response for word in positive_responses):
        speak("Okay, what do you need?")
        command = takecommand()
        if command != "None":
            perform_task(command)
    elif any(word in response for word in negative_responses):
        speak(f"Okay {user_name}, I'll be here if you need me.")
        os._exit(0)
        root.quit()
    else:
        # speak("I didn't understand your response. Please say yes or no.")
        ask_for_more()  # Ask again if the response wasn't clear

# Listen for activation command
def listen_for_activation():
    update_status("Waiting for activation...", "#808080")  # Gray color for waiting
    while True:
        query = takecommand()
        if query and any(word in query for word in ["hey nova", "hi nova", "yo nova", "nova", "sup nova"]):
            update_status("Active", "#4CAF50")  # Green color for active
            speak("Yes? How can I help?")  
            command = takecommand()
            if command and command != "None":
                perform_task(command)
            break  # Exit the loop to prevent infinite recursion

# Toggle dark/light mode
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    
    if dark_mode:
        # Dark mode
        root.configure(bg=DARK_BG)
        header_frame.configure(bg=DARK_BG)
        header_label.configure(bg=DARK_BG, fg=TEXT_COLOR_DARK)
        frame.configure(bg=DARK_BG)
        chat_box.configure(bg=DARK_BG, fg=TEXT_COLOR_DARK, insertbackground=TEXT_COLOR_DARK)
        status_label.configure(bg=DARK_BG)
        theme_button.configure(text="🌞 Light Mode")
        
        # Update text colors for dark mode
        chat_box.tag_configure("user", foreground=USER_TEXT_COLOR)
        chat_box.tag_configure("nova", foreground=NOVA_TEXT_COLOR)
        chat_box.tag_configure("user_tag", foreground=USER_TEXT_COLOR, font=("Arial", 12, "bold"))
        chat_box.tag_configure("nova_tag", foreground=NOVA_TEXT_COLOR, font=("Arial", 12, "bold"))
    else:
        # Light mode
        root.configure(bg=LIGHT_BG)
        header_frame.configure(bg=LIGHT_BG)
        header_label.configure(bg=LIGHT_BG, fg=TEXT_COLOR_LIGHT)
        frame.configure(bg=LIGHT_BG)
        chat_box.configure(bg=LIGHT_BG, fg=TEXT_COLOR_LIGHT, insertbackground=TEXT_COLOR_LIGHT)
        status_label.configure(bg=LIGHT_BG)
        theme_button.configure(text="🌙 Dark Mode")
        
        # Update text colors for light mode
        chat_box.tag_configure("user", foreground=USER_TEXT_COLOR)
        chat_box.tag_configure("nova", foreground=NOVA_TEXT_COLOR)
        chat_box.tag_configure("user_tag", foreground=USER_TEXT_COLOR, font=("Arial", 12, "bold"))
        chat_box.tag_configure("nova_tag", foreground=NOVA_TEXT_COLOR, font=("Arial", 12, "bold"))

# Initialize Tkinter window
root = tk.Tk()
root.title("NOVA - Voice Assistant")
root.geometry("800x600")
root.configure(bg=LIGHT_BG)

# Create a header frame
header_frame = Frame(root, bg=LIGHT_BG)
header_frame.pack(fill="x", padx=10, pady=5)

# Header label with logo
header_label = Label(header_frame, text="NOVA", font=("Arial", 24, "bold"), fg=ACCENT_COLOR, bg=LIGHT_BG)
header_label.pack(side="left", pady=10)

# Subtitle label
subtitle_label = Label(header_frame, text="Your Voice Assistant", font=("Arial", 14), fg=TEXT_COLOR_LIGHT, bg=LIGHT_BG)
subtitle_label.pack(side="left", padx=10, pady=10)

# Theme toggle button
theme_button = Button(header_frame, text="🌙 Dark Mode", command=toggle_theme, 
                     bg=ACCENT_COLOR, fg=BUTTON_TEXT_COLOR, font=("Arial", 10),
                     relief="flat", padx=10, pady=5)
theme_button.pack(side="right", pady=10, padx=10)

# Chat frame with rounded corners
frame = Frame(root, bg=LIGHT_BG, bd=1, relief="solid")
frame.pack(padx=20, pady=10, fill=BOTH, expand=True)

# Chatbox with custom styling
chat_box = Text(frame, wrap="word", height=20, width=70, font=("Arial", 12), 
               bg=LIGHT_BG, fg=TEXT_COLOR_LIGHT, bd=0, padx=10, pady=10,
               insertbackground=TEXT_COLOR_LIGHT)
scrollbar = Scrollbar(frame, command=chat_box.yview)
chat_box.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
chat_box.pack(side="left", fill="both", expand=True)

# Text color configurations with bold tags for names
chat_box.tag_configure("user", foreground=USER_TEXT_COLOR)
chat_box.tag_configure("nova", foreground=NOVA_TEXT_COLOR)
chat_box.tag_configure("user_tag", foreground=USER_TEXT_COLOR, font=("Arial", 12, "bold"))
chat_box.tag_configure("nova_tag", foreground=NOVA_TEXT_COLOR, font=("Arial", 12, "bold"))

# Status label with modern styling
status_label = Label(root, text="Starting up...", font=("Arial", 12), bg=LIGHT_BG, fg="#808080",
                    padx=10, pady=5)
status_label.pack(pady=10)

# Footer with version info
footer_label = Label(root, text="NOVA v2.0", font=("Arial", 8), fg="#888888", bg=LIGHT_BG)
footer_label.pack(side="bottom", pady=5)

# Welcome message
# welcome_message = "Hey there! I'm NOVA, your personal assistant."

# Main assistant loop
def assistant_loop():
    update_status("Starting up...", "#FFA500")
    get_user_name()
    # speak(welcome_message)
    wishme()
    update_status("Waiting for activation...", "#808080")
    listen_for_activation()

root.after(1000, assistant_loop)
root.mainloop()
