import pyttsx3

class Voice:
    """
    sapi5 - SAPI5 on Windows
    nsss - NSSpeechSynthesizer on Mac OS X
    espeak - eSpeak on every other platform
    """
    def __init__(self):
        self.engine = pyttsx3.init("sapi5")
        voice = self.engine.getProperty("voices")
        self.engine.setProperty('voice', voice[0].id)

    def speak(self, message):
        self.engine.say(message)
        self.engine.runAndWait()