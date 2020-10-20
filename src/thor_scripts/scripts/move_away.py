#! /usr/bin/env python
import rospy
import numpy
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist 
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry

'''
class movement:
	def __init__(self):
		self.move = rospy.Publisher('/thorvald_001/twist_mux/cmd_vel', Twist, queue_size=10)
		self.rate = rospy.Rate(10)
		while not rospy.is_shutdown():
			self.laser = rospy.Subscriber('/thorvald_001/scan', LaserScan, self.callback)
			self.rate.sleep()
		#this is it, it takes the messages LaserScan!!

	def turn_bitch(self):
		#rate = rospy.Rate(10)
		Coordinate = Twist()
		Coordinate.linear.x= 2
		Coordinate.angular.z= 1.5
		self.move.publish(Coordinate)

	def callback(self,data):
		laser_data = data.ranges[330:390]
		#print(laser_data)
		#return laser_data
		#while not rospy.is_shutdown():
			#rate = rospy.Rate(10)
		Coordinate = Twist()
		Coordinate.linear.x= 2
			
		self.move.publish(Coordinate)
		for laser in laser_data:	
			if laser <= 5:
				self.turn_bitch()'''
	

class movement:
	def __init__(self):
		self.move = rospy.Publisher('/thorvald_001/twist_mux/cmd_vel', Twist, queue_size=1)
		self.laser_data = 0.0
		self.current_v = 0.0
		self.distance_moved = 0.0
		rospy.Subscriber('/thorvald_001/scan', LaserScan, self.callback)
		
		rospy.Subscriber('/thorvald_001/odometry/base_raw', Odometry, self.distance_callback)
		

	
	def distance_callback(self, data):

		self.current_v = numpy.sqrt(data.twist.twist.linear.x**2 + data.twist.twist.angular.z**2)
		#print(self.current_v)
		
	
	

	
	def callback(self, data):
		self.laser_data = min(data.ranges)


	def print_distance(self):
		rate = rospy.Rate(1)
		while not rospy.is_shutdown():
			print(self.current_v)
		rate.sleep()
	
	def move_forward(self):
		#rate = rospy.Rate(10)
		current_time = time.time()
		while not rospy.is_shutdown():
			Coordinate = Twist()
			
			if self.laser_data <= 3:
				Coordinate.angular.z= 2
			else:
			
				Coordinate.linear.x= 2
			self.move.publish(Coordinate)
			elapsed_time = time.time() - current_time
			if elapsed_time >= 1:
				#self.current_v = numpy.sqrt(Coordinate.linear.x**2 + Coordinate.angular.z**2)
				self.distance_moved += self.current_v
				print("Thorvald has now moved:" + str(self.distance_moved) + " metres")
				current_time = time.time()
			#rate.sleep()




		

if __name__ == '__main__':
	try:
		rospy.init_node('mover', anonymous=True)
		Thor = movement()
		Thor.move_forward()
		#Thor.print_distance()
		#rospy.spin()
		#Thor.move_forward()
		#rospy.spin()
	
		
	except rospy.ROSInterruptException:
		pass
