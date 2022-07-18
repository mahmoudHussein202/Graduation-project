#!/usr/bin/env python3
import copy
from xxlimited import new
import pygame as pg
import random
import time
from pygame.math import Vector2
import algo
import math 
import numpy as np
import car 
import tools
from std_msgs.msg import Int32MultiArray
import rospy
from std_msgs.msg import Float32

car_speed_list = np.zeros([100])
defult_car_speed=[]
Error_list=np.zeros([100,100])
speed=np.zeros([100,100])
dist_from_c_list= np.full(100,-50000)
dist_v2v=np.zeros([100,100])
collisionCenter = (1280/2,720/2)
safeDist=400
counter_car = 0

def callback (car_info_message):
    global counter_car
    car_1 = rospy.Publisher('/15_ID',Float32,queue_size=10)
    car_2 = rospy.Publisher('/16_ID',Float32,queue_size=10)
    car_3 = rospy.Publisher('/17_ID',Float32,queue_size=10)
    message = Float32()
    car_array_inscene = tools.get_array_from_message(car_info_message)
    current_car_inscene_objects_array = tools.getDataToClass(car_array_inscene)
    car_numbers = len(current_car_inscene_objects_array)
    cIndex1=0
    cIndex2=1
    spd = 0.2
    #print(car_numbers)  
    if car_numbers  in [0] :
        #print("im here")
        message.data = 0.00
        car_1.publish(message)
        car_2.publish(message)
        car_3.publish(message)

    elif car_numbers in [1] :
        current_car_inscene_objects_array[0].setVelocity(0.4)
        
    elif car_numbers  > 1:
        for cIndex1 in range(car_numbers-1):
            #print("im here")
            if current_car_inscene_objects_array[cIndex1].getDir() == car.Directions.up_dir:
                dist_from_c_y = -1*abs(current_car_inscene_objects_array[cIndex1].getVehiclePositionFromGrade().y - collisionCenter[1]) 
                dist_from_c_list[cIndex1]=dist_from_c_y
                #print("im here")
            else :
                dist_from_c_x = -1*abs(current_car_inscene_objects_array[cIndex1].getVehiclePositionFromGrade().x - collisionCenter[0])
                dist_from_c_list[cIndex1]=dist_from_c_x
                #print("im here")
            for cIndex2 in range(car_numbers):
                if current_car_inscene_objects_array[cIndex2].getDir() == car.Directions.up_dir:
                    dist_from_c_y = -1*abs(current_car_inscene_objects_array[cIndex2].getVehiclePositionFromGrade().y - collisionCenter[1])
                    dist_from_c_list[cIndex2]=dist_from_c_y
                else :
                    dist_from_c_x = -1*abs(current_car_inscene_objects_array[cIndex2].getVehiclePositionFromGrade().x - collisionCenter[0])
                    dist_from_c_list[cIndex2]=dist_from_c_x
                #print(dist_from_c_list)
                car1InCM = current_car_inscene_objects_array[cIndex1].getVehiclePositionFromGrade()
                car2InCM = current_car_inscene_objects_array[cIndex2].getVehiclePositionFromGrade()
                dst_x = abs(car1InCM[0]-car2InCM[0])
                dst_y = abs(car1InCM[1]-car2InCM[1])
                dst = math.sqrt(dst_x**2+dst_y**2)
                dist_v2v[cIndex1][cIndex2] = dst
        Error_list = dist_v2v - safeDist
        #print(Error_list)
            #speed_change = k*(Error_list)
        
        max_priority_index = np.argmax(dist_from_c_list)
        compare_list = set(dist_from_c_list)
        compare_list.remove(max(compare_list))
        max_priority_index = np.argmax(compare_list)
        for cIndex_1 in range(car_numbers-1):
                for cIndex_2 in range(car_numbers):
                    if Error_list[cIndex_1][cIndex_2] > 0:
                        if dist_from_c_list[cIndex_1] < dist_from_c_list[cIndex_2]:
                            sp = current_car_inscene_objects_array[cIndex_1].getVelocity() + abs(Error_list[cIndex_1][cIndex_2])
                            if sp > 0.4:
                               sp = 0.4
                            current_car_inscene_objects_array[cIndex_1].setVelocity(sp) 
                        else:
                            sp = current_car_inscene_objects_array[cIndex_2].getVelocity() + abs(Error_list[cIndex_1][cIndex_2])
                            if sp > 0.4:
                               sp = 0.4
                            current_car_inscene_objects_array[cIndex_2].setVelocity(sp)                            
                    elif Error_list[cIndex_1][cIndex_2] < 0:
                        if dist_from_c_list[cIndex_1] < dist_from_c_list[cIndex_2]:
                            sp1 = 0.4
                            sp2 = current_car_inscene_objects_array[cIndex_1].getVelocity() - abs(Error_list[cIndex_1][cIndex_2])
                            if sp1 > 0.4:
                                sp1=0.4
                            if sp2 < 0:
                                sp2=0
                            current_car_inscene_objects_array[cIndex_2].setVelocity(sp1)
                            current_car_inscene_objects_array[cIndex_1].setVelocity(sp2)

                        elif dist_from_c_list[cIndex_1] == dist_from_c_list[cIndex_2] :
    
                            current_car_inscene_objects_array[cIndex_2].setVelocity(0.4)
                            current_car_inscene_objects_array[cIndex_1].setVelocity(0)

                        else:
                            
                            sp1 = 0.5
                            sp2 = current_car_inscene_objects_array[cIndex_1].getVelocity() - abs(Error_list[cIndex_1][cIndex_2])
                            
                            if sp1 > 0.5:
                                sp1=0.5
                            if sp2 < 0:
                                sp2 = 0
                            
                            current_car_inscene_objects_array[cIndex_2].setVelocity(sp2)
                            current_car_inscene_objects_array[cIndex_1].setVelocity(sp1)
                    current_car_inscene_objects_array[max_priority_index].setVelocity(0.4)
                    singularity_flag = 1  
    
    check_list = []
    #print(current_car_inscene_objects_array)
    for i in range (len(current_car_inscene_objects_array)):
        car_id = current_car_inscene_objects_array[i].getID()
        car_direction= current_car_inscene_objects_array[i].getDir()
        car_velocity = current_car_inscene_objects_array[i].getVelocity()
        a_list = [car_id,car_direction,car_velocity]
        check_list.append(a_list)
        
        new_publish_velocity = 50*(0.4+ car_velocity)
        if new_publish_velocity > 40 : 
            new_publish_velocity = 40 
        elif new_publish_velocity < 0 :
            new_publish_velocity =0
        print(new_publish_velocity)
        message.data = new_publish_velocity
        #message.data = car_velocity
        
        if counter_car == 4 :
            if car_id == 15 :
                car_1.publish(message)
            elif car_id == 16 :
                car_2.publish(message)
            elif car_id == 17 :
                car_3.publish(message)
            counter_car = 0 
        else :
            counter_car = counter_car +1

    
    print(check_list)












    #print(current_car_inscene_objects_array)


rospy.init_node("algorithm_node")
sub = rospy.Subscriber('/car_info',Int32MultiArray,callback)
rospy.spin()