import cv2
import numpy as np
import time
from myro import *

init("/dev/tty.Fluke2-0B3B-Fluke2")

class Intruder:
    MOVING = 0
    STATIONARY = 1

#take a image and find the countours of the red cylinder
def findContours():
    
    setPicSize("small")
    image = takePicture()
    savePicture(image, "image.jpg")

    image = cv2.imread("image.jpg")
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 80, 80])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    transformed = cv2.bitwise_and(image, image, mask=mask)
    edges = cv2.Canny(transformed, 100, 100)
    blurred = cv2.filter2D(edges, -1, np.ones((2, 2), np.float32)/4)
    targets = cv2.findContours(blurred.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    targets = sorted(targets, key=cv2.contourArea, reverse=True)
    
    center = (0,0)
    radius = 0
    if len(targets) == 0:
        return targets, center

    cnt = targets[0]
    (x,y), radius = cv2.minEnclosingCircle(cnt)
    radius = int(radius)
    center = (int(x), int(y))
    cv2.circle(image,center,radius,(0,255,0),2)
    
    print center, radius
    return targets, center, radius


#cv2.minEnclosingCirle()

#have robot rotate and look for intruder
def search():
    targets, center, radius = findContours()
    if(len(targets) == 0):
        checkWall()
        turnBy(30, "deg")
        search()

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
    # start = time.time()
    # current = time.time()
    # elapsed = current - start


    print "started"
    #first two minutes
    #when intruder is stationary
    moveToIntruder()

    # #last 3 minutes
    # #when intruder is moving
    # while(elapsed < 300):
    #     moveToIntruder()















