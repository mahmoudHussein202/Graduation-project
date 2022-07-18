import cv2.aruco as aruco
import cv2
import numpy as np
import car
import pygame as pg
from pygame.math import Vector2


def findArucoMarkers(img,markerSize=6,totalMarkers=250,draw=True):
    global list_ids
    #1-convert image to grey
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key= getattr(aruco , f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    #  (Value):aruco , (string): DICT  و يدمجهم كدا 
    #                  value.string
    arucoDict = aruco.Dictionary_get(key) #get the dictionary of aruco needed
    arucoParam = aruco.DetectorParameters_create() #aruco parameters create 
    #detect need grey (image) , (dictionary) , (parameters)
    #(bboxs): boundary boxes , (ids):id for each aruco , (rejected): found an aruco but can't resolve
    bboxs, ids, rejected = aruco.detectMarkers(imgGray,arucoDict, parameters=arucoParam) 
    list_ids=str(ids)
    list_ids = list_ids.replace('[','')
    list_ids=list_ids.replace(']','')
    #print(ids) 
    if draw:
        aruco.drawDetectedMarkers(img, bboxs)  
    return [bboxs, ids]


def print_corners(corners,ids):
    # verify at least one ArUco marker was detected
    x=[] 
    all_points = []

    if len(corners) > 0:
        ids = ids.flatten()
        for (markerCorner, markerID) in zip(corners, ids):
            xcorners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = xcorners
            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            x.append([int(topLeft[0]),int(topLeft[1]),int(markerID)])
            all_points.append(topLeft)
            all_points.append(topRight)
            all_points.append(bottomRight)
            all_points.append(bottomLeft)
            all_points.append(int(markerID))
        return x , all_points
    else:
        return -1 ,-1



def get_array_from_message(message):
    car_number = len(message.data)/4
    car_array_inscene = np.zeros([int(car_number),4])
    counter = 0
    for i in range(int(car_number)):
        for j in range(4):
            car_array_inscene[i][j]=int(message.data[counter])
            counter = counter +1
    return car_array_inscene





def getDataToClass(car_array_inscene):
    # List of Tuples  
    currentCarInScene_object = []
    for carIndex in range(len(car_array_inscene/4)):
        vec_pos_x = car_array_inscene[carIndex][0]
        vec_pos_y = car_array_inscene[carIndex][1]
        vec_id = car_array_inscene[carIndex][2]
        direction = car_array_inscene[carIndex][3]
        position = pg.math.Vector2(vec_pos_x,vec_pos_y)
        newCar = car.Car(vec_id,direction,position)
        currentCarInScene_object.append(newCar)
    return currentCarInScene_object
        #print ("id = " + str(vec_id) )
        #print ("x = " + str(vec_pos_x) )
        #print ("y = " + str(vec_pos_y) )


def get_direction_vector (all_points_tuple):
    direction_list = []
    if all_points_tuple == -1 :
        car_number=0
    else :
        car_number = int(len(all_points_tuple)/5)
        car_list_size_modified = np.reshape(np.array(all_points_tuple) , (car_number,5))
        #print(car_list_size_modified)
        for row_index in range (car_number):
            x1 = car_list_size_modified[row_index][0][0]
            x2 = car_list_size_modified[row_index][1][0]
            x3 = car_list_size_modified[row_index][2][0]
            x4 = car_list_size_modified[row_index][3][0]

            y1 = car_list_size_modified[row_index][0][1]
            y2 = car_list_size_modified[row_index][1][1]
            y3 = car_list_size_modified[row_index][2][1]
            y4 = car_list_size_modified[row_index][3][1]

            ID = car_list_size_modified[row_index][4]
            up_case1 =  y1 < y3 and y1 <y4 and y2 <y3 and y2<y4
            up_case2 = y1>y2 and y1 <= y3 and y1 < y4 and y2 <y3 and y2<y4 and y3 < y4
            up_case3 = y1<y2 and y1 < y3 and y1 <y4 and y2 <y3 and y2<=y4 and y3 > y4
            if up_case1 or up_case2 or up_case3:
                direction = 1 # upward
                direction_list.append(direction)
            
            else :
                direction = 0 # right
                direction_list.append(direction)
            direction_list.append(ID)

        direction_vector = np.array(direction_list)
        direction_vector = direction_vector.reshape(car_number,2)
        return direction_vector
        

    #print(car_number)
    