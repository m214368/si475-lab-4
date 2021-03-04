import cv2
import numpy as np
img = cv2.imread('imagefiles/balloon_green.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
outhsv = cv2.inRange(hsv, np.array([130/2, 20, 10]), np.array([160/2,255,235]))
img[:, :, 1] = np.bitwise_or(img[:, :, 1], outhsv)
cv2.imwrite('calculated/nogreenaugment.jpg', img)
cv2.imwrite('calculated/nogreenmap.jpg', outhsv)
