#!/usr/bin/env python

import rospy
import cv2
from cv2 import namedWindow, cvtColor, imshow, resizeWindow
from cv2 import destroyAllWindows
from cv2 import COLOR_BGR2HSV, waitKey
from cv2 import blur, Canny
import numpy as np
from numpy import mean
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class image_converter:

    def __init__(self):

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/thorvald_001/kinect2_camera/hd/image_color_rect", Image, self.image_callback)
        self.plant_pub = rospy.Publisher('green_plant_mask', Image, queue_size=1)

        #Obviously something needs to be publishing on the topic for the camera code to work

    def image_callback(self, data):
        namedWindow("Thorvald Kinect Feed", cv2.WINDOW_NORMAL)
        
        namedWindow("Mask", cv2.WINDOW_NORMAL)
        resizeWindow("Mask", 640,480)
        namedWindow("Result", cv2.WINDOW_NORMAL)
        resizeWindow("Result", 640, 480)

        sensitivity = 15
        green = 60

        lower_color = np.array([green - sensitivity, 100, 50])
        upper_color = np.array([green + sensitivity, 255, 255])
        cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        
        #This converts the messages back into (cv) images

        #Converts the cv image into suitable form
        hsv = cvtColor(cv_image, COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_color, upper_color)
        res = cv2.bitwise_and(cv_image,cv_image,mask=mask)

        #mask_pub = cvtColor(mask, )
        res_pub = self.bridge.cv2_to_imgmsg(res, "passthrough")
        #print(mean(mask))
        imshow("Thorvald Kinect Feed", cv_image)
        resizeWindow("Thorvald Kinect Feed", 640, 480)
        imshow('Mask', mask)
        imshow('Result', res)
        

        if mean(mask) > 3.0:
            rospy.loginfo(
            "I HAVE DETECTED PLANT!"
            )

            #Write a quick code that publishes to a topic the image
            self.plant_pub.publish(res_pub)
        waitKey(1)

#startWindowThread() #for some reason ubuntu hates this
rospy.init_node('image_converter')
ic = image_converter()
rospy.spin()

destroyAllWindows()