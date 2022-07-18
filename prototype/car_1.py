#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Float32

def callback (velocity):
    print ("car 15 Velocity = " + str(velocity.data))


rospy.init_node("Car_1_Node")
sub = rospy.Subscriber('/15_ID',Float32,callback)
rospy.spin()