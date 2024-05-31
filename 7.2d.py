import speech_recognition as sr
import RPi.GPIO as GPIO
import time
import tkinter as tk

# Setup GPIO
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Initialize the GUI
root = tk.Tk()
root.title("LED Control")
status_label = tk.Label(root, text="LED is OFF", font=("Helvetica", 24))
status_label.pack(pady=20)

def update_status(state):
    if state:
        status_label.config(text="LED is ON")
    else:
        status_label.config(text="LED is OFF")

def turn_on_led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    update_status(True)

def turn_off_led():
    GPIO.output(LED_PIN, GPIO.LOW)
    update_status(False)

def process_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)

    try:
        # Recognize the audio and convert it to text
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an issue connecting to the service.")
        return ""

def voice_control():
    command = process_voice_command()
    if "turn on" in command and "light" in command:
        turn_on_led()
    elif "turn off" in command and "light" in command:
        turn_off_led()
    elif "goodbye" in command or "stop" in command:
        GPIO.cleanup()
        root.quit()
    else:
        print("Command not supported.")

voice_button = tk.Button(root, text="Speak", command=voice_control, font=("Helvetica", 18))
voice_button.pack(pady=20)

root.mainloop()
