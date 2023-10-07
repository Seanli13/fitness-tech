import pyttsx3
import subprocess

class Voice:
    """
    sapi5 - SAPI5 on Windows
    nsss - NSSpeechSynthesizer on Mac OS X
    espeak - eSpeak on every other platform
    """
    def __init__(self):
        self.engine = pyttsx3.init("espeak")
        voice = self.engine.getProperty("voices")
        self.engine.setProperty('voice', voice[0].id)

    # def speak(self, message):
    #     self.engine.say(message)
    #     self.engine.runAndWait()

    def speak(self, text):
        try:
            # Create a wav file
            subprocess.run(["pico2wave", "-w", "output.wav", text], check=True)
            
            # Play the wav file
            subprocess.run(["aplay", "output.wav"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {str(e)}")


# text_to_speech("Hello, how are you?")