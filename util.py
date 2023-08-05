from datetime import datetime

def countdown(duration, voice=None):
    start_time = datetime.now()
    next_second = 1
    print(duration)
    while ((datetime.now() - start_time).total_seconds() <= duration):
        if (datetime.now() - start_time).total_seconds() >= next_second:
            if duration - next_second == 0:
                print("Start!")
                voice.speak("Start!")
            else:
                print(duration - next_second)
                voice.speak(f"{duration - next_second}")
            next_second += 1