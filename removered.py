import cv2
import numpy as np
img = cv2.imread('imagefiles/balloon_red.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
outhsv = cv2.inRange(hsv, np.array([-10/2, 20, 10]), np.array([10/2,255,235]))
img[:, :, 1] = np.bitwise_or(img[:, :, 1], outhsv)
cv2.imwrite('calculated/noredaugment.jpg', img)
cv2.imwrite('calculated/noredmap.jpg', outhsv)
