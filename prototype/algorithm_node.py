#!/usr/bin/env python3
import numpy as np
import rospy
import tools
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Float32




def callback (car_info_message):
    car_array_inscene = tools.get_array_from_message(car_info_message)
    print(car_array_inscene)
    x_center = 638/2 
    y_center = 478/2 
    car_1 = rospy.Publisher('/15_ID',Float32,queue_size=10)
    car_2 = rospy.Publisher('/16_ID',Float32,queue_size=10)
    car_3 = rospy.Publisher('/17_ID',Float32,queue_size=10)
    car_4 = rospy.Publisher('/18_ID',Float32,queue_size=10)
    
    message = Float32()
    if not rospy.is_shutdown():
        if car_array_inscene[0][0] < y_center :
            message.data = 0
        elif car_array_inscene[0][0] > y_center:
            message.data = 0.4
        car_2.publish(message)

    #print(car_array_inscene)
    



rospy.init_node("algorithm_node")
sub = rospy.Subscriber('/car_info',Int32MultiArray,callback)
rospy.spin()

