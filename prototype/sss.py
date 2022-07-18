#!/usr/bin/env python3
from subprocess import list2cmdline
from tokenize import String
import rospy
from cv_bridge import CvBridge
from std_msgs.msg import String
import cv2.aruco as aruco
import numpy as np
from gp.msg import camera_info
import tools
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import MultiArrayDimension
# import the necessary packages
from threading import Thread
import sys
from imutils.video import FileVideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
	from queue import Queue
# otherwise, import the Queue class for Python 2.7
else:
	from Queue import Queue


class FileVideoStream:
	def __init__(self, path, queueSize=128):
		# initialize the file video stream along with the boolean
		# used to indicate if the thread should be stopped or not
		self.stream = cv2.VideoCapture(path)
		self.stopped = False
		# initialize the queue used to store frames read from
		# the video file
		self.Q = Queue(maxsize=queueSize)

	def start(self):
		# start a thread to read frames from the file video stream
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self


	def update(self):
		# keep looping infinitely
		while True:
			# if the thread indicator variable is set, stop the
			# thread
			if self.stopped:
				return
			# otherwise, ensure the queue has room in it
			if not self.Q.full():
				# read the next frame from the file
				(grabbed, frame) = self.stream.read()
				# if the `grabbed` boolean is `False`, then we have
				# reached the end of the video file
				if not grabbed:
					self.stop()
					return
				# add the frame to the queue
				self.Q.put(frame)

	def read(self):
		# return next frame in the queue
		return self.Q.get()



	def more(self):
		# return True if there are still frames in the queue
		return self.Q.qsize() > 0



	def stop(self):
		# indicate that the thread should be stopped
		self.stopped = True



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

def start_node():
    #------------initialize-----------------#
    global corners
    global id 
    #camera
    fvs = FileVideoStream(4).start()
    time.sleep(1.0)
    # start the FPS timer
    fps = FPS().start()
    rospy.init_node('camear_node')
    rospy.loginfo('camera_node started')
    #img=cv2.imread(filename)   reading image 
    bridge=CvBridge()
    #imgMsg=bridge.cv2_to_imgmsg(img,'bgr8')   convert image to ros message 
    pub = rospy.Publisher('/car_info',Int32MultiArray,queue_size=10)

    #--------------loop---------------------#
    while not rospy.is_shutdown():
        complete_vector = []
        direction_iterator=0
        frame = fvs.read()
        frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])
        car_array_publish = Int32MultiArray()
        corners,ids = tools.findArucoMarkers(frame)
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

        cv2.imshow("image",frame)
        cv2.waitKey(1)
        fps.update() 
#---------------------------------------------------------------------#  
def camera_return():
    return [corners[0],id]







if __name__ == '__main__':
    print("main>>>>>>>>>>")
    try:
        start_node()
    except rospy.ROSInterruptException:
        pass



