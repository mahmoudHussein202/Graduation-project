#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import String


rospy.init_node("algorithm_node")
sub = rospy.Publisher("/phrase2",String,queue_size=10)
while (1):
    message = String()
    message.data = "data"
    sub.publish(message)
