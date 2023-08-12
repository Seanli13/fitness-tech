from voice import Voice
from bicep_curl import analyze_bicep_curl
from pushup import analyze_pushups
from plank import analyze_plank
from squat import analyze_squat
from downward_dog import analyze_downward_dog
from bench import analyze_bench
from deadlift import analyze_deadlift

class FitnessAnalyzer:
    def __init__(self):
        self.voice = Voice()

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