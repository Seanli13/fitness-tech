from voice import Voice
from exercises.bicep_curl import analyze_bicep_curl
from exercises.pushup import analyze_pushups
from exercises.plank import analyze_plank
from exercises.squat import analyze_squat
from exercises.downward_dog import analyze_downward_dog
from exercises.bench import analyze_bench
from exercises.deadlift import analyze_deadlift
import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer
import time

class FitnessAnalyzer:
    def __init__(self, user_data=None):
        self.user_data = user_data
        self.voice = Voice()
        # Setup Vosk
        if not os.path.exists("/home/sean/Desktop/fitness-tech/vosk-model-small-en-us-0.15"):
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
        if exercise_type == 'bicep curl':
            analyze_bicep_curl(self.voice, video_path=video_path)
        elif exercise_type == 'push ups': 
            analyze_pushups(self.voice, video_path=video_path)
        elif exercise_type == 'planks': 
            analyze_plank(self.voice, video_path=video_path)
        elif exercise_type == 'squat':
            analyze_squat(self.voice, video_path=video_path)
        elif exercise_type == 'downward dog':
            analyze_downward_dog(self.voice, video_path=video_path)
        elif exercise_type == 'bench':
            analyze_bench(self.voice, video_path=video_path)
        elif exercise_type == 'deadlift':
            analyze_deadlift(self.voice, video_path=video_path)

    def validate_response(self, message, mode=0):
        message = message['text'].strip()
        if mode == 0: # checking yes
            affirmatives = ["yes", "yea", "yeah", "sure"]
            for word in affirmatives:
                if word in message:
                    return True
        elif mode == 1: # checking no
            affirmatives = ["no", "nope"]
            for word in affirmatives:
                if word in message:
                    return True
        elif mode == 2: # checking name
            banned_phrases = {"hello there", "yes", "no", "there"}
            if 1 <= len(message) <= 20 and message not in banned_phrases and len(message.split()) <= 10:
                return True
        elif mode == 3: # checking age
            affirmatives = {"thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", "twenty one", "twenty two", "twenty three", "twenty four", "twenty five", "twenty six", "twenty seven", "twenty eight", "twenty nine", "thirty", "thirty one", "thirty two", "thirty three", "thirty four", "thirty five", "thirty six", "thirty seven", "thirty eight", "thirty nine", "forty", "forty one", "forty two", "forty three", "forty four", "forty five", "forty six", "forty seven", "forty eight", "forty nine", "fifty", "fifty one", "fifty two", "fifty three", "fifty four", "fifty five", "fifty six", "fifty seven", "fifty eight", "fifty nine", "sixty", "sixty one", "sixty two", "sixty three", "sixty four", "sixty five", "sixty six", "sixty seven", "sixty eight", "sixty nine", "seventy", "seventy one", "seventy two", "seventy three", "seventy four", "seventy five", "seventy six", "seventy seven", "seventy eight", "seventy nine", "eighty"}
            if message in affirmatives:
                return True
        return False

    def setup_new_user(self):
        print(f"Hello there! Thank for using FitnessTech. Before we begin, I would like to know a little bit about yourself.")
        self.voice.speak(f"Hello there! Thank for using FitnessTech. Before we begin, I would like to know a little bit about yourself.")
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
                print(json.loads(result_str)["text"])

                # Implement commands here
                result = json.loads(result_str)
                if 'text' in result and not asking_confirm and self.validate_response(result, mode=2):
                    name = result["text"]
                    print(f"I heard {name}, is this correct?")
                    self.voice.speak(f"I heard {name}, is this correct?")
                    asking_confirm = True
                elif asking_confirm and 'text' in result and self.validate_response(result, mode=0):
                    break
                elif asking_confirm and 'text' in result and self.validate_response(result, mode=1):
                    print("Please say your name again.")
                    self.voice.speak("Please say your name again.")
                    asking_confirm = False


        age = "18"
        
        asking_confirm = False
        print("What is your age?")
        self.voice.speak("What is your age?")

        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                result_str = self.rec.Result()
                print(result_str)

                # Implement commands here
                result = json.loads(result_str)
                if 'text' in result and 1 <= len(result['text'].strip().split()) <= 2 and not asking_confirm and self.validate_response(result, mode=3):
                    age = result["text"]
                    print(f"I heard {age}, is this correct?")
                    self.voice.speak(f"I heard {age}, is this correct?")
                    asking_confirm = True
                elif asking_confirm and 'text' in result and self.validate_response(result, mode=0):
                    break
                elif asking_confirm and 'text' in result and self.validate_response(result, mode=1):
                    print("Please say your age again.")
                    self.voice.speak("Please say your name again.")
                    asking_confirm = False

        print(f"Your name is {name} and your age is {age}.")
        self.voice.speak(f"Your name is {name} and your age is {age}.")
        f = open("/home/sean/Desktop/fitness-tech/user.txt", "w")
        if self.user_data == None:
            f.write('{' + f'"{name}":' + '{' + f'"age": "{age}"' + '}}')
        else:
            self.user_data[name] = {"age": age}
            f.write(json.dumps(self.user_data))

        f.close()
        self.shutdown()

    def shutdown(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def validate_user(self):
        print(f"Hello, please state your username to begin.")
        self.voice.speak(f"Hello, please state your username to begin.")

        name = "Test"
        asking_confirm = False

        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                result_str = self.rec.Result()
                print(json.loads(result_str)["text"])

                # Implement commands here
                result = json.loads(result_str)
                if 'text' in result and not asking_confirm and self.validate_response(result, mode=2):
                    name = result["text"]
                    print(f"I heard {name}, is this correct?")
                    self.voice.speak(f"I heard {name}, is this correct?")
                    asking_confirm = True
                elif asking_confirm and 'text' in result and self.validate_response(result, mode=0):
                    if self.user_data is not None and name not in self.user_data:
                        print(f"I don't have a record of you, setting up new user...")
                        self.voice.speak(f"I don't have a record of you, setting up new user...")
                        self.setup_new_user()
                    elif self.user_data is not None and name in self.user_data:
                        self.initiate_user(name)
                    break
                elif asking_confirm and 'text' in result and self.validate_response(result, mode=1):
                    print("Please say your name again.")
                    self.voice.speak("Please say your name again.")
                    asking_confirm = False
                
        self.shutdown()

    def process_excercise_name(self, value):
        for phrase in {"bicep", "biceps", "curls", "curl"}:
            if phrase in value:
                value = "bicep curl"

        for phrase in {"push up", "pushups"}:
            if phrase in value:
                value = "push ups"

        for phrase in {"plank", "plink", "plonk", "plunk"}:
            if phrase in value:
                value = "planks"

        for phrase in {"squats", "squatting"}:
            if phrase in value:
                value = "squat"
        
        for phrase in {"downwards", "downward", "dog", "dogs"}:
            if phrase in value:
                value = "downward dog"

        for phrase in {"bench press", "benches"}:
            if phrase in value:
                value = "bench"

        for phrase in {"dead lift", "dead lif", "dead live", "dad live", "that lives", "del live"}:
            if phrase in value:
                value = "deadlift"

        print(f"Sanitized result: {value}")
        return value

    def initiate_user(self, name):
        print(f"Hello {name}, what exercises would you like to do?")
        self.voice.speak(f"Hello {name}, what exercises would you like to do?")

        asking_confirm = False
        chosen_exercise = ""
        
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                result_str = self.rec.Result()
                print(json.loads(result_str)["text"])
                result = json.loads(result_str)

                if "text" in result:
                    sanitized_response = self.process_excercise_name(result["text"].strip())
                    if "what" in result["text"]:
                        self.voice.speak(f"The available exercises are: bicep curl, push ups, planks, squat, downward dog, bench, deadlift")
                    elif "logout" in result["text"]:
                        self.setup_new_user()
                    elif sanitized_response in {"bicep curl", "push ups", "planks", "squat", "downward dog", "bench", "deadlift"}:
                        name = sanitized_response
                        print(f"I heard {name}, is this correct?")
                        self.voice.speak(f"I heard {name}, is this correct?")
                        chosen_exercise = name
                        asking_confirm = True
                    elif asking_confirm and self.validate_response(result, mode=0):
                        self.analyze_exercise(chosen_exercise)
                    elif asking_confirm and self.validate_response(result, mode=1):
                        self.voice.speak("Please say the exercise you want to do again.")
        self.shutdown()