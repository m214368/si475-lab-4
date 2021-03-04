import cv2
import numpy as np
img = cv2.imread('purp.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
outhsv = cv2.inRange(hsv, np.array([300/2, 15, 20]), np.array([310/2, 255, 255]))
img[:, :, 1] = np.bitwise_or(img[:, :, 1], outhsv)
cv2.imwrite('nopurpaugment.jpg', img)
cv2.imwrite('nopurp.jpg', outhsv)
