# NOVA – AI Voice Assistant with GUI

**NOVA** is an advanced voice-activated desktop assistant developed using Python. With an intuitive graphical interface and seamless voice command integration, NOVA assists users with tasks like opening applications, sending emails, playing music, checking the weather, telling jokes, and much more.

## 🌟 Features

- 🎙️ **Voice Activation**: Trigger the assistant with "Hey Nova".
- 🔍 **Smart Queries**: Search Wikipedia, Google, or define terms using APIs.
- 📧 **Send Emails**: Speak recipient and message content to send emails.
- 📱 **WhatsApp Messaging**: Send WhatsApp messages instantly via voice.
- 🎵 **YouTube Songs**: Play any song from YouTube using voice input.
- 🗃️ **Open Files & Applications**: Locate and open local files or system apps.
- 📸 **Screenshot Capture**: Save screenshots with voice command.
- 📰 **News & Weather Updates**: Get the latest Indian headlines or local weather.
- 🌓 **Dark/Light Theme Toggle**: Switch between sleek modern UI modes.
- 🧠 **Memory**: Remembers your name across sessions.
- 🤖 **Fun Interactions**: Hear jokes, fun facts, and inspirational quotes.

## 🖥️ GUI Highlights

- Built using **Tkinter** for a modern chat-like interface.
- Chat messages from both user and NOVA are color-coded.
- Status bar shows current state (listening, processing, idle).
- Theme switcher button for light/dark UI experience.

## 🔧 Technologies Used

- Python 3.x
- `Tkinter` – GUI
- `SpeechRecognition` – Voice input
- `pyttsx3` – Text-to-speech
- `pyautogui`, `pywhatkit`, `subprocess`, `requests`, `wikipedia`, `PIL`
- API integrations:
  - OpenWeatherMap
  - NewsAPI
  - ZenQuotes
  - DictionaryAPI
  - icanhazdadjoke

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/nova-voice-assistant.git
   cd nova-voice-assistant
## Install dependencies
pip install -r requirements.txt

## Run the assistant
python automation.py

## Ensure
**Microphone access is enabled.**</br>
**Stable internet connection for APIs.**</br>
**You update the email credentials inside sendEmail() function.**


## ScreenShot

![image](https://github.com/user-attachments/assets/5d5a5cf9-dbfd-41c1-bc90-921a2d7384b8)

## 🧪 Sample Commands
**Here are some commands NOVA understands:**

"Hey Nova, open Notepad"

"Search Google for artificial intelligence"

"Play Shape of You on YouTube"

"Send an email to example at gmail dot com"

"What's the weather in Mumbai?"

"Tell me a joke"

"Take a screenshot"

"Define philosophy"

"Lock the system"

"Tell me a fun fact"

## Developed By

Viraj Jadhav & Devang Deokule

[[LinkedIn](https://www.linkedin.com/in/viraj-jadhav-a630182a4/) | [GitHub](https://github.com/vira250/) |jviraj666@gmail.com]

[[LinkedIn](https://www.linkedin.com/in/devang-deokule-188584268/) |[ GitHub](https://github.com/Devang-Deokule) | deokuledevang@gmail.com]
