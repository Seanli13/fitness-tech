# Boot up the analyzer
from analyzer import FitnessAnalyzer
import json

# Open and read the contents of your text file
with open('user.txt', 'r') as file:
    content = file.read()

# Load the JSON content into a Python dictionary
data = json.loads(content)
file.close()

# Initialize the Fitness Analyzer
fitness = FitnessAnalyzer(data)

# Now, 'data' contains the dictionary with the contents from your file
if len(data) > 0:
    print(f"{len(data)} user(s) found!")
    fitness.validate_user()
else:
    print("No user found, setting up new user.")
    fitness.setup_new_user()
# fitness.analyze_exercise(exercise_type="deadlift") # provide video path if file






















# import cv2
# import numpy as np

# grey_image = cv2.imread("OIP.jpg", 0)
# regular_image = cv2.imread("OIP.jpg")
# # cv2.imshow("Grey Image", grey_image)
# # cv2.imshow("Original Image", regular_image)

# # cv2.waitKey()

# width = 100
# height = 1000
# new_size = (width, height)
# resized_image = cv2.resize(regular_image, new_size, interpolation=cv2.INTER_LINEAR)

# scale_x = 0.75
# scale_y = 0.5

# scaled_image = cv2.resize(regular_image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_AREA)
# cubic_image = cv2.resize(regular_image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_CUBIC)
# linear_image = cv2.resize(regular_image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_LINEAR)
# nearest_image = cv2.resize(regular_image, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_NEAREST)

# # cv2.imshow("Resized Image", resized_image)
# # cv2.imshow("area Image", scaled_image)
# # cv2.imshow("cubic Image", cubic_image)
# # cv2.imshow("linear Image", linear_image)
# # cv2.imshow("nearest Image", nearest_image)

# horizontal = np.concatenate((scaled_image, cubic_image, linear_image, nearest_image), axis=1)
# # cv2.imshow("Collection", horizontal)

# vertical = np.concatenate((scaled_image, cubic_image, linear_image, nearest_image), axis=0)
# # cv2.imshow("Collection", vertical)

# # cv2.waitKey(0)

# # cv2.destroyAllWindows()

# # cv2.imwrite("grey_image.jpg", grey_image)


# video_capture = cv2.VideoCapture("rabbit.mp4")
# webcam_feed = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# if (video_capture.isOpened() == False):
#     print("Error opening file")
# else:
#     width = int(video_capture.get(3))
#     height = int(video_capture.get(4))
#     frame_size = (width, height)

#     # fps = video_capture.get(5)
#     fps = 5

#     print(f"Video FPS: {fps} fps")

#     frame_count = video_capture.get(7)
#     print(f"Frame Count: {frame_count}")

#     output = cv2.VideoWriter("newvideo.mp4", cv2.VideoWriter_fourcc("m", "p", "4", "v"), fps, frame_size)

#     while(video_capture.isOpened()):
#         ret, frame = video_capture.read()
#         if ret:
#             output.write(frame)
#             cv2.imshow("frame", frame)
#             key = cv2.waitKey(20)

#             if key == ord('q'):
#                 break
#         else:
#             print("stream disconnected")
#             break

# # while(True):
# #     ret, frame = webcam_feed.read()
# #     cv2.imshow("frame", frame)

# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# video_capture.release()
# webcam_feed.release()
# cv2.destroyAllWindows()