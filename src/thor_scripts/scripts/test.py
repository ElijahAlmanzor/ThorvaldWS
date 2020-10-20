#! /usr/bin/env python
import rospy
from std_msgs.msg import String
import psutil


print(str(psutil.virtual_memory().percent))
