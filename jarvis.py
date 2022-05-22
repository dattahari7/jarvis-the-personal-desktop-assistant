from re import search
import sys
from pip import main
import pyttsx3
import speech_recognition as sr
import datetime
import time
import wikipedia
import webbrowser
import os
import pywhatkit
import pyautogui
from dataclasses import dataclass
from bs4 import BeautifulSoup
from itertools import count
from multiprocessing.connection import wait
from unicodedata import name
from matplotlib import image
import requests
from playsound import playsound


from PyPDF2 import PdfFileReader
import subprocess32 as sp
import requests
from email.message import EmailMessage
import smtplib

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisGui import Ui_JarvisUi

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Set Rate
engine.setProperty('rate', 190)
# Set Volume
engine.setProperty('volume', 1.0)
# print(voices[1].id)
# Set Voice (Male)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = datetime.datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning sir")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon sir")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening sir")
    speak("Please tell me how may I help you")


def location():
    speak('wait sir, let me check')
    try:
        ipAdd = requests.get('https://api.ipify.org/').text
        print(ipAdd)
        url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
        geo_requests = requests.get(url)
        geo_data = geo_requests.json()
        city = geo_data['city']
        country = geo_data['country']
        speak(
            f'sir i am not sure, but i think we are in {city} city of {country} country')
    except Exception as e:
        speak('sorry sir, due to network issue i am not able to find where we are.')


def open_camera():
    sp.run('start microsoft.windows.camera:', shell=True)


def find_my_ip():
    ipAdd = requests.get('https://api.ipify.org/').text
    # print(ipAdd)
    # ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ipAdd


def open_calculator():
    calculatorPath = "C:\\Windows\\System32\\calc.exe"
    os.startfile(calculatorPath)


def send_email(receiver_address, subject, message):
    EMAIL = "jarvisdesktopassistant7@gmail.com"
    PASSWORD = "Jarvisdesktopassistant@7"
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_weather_report(city):
    OPENWEATHER_APP_ID = "839b07c59559a38c8a08c7e81268b5a5"
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"


def get_latest_news():
    NEWS_API_KEY = "a948deedb04842079ce4fea7d21744c0"
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def saveFile():
    pyautogui.keyDown('ctrl')
    pyautogui.press('s')
    pyautogui.keyUp('ctrl')


