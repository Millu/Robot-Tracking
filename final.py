import cv2
import numpy as np
from myro import *


init("/dev/tty.Fluke2-0B3B-Fluke2")

class Intruder:
    MOVING = 0
    STATIONARY = 1

#take in a image and find the countours of the red cylinder
def findContours():
    img = takePicture()
    img = cv2.imRead(img)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 80, 80])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    transformed = cv2.bitwise_and(image, image, mask=mask)
    edges = cv2.Canny(filtered, 100, 100)
    targets = cv2.findContours(blurred.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    targets = sorted(targets, key=cv2.contourArea, reverse=True)
    return targets

#have robot rotate and look for intruder
def search():
    targets = findContours()
    while(len(targets) == 0):
        turnBy(20, "deg")
        targets = findContours()
`

def moveToIntruder():
    forward(1,3)
    search()

#have robot center itself
def reorient(img):



def checkWall():
    distance = getObstacle()
    while(distance[0] > 6400):
        backward(1,.4)
        turnBy(30, "deg")




if __name__ == '__main__':
    