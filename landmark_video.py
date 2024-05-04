import cv2
import mediapipe as mp

def draw_landmarks_on_video(input_file, output_file):
    # Load the video file
    video = cv2.VideoCapture(input_file)

    # Create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Initialize the MediaPipe model
    model = mp.solutions.pose.Pose(
        static_image_mode=False, 
        model_complexity=1, 
        smooth_landmarks=True, 
        enable_segmentation=False,
        smooth_segmentation=True,
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5)

    while True:
        # Read a frame from the video
        ret, frame = video.read()
        if not ret:
            break

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect landmarks on the frame
        results = model.process(frame_rgb)

        # Draw the landmarks on the frame
        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        # Convert the frame back to BGR
        # frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Show the frame
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Write the frame to the output video
        output.write(frame)

    # Release the video capture and writer objects
    video.release()
    output.release()

    # Close the MediaPipe FaceMesh model
    model.close()

# Usage example
input_file = 'videos/bench_press.mp4'
output_file = 'videos/output.mp4'
draw_landmarks_on_video(input_file, output_file)