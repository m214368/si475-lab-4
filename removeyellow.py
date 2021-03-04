import cv2
import numpy as np
img = cv2.imread('imagefiles/balloon_yellow.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
outhsv = cv2.inRange(hsv, np.array([50/2, 20, 10]), np.array([70/2,255,235]))
img[:, :, 1] = np.bitwise_or(img[:, :, 1], outhsv)
cv2.imwrite('calculated/noyellowaugment.jpg', img)
cv2.imwrite('calculated/noyellowmap.jpg', outhsv)
