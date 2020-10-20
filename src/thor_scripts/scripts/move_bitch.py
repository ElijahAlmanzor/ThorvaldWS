#! /usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist 

'''
def mover():
	move = rospy.Publisher('/thorvald_001/twist_mux/cmd_vel', Twist, queue_size=10)
	rospy.init_node('mover', anonymous=True)
	rate = rospy.Rate(10) #10 Hz
	while not rospy.is_shutdown():
		Coordinate = Twist()
		#print(Coordinate)
		Coordinate.linear.x = 0.5
		Coordinate.angular.z = 0.5
		#rospy.loginfo(hello_str)
		move.publish(Coordinate)
		rate.sleep()
'''

class movement:
	def __init__(self):
		self.move = rospy.Publisher('/thorvald_001/twist_mux/cmd_vel', Twist, queue_size=10)
		#message to cmd_vel is what makes it move


	def move_bitch(self):
		rate = rospy.Rate(10)
		while not rospy.is_shutdown():

			Coordinate = Twist()
			Coordinate.linear.x= 2
			Coordinate.angular.z=0.5
			self.move.publish(Coordinate)
			rate.sleep()

if __name__ == '__main__':
	try:
		rospy.init_node('mover', anonymous=True)
		Thor = movement()
		Thor.move_bitch()
		
	except rospy.ROSInterruptException:
		pass
