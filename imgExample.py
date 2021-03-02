import rospy
from turtleAPI import robot
import cv2

try:
  print("creating robot")
  r= robot()
  while not rospy.is_shutdown():
    dpth=r.getDepth()
    img=r.getImage()
    cv2.imshow("Depth",dpth)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
except Exception as e:
  print(e)
  rospy.loginto("node now terminated")
