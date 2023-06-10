import cv2

grey_image = cv2.imread("OIP.jpg", 0)
cv2.imshow("Grey Image", grey_image)

cv2.waitKey(0)

cv2.destroyAllWindows()

cv2.imwrite("grey_image.jpg", grey_image)