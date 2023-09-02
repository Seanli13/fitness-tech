from voice import Voice
from bicep_curl import analyze_bicep_curl
from pushup import analyze_pushups
from plank import analyze_plank
from squat import analyze_squat
from downward_dog import analyze_downward_dog
from bench import analyze_bench
from deadlift import analyze_deadlift
import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer
import time

class FitnessAnalyzer:
    def __init__(self):
        self.voice = Voice()
        # Setup Vosk
        if not os.path.exists("vosk-model-small-en-us-0.15"):
            print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        else:
            self.model = Model("vosk-model-small-en-us-0.15")
            self.rec = KaldiRecognizer(self.model, 16000)

            # Setup PyAudio
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input = True, frames_per_buffer=8000)
            self.stream.start_stream()

    def analyze_exercise(self, exercise_type: str, video_path=0):
        print(f"The chosen exercise is: {exercise_type}")
        if exercise_type == 'bicep_curl':
            analyze_bicep_curl(self.voice, video_path=video_path)
        elif exercise_type == 'pushups': 
            analyze_pushups(self.voice, video_path=video_path)
        elif exercise_type == 'planks': 
            analyze_plank(self.voice, video_path=video_path)
        elif exercise_type == 'squat':
            analyze_squat(self.voice, video_path=video_path)
        elif exercise_type == 'downward_dog':
            analyze_downward_dog(self.voice, video_path=video_path)
        elif exercise_type == 'bench':
            analyze_bench(self.voice, video_path=video_path)
        elif exercise_type == 'deadlift':
            analyze_deadlift(self.voice, video_path=video_path)

    def setup_new_user(self):
        print(f"Hello there! Thank for using [insert product name]. Before we begin, I would like to know a little bit about yourself.")
        self.voice.speak(f"Hello there! Thank for using [insert product name]. Before we begin, I would like to know a little bit about yourself.")
        print("What is your name?")
        self.voice.speak("What is your name?")

        name = "Test"
        asking_confirm = False

        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                result_str = self.rec.Result()
                print(result_str)

                # Implement commands here
                result = json.loads(result_str)
                if 'text' in result and len(result['text']) > 0 and not asking_confirm:
                    name = result["text"]
                    print(f"I heard {name}, is this correct?")
                    asking_confirm = True
                elif asking_confirm and 'text' in result and 'yes' in result['text']:
                    break
                elif asking_confirm and 'text' in result and 'no' in result['text']:
                    print("Please say your name again.")
                    asking_confirm = False


        age = "18"
        
        asking_confirm = False
        print("What is your age?")

        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                result_str = self.rec.Result()
                print(result_str)

                # Implement commands here
                result = json.loads(result_str)
                if 'text' in result and len(result['text']) > 0 and not asking_confirm:
                    age = result["text"]
                    print(f"I heard {age}, is this correct?")
                    asking_confirm = True
                elif asking_confirm and 'text' in result and 'yes' in result['text']:
                    break
                elif asking_confirm and 'text' in result and 'no' in result['text']:
                    print("Please say your age again.")
                    asking_confirm = False

        print(f"Your name is {name} and your age is {age}.")
        self.shutdown()

    def shutdown(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()