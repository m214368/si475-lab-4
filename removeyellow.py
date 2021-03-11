import cv2
import numpy as np
img = cv2.imread('imagefiles/balloon_yellow.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
outhsv = cv2.inRange(hsv, np.array([50/2, 20, 10]), np.array([70/2,255,235]))

# blue colored
#img[:, :, 0] = np.bitwise_or(img[:, :, 0], outhsv)

# green colored
img[:, :, 1] = np.bitwise_or(img[:, :, 1], outhsv)

# orange/red colored
#img[:, :, 2] = np.bitwise_or(img[:, :, 2], outhsv)
cv2.imwrite('noyellowaugment.jpg', img)
cv2.imwrite('noyellowmap.jpg', outhsv)
