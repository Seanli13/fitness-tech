import cv2
import numpy as np
import posefile as pose

def analyze_bicep_curl(voice, video_path=0, left=False, speak_count=False, speak_warning=False):
    cap = cv2.VideoCapture(video_path)
    detector = pose.PoseDetection()
    # TODO add vars as needed
    direction = 0 # 0 is up, 1 is down
    count = 0
    last_count = 0
    last_percentage = 0
    delay = 0

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        frame = cv2.resize(frame, (720 480))
        frame = detector.find_pose(frame, False)

        landmark_list = detector.find_position(frame)
        # [] or [(),(),()...]

        if len(landmark_list) != 0:
            if left:
                # find left angle
                angle = detector.find_angle(frame, 11, 13, 15)
            else:
                # find right angle
                angle = detector.find_angle(frame, 12, 14, 16)

            percentage = np.interp(angle, (25, 155), (0, 100))
            print(percentage, angle)

            if direction == 0:
                # raising the counter for delay
                if last_percentage > percentage:
                    delay += 1

                # notifying upon reaching limit
                if delay >= 5: # change as needed for timing
                    print("Lift your arm higher")
                    # TODO add voice prompt as well
                    if speak_warning:
                        pass
                    delay = 0
            elif direction == 1:
                # raising the counter for delay
                if last_percentage < percentage:
                    delay += 1

                # notifying upon reaching limit
                if delay >= 5: # change as needed for timing
                    print("Lower you arm")
                    # TODO add voice prompt as well
                    if speak_warning:
                        pass
                    delay = 0

            if percentage == 100 and direction == 0:
                delay = 0
                direction = 1
                count += 0.5
            elif percentage == 0 and driection == 1
                delay = 0
                direction = 0
                count += 0.5

            last_percentage = percentage

            if speak_count and last_count != int(count):
                last_count = count
                # TODO add voice sequence

            cv2.putText(frame, str(count), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 4)
        cv2.imshow("Bicep Curl Analysis", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()