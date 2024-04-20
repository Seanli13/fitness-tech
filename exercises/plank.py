import cv2
import numpy as np
import posefile as pose
import util
from datetime import datetime

def analyze_plank(voice, video_path=0, speak_warning=False, straight_arm=True):
    cap = cv2.VideoCapture(video_path,cv2.CAP_DSHOW)
    detector = pose.PoseDetection()
    leg_delay = 0
    hip_delay = 0
    elbow_delay = 0

    util.countdown(3, voice)

    start_time = datetime.now()
    interval_start = start_time
    timer_interval = 30

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
            

            # General Checks
            if leg_angle < 160:
                    leg_delay += 1
            if leg_delay >= 5:
                print("Straighten your legs")
                if speak_warning:
                    voice.speak("Straighten your legs")
                leg_delay = 0
            if hip_angle < 170:
                hip_delay += 1
            if hip_delay >= 10:
                print("Straighten your back")
                if speak_warning:
                    voice.speak("Straighten your back")
                hip_delay = 0
                
            # elbow logic
            if (straight_arm and elbow_angle < 170) or (not straight_arm and not 75 <= elbow_angle <= 105): # bent
                elbow_delay += 1

            if elbow_delay >= 10:
                if straight_arm:
                    print("Straighten your arms")
                    if speak_warning:
                        voice.speak("Straighten your arms")
                else:
                    print("Move your shoulder above your elbow")
                    if speak_warning:
                        voice.speak("Move your shoulder above your elbow")
                elbow_delay = 0


            if (datetime.now() - interval_start).total_seconds() >= timer_interval:
                interval_start = datetime.now()
                voice.speak(f"{(datetime.now() - start_time).total_seconds()} seconds have passed!")

            # cv2.putText(frame, f"{int(count)}", (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 4)
        cv2.imshow("Pushup Analysis", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()