def alarm(timing):
    alarmTime = str(datetime.datetime.now().strptime(timing, "%I:%M %p"))
    alarmTime = alarmTime[11:-3]
    
    alhours = alarmTime[:2]
    alhours = int(alhours)
    alMinutes = alarmTime[3:5]
    alMinutes = int(alMinutes)
    speak(f"Done, alarm is set for {timing}")
    while True:
        if alhours == datetime.datetime.now().hour:
            if alMinutes == datetime.datetime.now().minute:
                print("alarm is running")
                playsound(r"C:\\Users\\Jarvis\\Desktop\\JarvisFinal\\alarmSound.mp3")
            elif alMinutes < datetime.datetime.now().minute:
                break


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
        # It takes microphone input from the user and returns string output
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=3, phrase_time_limit=5)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")

        except Exception:
            speak('Sorry, I could not understand. Could you please say that again?')
            query = 'None'
        return query

    def TaskExecution(self):
        playsound(r'C:\\Users\\Jarvis\\Desktop\\JarvisFinal\\JarvisVoice.mp3')
        while True:
            wishMe()
            while True:
                self.query = self.takeCommand().lower()
                # Logic for executing tasks based on self.query
                if 'search on wikipedia' in self.query or 'search on wikipedia jarvis' in self.query:
                    speak('what can i search on wikipedia sir')
                    self.query = self.takeCommand().lower()
                    speak('Searching On Wikipedia...')
                    results = wikipedia.summary(self.query, sentences=2)
                    speak("According to Wikipedia")
                    # print(results)
                    speak(results)

                elif 'open youtube' in self.query or 'search on youtube' in self.query:
                    speak('what can i search on youtube sir')
                    searchOnYoutube = self.takeCommand().lower()
                    speak('Opening youtube')
                    pywhatkit.playonyt(searchOnYoutube)
                    # webbrowser.open("https://www.youtube.com")

                elif 'close youtube' in self.query or 'close youtube jarvis' in self.query:
                    speak('closing youtube..')
                    os.system("taskkill /f /im chrome.exe")

                elif 'open google' in self.query or 'search on google' in self.query:
                    speak('what can i search on google sir')
                    searchOnGoogle = self.takeCommand().lower()
                    pywhatkit.search(searchOnGoogle)

                elif 'close google' in self.query or 'close google jarvis' in self.query:
                    speak('closing google..')
                    os.system("taskkill /f /im chrome.exe")

                elif 'open stackoverflow' in self.query:
                    webbrowser.open("https://www.stackoverflow.com")

                elif 'close stackoverflow' in self.query or 'close stackoverflow jarvis' in self.query:
                    os.system("taskkill /f /im chrome.exe")

                elif 'play music' in self.query or 'jarvis play music' in self.query:
                    speak('Playing Music')
                    music_dir = 'C:\\Users\\Jarvis\\Music'
                    songs = os.listdir(music_dir)
                    print(songs)
                    os.startfile(os.path.join(music_dir, songs[0]))

                elif 'set alarm' in self.query or 'alarm' in self.query:
                    speak('sir please tell me the time to set alarm for example set alarm to 5:30 am')
                    alTime = self.takeCommand()
                    alTime = alTime.replace("set alarm to", "")
                    alTime = alTime.replace(".", "")
                    alTime = alTime.upper()
                    alarm(alTime)

                elif 'what is time now' in self.query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"Sir, the current time is {strTime}")

                elif 'open notepad' in self.query or 'open notepad jarvis' in self.query:
                    speak('Opening notepad...')
                    notepadPath = "C:\\Windows\\System32\\notepad"
                    os.startfile(notepadPath)
                    speak('do you want write something on notepad sir')
                    while True:
                        self.query = self.takeCommand().lower()
                        if 'yes' in self.query or 'yes jarvis' in self.query:
                            speak('what can you want to write please speak')
                            self.query = self.takeCommand()
                            pyautogui.write(self.query, interval=0.25)
                            speak('can i save this file sir')
                            while True:
                                self.query = self.takeCommand().lower()
                                if 'yes' in self.query or 'yes jarvis' in self.query:
                                    saveFile()
                                    speak("give the name of file sir")
                                    while True:
                                        self.query = self.takeCommand().lower()
                                        pyautogui.write(
                                            self.query, interval=0.25)
                                        pyautogui.press('enter')
                                        speak('file saved succesfully sir')
                                        if True:
                                            break
                                    break
                                elif 'no' in self.query or 'no jarvis' in self.query:
                                    speak('okay sir')
                                    break
                            break
                        elif 'no' in self.query or 'no jarvis' in self.query:
                            speak('okay sir')
                            break

                elif 'close notepad' in self.query or 'close notepad jarvis' in self.query:
                    speak('closing notepad...')
                    os.system("taskkill /f /im notepad.exe")

                elif 'open command prompt' in self.query or 'open command prompt jarvis' in self.query:
                    speak('Opening command prompt')
                    os.system("start cmd")

                elif 'close command prompt' in self.query or 'close cmd' in self.query or 'close command prompt jarvis' in self.query:
                    speak('closing command prompt..')
                    os.system("taskkill /f /im chrome.exe")

                elif 'send message' in self.query or 'send a whatsApp message' in self.query or 'send message jarvis' in self.query:
                    phoneBook = {
                        "datta": 9130809293,
                        "rushi": 9604583520,
                        "harjinder": 7447245787,
                        "prashant": 9960317906,
                        "ganesh":7499500168
                    }
                    speak('whome i send message sir')
                    while True:
                        contactName = self.takeCommand().lower()
                        if contactName in phoneBook.keys():
                            phoneNo = phoneBook[contactName]
                            speak(f'what message i send to {contactName} sir')
                            wpMessage = self.takeCommand().lower()
                            pywhatkit.sendwhatmsg_instantly(f"+91{phoneNo}", wpMessage, 10)
                            time.sleep(5)
                            pyautogui.click()
                            pyautogui.press('enter')
                            time.sleep(2)
                            speak(
                                f'message send to {contactName} successfully')
                            pyautogui.hotkey('ctrl', 'f4')
                            break
                        else:
                            continue
                elif 'shutdown the system' in self.query or 'shutdown the system jarvis' in self.query:
                    os.system("shutdown /s /t 5")

                elif 'restart the system' in self.query or 'restart the system jarvis' in self.query:
                    os.system("shutdown /r /t 5")

                elif 'sleep the system' in self.query or 'sleep the system jarvis' in self.query:
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

                elif 'switch the window' in self.query or 'switch the window jarvis' in self.query:
                    pyautogui.keyDown('alt')
                    pyautogui.press('tab')
                    time.sleep(0.5)
                    pyautogui.keyUp('alt')

                elif 'close current window' in self.query or 'close current window jarvis' in self.query or 'jarvis close current window' in self.query:
                    speak('closing current window')
                    pyautogui.hotkey('alt', 'f4')
                elif 'minimize all windows' in self.query or 'minimise all windows' in self.query or 'minimize all windows jarvis' in self.query:
                    speak('minimizing all windows')
                    pyautogui.hotkey('win', 'm')
                elif 'maximize all windows' in self.query or 'maximize all windows jarvis' in self.query:
                    speak('maximizing all windows...')
                    pyautogui.hotkey('win', 'shift', 'm')
                elif 'go to sleep jarvis' in self.query or 'quite jarvis' in self.query or 'ok quite jarvis' in self.query or 'jarvis go to sleep' in self.query or 'go to sleep' in self.query:
                    speak('okk sir i am going to sleep')
                    exit()

                elif 'private all files' in self.query or 'jarvis private all files' in self.query:
                    speak('sir please conform you want to private files of this folder or make it visible for everyone')
                    while True:
                        conformation = self.takeCommand().lower()
                        if 'yes make it private' in conformation:
                            os.system("attrib +h /s /d")
                            speak('sir, all the files in this folder are now private')
                            break
                        elif 'leave it' in conformation:
                            speak('ok sir')
                            break

                elif 'visible all files' in self.query or 'visible all files jarvis' in self.query:
                    os.system("attrib -h /s /d")
                    speak('sir, all the files in this folder are now visible to everyone. i wish you are taking this decesion on yourself')
                    break
                elif 'where we are' in self.query:
                    location()

                elif 'jarvis take a screenshot' in self.query or 'take screenshot' in self.query:
                    speak('please sir hold the screen for few seconds, i am taking screenshot')
                    time.sleep(3)
                    img = pyautogui.screenshot()
                    speak('sir, please tell me the name for this screenshot file')
                    name = self.takeCommand().lower()
                    img.save(f"{name}.png")
                    speak('i am done sir, the screenshot is saved in our main folder. now i am ready for next command sir')

                elif 'open camera' in self.query or 'open camera jarvis' in self.query:
                    speak('opening camera..')
                    open_camera()

                elif 'close camera' in self.query or 'close camera jarvis' in self.query:
                    speak('closing camera..')
                    os.system("taskkill /f /im WindowsCamera.exe")

                elif 'open calculator' in self.query or 'open calculator jarvis' in self.query:
                    speak('opening calculator..')
                    open_calculator()

                elif 'close calculator' in self.query or 'close calculator jarvis' in self.query:
                    speak('closing calculator..')
                    os.system("taskkill /f /im Calculator.exe")

                elif 'ip address' in self.query or 'what is ip address jarvis' in self.query or 'what is ip address' in self.query:
                    ip_address = find_my_ip()
                    speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                    # print(f'Your IP Address is {ip_address}')

                elif "send an email" in self.query or "send email" in self.query or "send an email jarvis" in self.query:
                    emailBook = {
                        "datta": 'dattaharik61@gmail.com',
                        "rushikesh": 'gawanderushi1999@gmail.com',
                        "harjinder": 'ganeshnikam1407@gmail.com',
                        "prashant": 'ganeshnikam1407@gmail.com',
                        "ganesh":'ganeshnikam1407@gmail.com'
                    }
                    speak('whome i send email sir?')
                    while True:
                        emailName = self.takeCommand().lower()
                        if emailName in emailBook.keys():
                            receiver_address = emailBook[emailName]
                            print(receiver_address)
                            # emailId= input("Enter email address: ")
                            speak("What should be the subject sir?")
                            subject = self.takeCommand().capitalize()
                            speak("What is the message sir?")
                            message = self.takeCommand().capitalize()
                            if send_email(receiver_address, subject, message):
                                speak(f"I've sent the email successfully to {emailName} sir.")
                            else:
                                speak("Something went wrong while I was sending the mail. Please check the error logs sir.")
                            break

                elif 'joke' in self.query or 'tell me joke' in self.query or 'tell me joke jarvis' in self.query:
                    speak(f"Hope you like this one sir")
                    joke = get_random_joke()
                    speak(joke)
                    # speak("For your convenience, I am printing it on the screen sir.")
                    # print(joke)

                elif "tell me advice" in self.query or "tell me advice jarvis" in self.query or "any advice for me jarvis" in self.query or "advice" in self.query:
                    speak(f"Here's an advice for you, sir")
                    advice = get_random_advice()
                    speak(advice)
                    # speak("For your convenience, I am printing it on the screen sir.")
                    # print(advice)

                elif 'todays news' in self.query or 'todays news jarvis' in self.query or 'any news update jarvis' in self.query or 'news' in self.query:
                    speak(f"I'm reading out the latest news headlines, sir")
                    speak(get_latest_news())
                    # speak("For your convenience, I am printing it on the screen sir.")
                    # print(*get_latest_news(), sep='\n')

                elif 'what is weather today' in self.query or 'what is weather today jarvis' in self.query or 'weather' in self.query or 'what is weather' in self.query:
                    ip_address = find_my_ip()
                    city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                    speak(f"Getting weather report for your city sir.")
                    weather, temperature, feels_like = get_weather_report(city)
                    speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
                    speak(f"Also, the weather report talks about {weather}")
                    # speak("For your convenience, I am printing it on the screen sir.")
                    # print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_JarvisUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.closeTask)

    def startTask(self):
        self.ui.movie = QtGui.QMovie(r"C:\\Users\\Jarvis\\Desktop\\JarvisFinal\\img\\jarvisBg.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(r"C:\\Users\\Jarvis\\Desktop\\JarvisFinal\\img\\initialization.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def closeTask(self):
        sys.exit()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        lable_time = current_time.toString('hh:mm:ss')
        lable_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(lable_date)
        self.ui.textBrowser_2.setText(lable_time)


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
sys.exit(app.exec_())
