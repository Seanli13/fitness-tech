import math
import cv2
import mediapipe as mp

class PoseDetection:
    def __init__(self,
                 static_image_mode=False, # True for videos, false for unrelated
                 model_complexity=1, # can be set to 0,1,2 time vs precision
                 smooth_landmarks=True, # reduce landmark jitter
                 enable_segmentation=False, # toggle use of segmentation
                 smooth_segmentation=True, # reduce mask jitter
                 min_detection_confidence=0.5, # min value where success is considered
                 min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_segmentation
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, self.model_complexity, self.smooth_landmarks, self.enable_segmentation, self.smooth_segmentation, self.min_detection_confidence, self.min_tracking_confidence)

    def find_pose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        # use results
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def find_position(self, img, draw=True):
        self.lmList = []

        if self.results.pose_landmarks:
            for idx, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                x, y = int(lm.x * w), int(lm.y * h)
                self.lmList.append(idx, x, y)
                if draw:
                    cv2.circle(img, (x, y), 5, (255, 0, 0), cv2.FILLED)
        else:
            print("There are no landmarks at this time! Please call find_pose() first if there should be.")

        return self.lmList

    def find_angle(self, img, p1, p2, p3, draw=True):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p2][1:]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # Note: might have issues, deal with later if so

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (230, 99, 0), 1)
            cv2.line(img, (x3, y3), (x2, y2), (230, 99, 0), 1)
            cv2.circle(img, (x1, y1), 5, (54, 54, 186), cv2.FILLED)
            cv2.circle(img, (x2, y2), 5, (54, 54, 186), cv2.FILLED)
            cv2.circle(img, (x3, y3), 5, (54, 54, 186), cv2.FILLED)
            cv2.putText(img, f"{int(angle)}°", (x2 + 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (58, 186, 54), 2)

        return angle
