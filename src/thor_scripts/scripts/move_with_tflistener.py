#! /usr/bin/env python
import rospy
import math
import tf
import geometry_msgs.msg
from math import atan2, pi, cos, sin
import numpy as np
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry


class movement:
    def __init__(self):
        self.move = rospy.Publisher('/thorvald_001/twist_mux/cmd_vel', Twist, queue_size=1)
        self.listener = tf.TransformListener()
        self.pose_pub = rospy.Publisher('laser_scan_pose', PoseStamped, queue_size=1)
        self.laser_data = 0.0

        rospy.Subscriber('/thorvald_001/scan', LaserScan, self.callback)

    def callback(self, data):
        self.laser_data = min(data.ranges)
        arg_min = np.argmin(data.ranges)
        angle_increment = 0.00436940183863
        angle_min = -1.57079994678
        angle = angle_min + (arg_min*angle_increment)
        #laser scan rotates around the z axis so it is xy 2D hence z = 0
        laser_point_cartesian = [cos(angle)*self.laser_data, sin(angle)*self.laser_data, 0]

        laser_pose = PoseStamped() #just post stamped? because of from geometry_msgs.msg import PoseStamped
        laser_pose.header = data.header
        #something done in practice just to have timestamps etc.


        #For the cartesian coordinates of the laser points
        laser_pose.pose.position.x = laser_point_cartesian[0]
        laser_pose.pose.position.y = laser_point_cartesian[1]
        laser_pose.pose.position.z = laser_point_cartesian[2]

        #For the quaternion coordinates of the laser point
        laser_pose.pose.orientation.x = 0
        laser_pose.pose.orientation.y = 0
        laser_pose.pose.orientation.z = sin(angle/2)      
        laser_pose.pose.orientation.w = cos(angle/2)      


        #publish into the laser_scan_pose topic purely for RViz go visualise it
        self.pose_pub.publish(laser_pose)

        #print("The closest object wrt to laser scan frame")
        #print(laser_pose)

        #rospy.loginfo is the ros way of print - pretty sure it goes into ros logs as well
        rospy.loginfo(
            "The closest point in laser frame coords is at\n%s"
            % laser_pose.pose.position
            )
        #print("The closest object wrt to the baselink of the robot")
        laser_pose_in_base = self.listener.transformPose("thorvald_001/base_link", laser_pose)
        #print(laser_pose_in_base)

        rospy.loginfo(
            "The closest point in the robot base coords is at\n%s"
            % laser_pose_in_base.pose.position
            )
        #zero for z as the laser scan is in 2D!
        #laser scan doesnt have a frame id

        


    def move_func(self):


        while not rospy.is_shutdown():
            Coordinate = Twist()
            
            if self.laser_data <= 3:
                Coordinate.angular.z= 2
            else:
            
                Coordinate.linear.x= 2
            self.move.publish(Coordinate)
    
        


if __name__ == '__main__':
    try:
        rospy.init_node('mover', anonymous=True)
        Thor = movement()
        Thor.move_func()	
        
    except rospy.ROSInterruptException:
        pass
