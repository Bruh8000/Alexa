import pyttsx3
import speech_recognition as br
import pywhatkit
import datetime
import wikipedia

listener = br.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():


    try:
       with br.Microphone() as source:
            print('Listening...')
        # Увеличиваем время прослушивания до 5 секунд
            voice = listener.listen(source, timeout=7, phrase_time_limit=7)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)


    except Exception as e:

        print(f"Error: {e}")
        pass
    return command

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M %p')
        print(time)
        talk('Current time is' + time)
    elif 'who is' in command:
        person = command.replace('who  is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)


run_alexa()




