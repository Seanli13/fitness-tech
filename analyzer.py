# TODO import voice functionality
from bicep_curl import analyze_bicep_curl

class FitnessAnalyzer:
    def __init__(self):
        pass
        #TODO import voice

    def analyze_exercise(self, exercise_type: str, video_path=0):
        if exercise_type == 'bicep_curl':
            analyze_bicep_curl(None, video_path=video_path)