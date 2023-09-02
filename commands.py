# https://alphacephei.com/vosk/models

import os
import pyaudio
import json
from vosk import Model, KaldiRecognizer

def initialize_voice_commands():
    # Setup Vosk
    if not os.path.exists("vosk-model-small-en-us-0.15"):
        print("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit(1)

    model = Model("vosk-model-small-en-us-0.15")
    rec = KaldiRecognizer(model, 16000)

    # Setup PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input = True, frames_per_buffer=8000)
    stream.start_stream()

    print("Listening... 'stop' to terminate")

    while True:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result_str = rec.Result()
            print(result_str)

            # Implement commands here
            result = json.loads(result_str)
            if 'text' in result and 'stop' in result['text']:
                print("Terminating...")
                break

    stream.stop_stream()
    stream.close()
    p.terminate()