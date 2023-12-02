import cv2

cap = cv2.VideoCapture(0)

print(cap.isOpened())

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        print("Could not get frame.")
        break

    cv2.imshow("Bench Analysis", frame)
    cv2.waitKey(0)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

cap.release()
cv2.destroyAllWindows()