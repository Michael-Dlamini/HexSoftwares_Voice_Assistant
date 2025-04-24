import pyttsx3
import datetime
import time
import speech_recognition as sr
import threading
import webbrowser
import tkinter as tk
from tkinter import messagebox

# --- Initialize the engine ---
engine = pyttsx3.init()

# Set the voice (replace 'index' with the correct voice index)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Adjust this index based on the test you did

def talk(text):
    engine.say(f"Michael, {text}")
    engine.runAndWait()

def listen_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = listener.listen(source)
    try:
        command = listener.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        talk("I didn't catch that.")
        return ""
    except sr.RequestError:
        talk("There's a network problem.")
        return ""

# --- Alarm function ---
def set_alarm(alarm_time):
    def alarm_thread():
        while True:
            now = datetime.datetime.now().strftime('%H:%M')
            if now == alarm_time:
                talk("Your alarm is going off!")
                break
            time.sleep(30)
    threading.Thread(target=alarm_thread).start()
    talk(f"Alarm set for {alarm_time}")

# --- Lunch reminder ---
def lunch_reminder():
    def reminder_loop():
        while True:
            now = datetime.datetime.now().strftime('%H:%M')
            if now == "12:00":
                talk("it's Lunch time.")
                time.sleep(60)
            time.sleep(30)
    threading.Thread(target=reminder_loop, daemon=True).start()

# --- Command handler ---
def run_assistant(command):
    if 'time' in command:
        now = datetime.datetime.now().strftime('%H:%M')
        talk(f"the time is {now}")

    elif 'set alarm' in command:
        talk("What time should I set the alarm for? Say it like '14 30' for 2:30 PM")
        alarm_input = listen_command()
        alarm_time = alarm_input.replace(" ", ":")
        set_alarm(alarm_time)

    elif 'news' in command or 'open news' in command:
        talk("Opening MyBroadband news.")
        webbrowser.open("https://mybroadband.co.za/news/")

    elif 'exit' in command:
        talk("Goodbye!")
        exit()

    else:
        talk("Can you say that again?")

# --- GUI code ---
class VoiceAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("400x400")
        self.root.configure(bg="#f0f0f0")

        self.label = tk.Label(root, text="Hello Michael!", font=("Arial", 16), bg="#f0f0f0")
        self.label.pack(pady=20)

        self.time_label = tk.Label(root, text=f"Current Time: {datetime.datetime.now().strftime('%H:%M:%S')}", font=("Arial", 12), bg="#f0f0f0")
        self.time_label.pack(pady=10)

        self.mic_button = tk.Button(root, text="Start Listening", font=("Arial", 14), command=self.start_listening, bg="#4CAF50", fg="white", padx=20, pady=10)
        self.mic_button.pack(pady=10)

        self.news_button = tk.Button(root, text="Open News", font=("Arial", 14), command=self.open_news, bg="#2196F3", fg="white", padx=20, pady=10)
        self.news_button.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=root.quit, bg="#f44336", fg="white", padx=20, pady=10)
        self.exit_button.pack(pady=20)

        lunch_reminder()

    def start_listening(self):
        command = listen_command()
        run_assistant(command)

    def open_news(self):
        webbrowser.open("https://mybroadband.co.za/news/")

# --- Start the GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantApp(root)
    root.mainloop()
