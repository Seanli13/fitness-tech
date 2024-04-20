import cv2
import numpy as np
import posefile as pose
import util

def analyze_pushups(voice, video_path=0, left=False, speak_count=False, speak_warning=False):
    cap = cv2.VideoCapture(video_path,cv2.CAP_DSHOW)
    detector = pose.PoseDetection()
    direction = 1 # 0 is up, 1 is down
    count = 0.5
    last_count = 0
    last_percentage = 0
    leg_delay = 0
    hip_delay = 0
    elbow_delay = 0
    delay = 0

    util.countdown(3, voice)

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
            
            percentage = np.interp(elbow_angle, (80, 160), (100, 0))

            # print(percentage)

            # Direction Specific Checks
            if direction == 0:
                if last_percentage < percentage:
                    delay += 1

                if delay >= 5:
                    print("Keep going up!")
                    if speak_warning:
                        voice.speak("Keep going up")
                    delay = 0
            elif direction == 1:
                if last_percentage > percentage:
                    delay += 1

                if delay >= 5:
                    print("Keep going down!")
                    if speak_warning:
                        voice.speak("Keep going down")
                    delay = 0

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
            if elbow_angle <= 70 and direction == 1: # bent
                direction = 0
                count += 0.5

            if elbow_angle >= 170 and direction == 0: # Note: adjust if needed
                direction = 1
                count += 0.5

            if last_count != int(count):
                last_count = count
                voice.speak(last_count)

            last_percentage = percentage

            cv2.putText(frame, f"{int(count)}", (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 4)
        cv2.imshow("Pushup Analysis", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()