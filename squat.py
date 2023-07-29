import cv2
import numpy as np
import posefile as pose

def analyze_squat(voice, video_path=0, speak_warning=False):
    cap = cv2.VideoCapture(video_path)
    detector = pose.PoseDetection()

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            print("Could not get frame.")
            break

        frame = cv2.resize(frame, (720, 480))
        frame = detector.find_pose(frame, False)

        landmark_list = detector.find_position(frame)

        if len(landmark_list) != 0:
            pass 

        #12 24 26 28 or 11 23 25 27