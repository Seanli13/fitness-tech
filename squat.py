import cv2
import numpy as np
import posefile as pose

def analyze_squat(voice, video_path=0, speak_warning=False):
    cap = cv2.VideoCapture(video_path)
    detector = pose.PoseDetection()
    direction = 1
    count = 0.5
    last_count = 0
    last_percentage = 0
    hip_delay = 0
    knee_delay = 0
    delay = 0

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            print("Could not get frame.")
            break

        frame = cv2.resize(frame, (720, 480))
        frame = detector.find_pose(frame, False)

        landmark_list = detector.find_position(frame)

        if len(landmark_list) != 0:
            hip_angle = detector.find_angle(frame, 12, 24, 26)
            knee_angle = detector.find_angle(frame, 24, 26, 28)

            # TODO: determine correct numbers through testing
            percentage = np.interp(knee_angle, (80, 160), (100, 0))

            # Direction Specifc Checks
            if direction == 0:
                if last_percentage < percentage:
                    delay += 1
            else:
                if last_percentage > percentage:
                    delay += 1

            if delay >= 5:
                if direction == 0:
                    print("Keep going up!")
                    if speak_warning:
                        voice.speak("Keep going up")
                else:
                    print("Keep going down!")
                    if speak_warning:
                        voice.speak("Keep going down")

            # General Checks
            if hip_angle < 50:
                hip_delay += 1
            if knee_angle < 50:
                knee_delay += 1

            if hip_delay >= 10 or knee_delay >= 10:
                print("You are going too low!")
                if speak_warning:
                    voice.speak("You are going too low!")
                hip_delay = 0
                knee_delay = 0

        #12 24 26 28 or 11 23 25 27