from voice import Voice
from bicep_curl import analyze_bicep_curl

class FitnessAnalyzer:
    def __init__(self):
        self.voice = Voice()

    def analyze_exercise(self, exercise_type: str, video_path=0):
        if exercise_type == 'bicep_curl':
            analyze_bicep_curl(self.voice, video_path=video_path)