python.py
import os
import random
import speech_recognition as sr
import wikipedia
import webbrowser
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the speaker
speaker = pyttsx3.init()

# Define the assistant's name
assistant_name = "ARIA"

# Define the path to save the owner's voice
voice_dir = "owner_voice"

# Define the listening function
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said.")
            return "None"
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return "None"

# Define the speaking function
def speak(text):
    speaker.say(text)
    speaker.runAndWait()

# Define the greeting function
def greeting():
    speak("Hello world, I am ARIA - Artificial Responsive Intelligent Assistant.")
    speak("I am here because of my master Lucifer.")
    speak("Let's begin by registering your voice.")
    register_owner_voice()

# Define the function to register owner's voice
def register_owner_voice():
    speak("Please speak the passphrase to register your voice.")
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if text:
                # Save the voice file
                with open(os.path.join(voice_dir, "owner_voice.wav"), "wb") as f:
                    f.write(audio.get_wav_data())
                speak("Your voice has been registered successfully.")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand your voice.")
        except sr.RequestError:
            speak("Sorry, I could not process your request.")

# Define the function to handle queries
def handle_query(query):
    # Greet the user and register voice
    if 'activate' in query:
        greeting()

    # Search something on Wikipedia
    elif 'wikipedia' in query:
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            wikipedia_page = wikipedia.page(query).url
            speak(f"According to Wikipedia, {results}. You can find more information on {wikipedia_page}")
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results for this query. Please specify.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any relevant information.")

    # Open a website
    elif 'open' in query:
        query = query.replace("open", "")
        query = query.replace(".com", "")
        query = query.replace(".org", "")
        webbrowser.open_new(query + ".com")

    # Play a song
    elif 'play' in query:
        query = query.replace("play", "")
        songs_dir = '/path/to/music/directory'
        songs = os.listdir(songs_dir)
        os.startfile(os.path.join(songs_dir, random.choice(songs)))

    # Close the program
    elif 'thanks' in query:
        speak("Anytime sir.")
        exit()

    # If the user input doesn't match any of the above conditions, ask for a clarification
    else:
        speak("I am sorry, sir. I did not understand your command.")

# Run the assistant
if __name__ == "__main__":
    while True:
        user_input = listen()
        handle_query(user_input)
