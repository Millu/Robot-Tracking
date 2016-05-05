import cv2
import numpy as np
import time
from myro import *

init("/dev/tty.Fluke2-0B3B-Fluke2")

class Intruder:
    MOVING = 0
    STATIONARY = 1

lastSeen = "n"

#take a image and find the countours of the red cylinder
def findContours():
    
    setPicSize("small")
    pic = takePicture()
    image = np.array(pic.image.convert('RGB'))
    

    # savePicture(image, "image.jpg")
    # image = cv2.imread("image.jpg")

    # blur = cv2.medianBlur(image,5)
    # hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    # red = cv2.inRange(hsv, np.array(np.array((0, 100, 100))), np.array((10, 255, 255)))
    # erode = cv2.erode(red,None,iterations = 3)
    # dilate = cv2.dilate(erode,None,iterations = 10)
    # contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # targets = sorted(contours, key=cv2.contourArea, reverse=True)
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    
    # output_img = hsv.copy()
    # output_img[np.where(mask==0)] = 0
    # cv2.imshow("",output_img)
    # cv2.waitKey(1000)
    # mask1 = cv2.inRange(hsv, np.array([0, 90, 30]), np.array([10, 255, 255]))
    # mask2 = cv2.inRange(hsv, np.array([170, 90, 30]), np.array([180, 255, 255]))
    # mask = mask1+mask2
    transformed = cv2.bitwise_and(image, image, mask = mask)
    # cv2.imshow('transformed', transformed)
    edges = cv2.Canny(transformed, 100, 100)
    # cv2.imshow('edges', edges)
    blurred = cv2.filter2D(edges, -1, np.ones((2, 2), np.float32)/4)
    # cv2.imshow('blurred', blurred)
    targets = cv2.findContours(blurred.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    targets = sorted(targets, key=cv2.contourArea, reverse=True)
    

    
    # cv2.imshow('img',image)
    center = (0,0)
    radius = 0
    if len(targets) == 0:
        return targets, center, radius

    cnt = targets[0]
    (x,y), radius = cv2.minEnclosingCircle(cnt)
    radius = int(radius)
    center = (int(x), int(y))
    # cv2.circle(image,center,radius,(0,255,0),2)
    # cv2.imshow('image_final', image)
    # print "center", center, "radius:", radius
    return targets, center, radius


#cv2.minEnclosingCirle()

#have robot rotate and look for intruder
def search():
    targets, center, radius = findContours()
    if(len(targets) == 0 or radius <= 8):
            checkWall()
            turnRight(1, .2)        
            stop()
            search()            
    else:
        # stop()
        origin = (214, 133)
        diff = center[0] - origin[0]
        print "diff: ", diff
        if diff <= 10 and diff >= -10:
            translate(1)
            # forward(1, 2)
        else:
            stop()
            theta = float(diff) / -9.0
            if(abs(theta) > 7):
                turnBy(int(theta), "deg")
            #fwd = 2
            #fwd = float(radius) / 20
            print "fwd: ", fwd
            translate(1)
            # forward(1, fwd) 
        '''elif diff > 10 and diff <= 78:
            #move(1, -.5)
            #trun right a bit
            turnBy(-10, "deg")
        elif diff > 78 and diff <= 146:
            #turn right a bunch
            turnBy(-15, "deg")
        elif diff > 146 and diff <= 214:
            #turn right a ton
            turnBy(-20, "deg")
        elif diff < -10 and diff >= -78:
            #trun left a bit
            turnBy(10, "deg")
        elif diff < -78 and diff >= -146:
            #turn left a bunch
            turnBy(15, "deg")
        elif diff < -146 and diff >= -214:
            #turn left a ton
            turnBy(20, "deg")'''

#check if infront of a wall
def checkWall():
    distance = getObstacle()
    while(distance[0] > 6400):
        backward(1,.4)
        turnBy(30, "deg")

#move towards intruder
def moveToIntruder():
    search()


# TODO
# segment the image 
# smooth turning based on segement of the image blob is in
# move distance based on how far the blob is based on size   

if __name__ == '__main__':

    # print "battery: ", getBattery()
    print "started"
    while True:
    #    search()
    #moveToIntruder()
        search()














