import cv2
import numpy as np
import posefile as pose

def analyze_pushups(voice, video_path=0, left=False, speak_count=False, speak_warning=False):
    cap = cv2.VideoCapture(video_path)
    detector = pose.PoseDetection()
    direction = 1 # 0 is up, 1 is down
    count = 0
    last_count = 0
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
            # elbow angle
            elbow_angle = detector.find_angle(frame, 12, 14, 16)
            # leg angle
            leg_angle = detector.find_angle(frame, 24, 26, 28)
            # hip angle
            hip_angle = detector.find_angle(frame, 12, 24, 26)
            
            percent = np.interp(elbow_angle, (80, 160), (100, 0))

            # print(percentage)

            if direction == 0:
                if leg_angle < 160: # bad leg
                    pass
            elif direction == 1:
                pass