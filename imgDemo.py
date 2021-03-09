import math, rospy
from turtleAPI import robot
import cv2
import numpy as np

# make the robot and lists for tracking error
r = robot()
error_list_pos = []
error_list_angle = []
pi = math.pi

# error function for angle
def angleDiff(cur_angle, desired):
    # calculate difference
    diff = cur_angle - desired
    # bind between pi and -pi
    while diff > pi:
        diff -= 2*pi
    while diff < -pi:
        diff += 2*pi

    if (abs(diff) < .1):
        if diff > 0: return .1
        if diff < 0: return -.1

    if (abs(diff) > 3):
        if diff > 0: return 3
        if diff < 0: return -3

    return diff

# error function for position
def posDiff(current, desired):
    # calculate component differences
    x_diff = current[0] - desired[0]
    y_diff = current[1] - desired[1]

    #calculate the total distance
    return (x_diff**2 + y_diff**2)**.5

# pid
def pid_speed(kp, ki, kd, error, old_error, error_list):

    # add the error to the integral portion
    if len(error_list) > 5:
        error_list.pop()
        error_list.append(error)

    # calculate sum
    error_sum = 0
    for i in error_list:
        error_sum += i

    # kp portion + ki portion
    to_return = (kp * error) + (ki * error_sum)
    to_return += kd * (error - old_error)

    return to_return

def hunt(color):
    speed_limit = 4 # speed limit
    colormap = {"blue":[210,240],"green":[130,160],"purple":[300,310],"red":[-10,10],"yellow":[50,70]}
    bot = np.array([colormap[color][0]/2, 20, 10])
    top = np.array([colormap[color][1]/2,255,235])

    rate = rospy.Rate(10)

    # inital camera setup
    cur_pos = r.getPositionTup()
    cur_ang = cur_pos[2]
    image = r.getImage()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mapimage = cv2.inRange(hsv, bot, top)
    augimage = image
    augimage[:, :, 1] = np.bitwise_or(image[:, :, 1], mapimage)
    # cv2.imshow('normal',image)
    # cv2.imshow('mapped',mapimage)
    cv2.imshow('augmented',augimage)
    cv2.waitKey(1)

    # initial spin to find largest color blob
    cur_pos = r.getPositionTup()
    init_ang = cur_pos[2]
    size = 0
    for i in (pi/2,pi,3*pi/2,2*pi):
        while True:
            cur_pos = r.getPositionTup()
            cur_ang = cur_pos[2]
            image = r.getImage()
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mapimage = cv2.inRange(hsv, bot, top)
            augimage = image
            augimage[:, :, 1] = np.bitwise_or(image[:, :, 1], mapimage)
            cv2.imshow('augmented',augimage)
            cv2.waitKey(1)
            height, width = mapimage.shape[0:2]
            total = cv2.countNonZero(mapimage)
            if total > size:
                size = total
            width = width//2
            halfLeft = mapimage[:,:width]
            left = cv2.countNonZero(halfLeft)
            halfRight = mapimage[:,width:]
            right = cv2.countNonZero(halfRight)
            print ("total: "+str(total)+" left: "+str(left)+" right: "+str(right))
            r.drive(angSpeed=2, linSpeed=0)
            if ( abs(cur_ang-init_ang) > i):
                print("quarter turn done" + str(i))
                break
            rate.sleep()

    r.drive(angSpeed=0, linSpeed=0)
    print("done with spin")
    print("largest blob",size)

    # loop until at position
    old_ang_error = 0
    old_pos_error = 0

    while True:
        image = r.getImage()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mapimage = cv2.inRange(hsv, bot, top)
        augimage = image
        augimage[:, :, 1] = np.bitwise_or(image[:, :, 1], mapimage)
        cv2.imshow('augmented',augimage)
        cv2.waitKey(1)
        # current pos
        current_pos = r.getPositionTup()
        print('current pos: ' + str(current_pos))
        current_angle = current_pos[2]
        
        # calculate the goal angle
        relative_x = goal_pos[0]-current_pos[0]
        relative_y = goal_pos[1]-current_pos[1]
        goal_angle = math.atan2(relative_y, relative_x)
        print('goal angle: ' + str(goal_angle))
        # break if within .1 m
        if (posDiff(current_pos, goal_pos) < .1 ):
            break

        # calculate angle speed and lin speed drive
        ang_error = angleDiff(current_angle, goal_angle)
        pos_error = posDiff(current_pos, goal_pos)
        print('error: ' + str(ang_error) + ' ' +str(pos_error))

        # speed
        ang_speed = pid_speed(-.1, 0, -.01, ang_error, old_ang_error, error_list_angle)
        lin_speed = pid_speed(.05, 0, .01, pos_error, old_pos_error, error_list_pos)

        # set speed limit
        if lin_speed > speed_limit:
            lin_speed = speed_limit

        r.drive(angSpeed=ang_speed, linSpeed=lin_speed)
        print('speed: ' + str(ang_speed) + ' ' + str(lin_speed))

        # set old values
        old_ang_error=ang_error
        old_pos_error=pos_error
        rate.sleep()
        print(' ')

def Blob(): 
    # https://learnopencv.com/blob-detection-using-opencv-python-c/
    # https://www.geeksforgeeks.org/find-circles-and-ellipses-in-an-image-using-opencv-python/
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
    
    # Change thresholds
    params.minThreshold = 10;
    params.maxThreshold = 200;

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 1500

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
        detector = cv2.SimpleBlobDetector(params)
    else :
        detector = cv2.SimpleBlobDetector_create(params)

color = raw_input("What color to hunt:")
while True:
    hunt(color)

