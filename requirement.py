import os
modules = ["pyttsx3", "turtle", "speech_recognition", "pipwin", "pyaudio", "SpeechRecognition", "pywhatkit", "pandas", "webbrowser",
           "covid", "numpy", "wikipedia", "pyautogui", "smtplib", "sinchsms", "Flask", "PyAudio", "utils", "pyqt5", "pyqt5-tools", "playsound","Pyinstaller"]
for i in range(len(modules)):
	# print(modules[i])
    os.system(f'cmd /c "pip install {modules[i]}"')
