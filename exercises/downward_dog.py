import cv2
import numpy as np
import posefile as pose

def analyze_downward_dog(voice, video_path=0, speak_warning=False):
    cap = cv2.VideoCapture(video_path)
    detector = pose.PoseDetection()
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = fps * 5


    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            print("Could not get frame.")
            break

        frame = cv2.resize(frame, (720, 480))
        frame = detector.find_pose(frame, False)

        landmark_list = detector.find_position(frame)

        if len(landmark_list) != 0:
            # elbow angle
            elbow_angle = detector.find_angle(frame, 12, 14, 16)
            # leg angle
            leg_angle = detector.find_angle(frame, 24, 26, 28)
            # hip angle
            hip_angle = detector.find_angle(frame, 12, 24, 26)

            if hip_angle:
                pass