#! /usr/bin/env python
import rospy
from std_msgs.msg import String
import psutil
def ram_talker():
	pub = rospy.Publisher('freemem', String, queue_size=10)
	rospy.init_node('ram_talker', anonymous=True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		ram_percent = ('Using up this much ram: %s'%str(psutil.virtual_memory().free))
		pub.publish(ram_percent)
		rate.sleep()




if __name__ == '__main__':
	try:
		ram_talker()
	except rospy.ROSInterruptException:
		pass
