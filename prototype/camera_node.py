#!/usr/bin/env python3
from subprocess import list2cmdline
from tokenize import String
import rospy
import cv2
#from cv_bridge import CvBridge
from std_msgs.msg import String
import cv2.aruco as aruco
import numpy as np
from gp.msg import camera_info
import time
import tools
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import MultiArrayDimension


#for direction calculation
x1 = []
y1 = []
x2 = []
y2 = []
direction_vector = []

#-----------------------
list_ids=''
corners = 0
id = 0
#--for agumentation
VIDEO_SOURCE = 0
CAMERA_CAPTURE_FPS = 60
CAMERA_CAPTURE_WIDTH = 640
CAMERA_CAPTURE_HEIGHT = 480
timer = 1
def start_node():
    #------------initialize-----------------#
    global corners
    global id 
    #camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CAPTURE_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CAPTURE_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, CAMERA_CAPTURE_FPS)
    cap.set(cv2.CAP_PROP_EXPOSURE,10)
    cap.open
    rospy.init_node('camear_node')
    rospy.loginfo('camera_node started')
    #img=cv2.imread(filename)   reading image 
    #bridge=CvBridge()
    #imgMsg=bridge.cv2_to_imgmsg(img,'bgr8')   convert image to ros message 
    pub = rospy.Publisher('/car_info',Int32MultiArray,queue_size=10)

    #--------------loop---------------------#
    while not rospy.is_shutdown():
        complete_vector = []
        direction_iterator=0
        success, img = cap.read()
        car_array_publish = Int32MultiArray()
        corners,ids = tools.findArucoMarkers(img)
        car_list,all_points_tuple = tools.print_corners(corners,ids)
        
        #print(all_points_tuple)
        direction_vector = tools.get_direction_vector(all_points_tuple)
        if (car_list != -1) :
            car_number = len(car_list)
            for index in range (car_number):
                row_from_list = car_list[index][0:3]
                list_id = car_list[index][2]
                for i in range(car_number):
                    if list_id == int(direction_vector[i][1]):
                        row_from_list.append(direction_vector[i][0])
                        complete_vector.append(row_from_list)
        

       
        car_array = np.array(complete_vector)
        #print(car_array)
        #list of x,y,iD 
        

                        
    
        #print(direction_vector)



        
        
        
        #print(car_array)
        if(car_list != -1):
            car_vector_flatten = car_array.reshape(1,car_array.shape[0]*car_array.shape[1]) 
            #print(car_list_flatten)
            car_list_flatten = car_vector_flatten.tolist()
            car_array_publish.data = car_list_flatten[0]
            print(car_array_publish.data)
            pub.publish(car_array_publish)
            rospy.sleep(0.01)
        elif (car_list == -1):
            car_array_publish.data = [] 
            pub.publish(car_array_publish)

        cv2.imshow("image",img)
        cv2.waitKey(4) 
#---------------------------------------------------------------------#  
def camera_return():
    return [corners[0],id]







if __name__ == '__main__':
    print("main>>>>>>>>>>")
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass



