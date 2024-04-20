import cv2
import numpy as np
import posefile as pose

def analyze_bench(voice, video_path=0, speak_warning=False):
    cap = cv2.VideoCapture(video_path,cv2.CAP_DSHOW)
    detector = pose.PoseDetection()
    direction = 1 # 0 is up, 1 is down
    count = 0.5
    last_count = 0
    last_left_percentage = 0
    last_right_percentage = 0
    elbow_delay = 0
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
            left_elbow_angle = detector.find_angle(frame, 11, 13, 15)
            right_elbow_angle = detector.find_angle(frame, 12, 14, 16)

            left_percentage = np.interp(left_elbow_angle, (80, 160), (100, 0))
            right_percentage = np.interp(right_elbow_angle, (80, 160), (100, 0))

            # Direction Specific Checks
            if direction == 0: # we need to go up
                if last_left_percentage < left_percentage or last_right_percentage < right_percentage:
                    delay += 1
                
                if delay >= 5:
                    print("Keep going up!")
                    if speak_warning:
                        voice.speak("Keep going up!")
                    delay = 0
            elif direction == 1: # we need to go down
                if last_left_percentage > left_percentage or last_right_percentage > right_percentage:
                    delay += 1
                
                if delay >= 5:
                    print("Keep going down!")
                    if speak_warning:
                        voice.speak("Keep going down!")
                    delay = 0

            # General Checks
            if (abs(left_percentage - right_percentage) > 10):
                elbow_delay += 1

            if elbow_delay >= 5:
                print("Bar is not even! Watch your balance.")
                if speak_warning:
                    voice.speak("Bar is not even! Watch your balance.")
                elbow_delay = 0

        cv2.imshow("Bench Analysis", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
