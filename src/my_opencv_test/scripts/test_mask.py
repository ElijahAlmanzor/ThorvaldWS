import cv2
import numpy as np

img = cv2.imread('green.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#convert to HSV

sensitivity = 15
green = 60

lower_color = np.array([green - sensitivity, 100, 50])
upper_color = np.array([green + sensitivity, 255, 255])

#threhold the HSV image to get only the green colours
mask = cv2.inRange(hsv, lower_color, upper_color)
#res is where it's 1 for the mask so displays only where its white from the image
res = cv2.bitwise_and(img,img,mask=mask)

cv2.imshow('green', img)
cv2.imshow('mask', mask)
cv2.imshow('res',res)

cv2.waitKey(0)
cv2.destroyAllWindows()