# Import modules
from re import X
import pygame as pg
import time
from pygame.math import Vector2
from scipy.spatial import distance
import car
import time
import xlsxwriter
import math 
safeDist = 300


def startAlgo(currentCarInScene, collisionCenter,screen):
    
    start = time.time()
    workbook = xlsxwriter.Workbook('arrays.xlsx')
    worksheet = workbook.add_worksheet()
    vehiclePriorities = []
    
    carsOutofCalc = []
    currentVechiles = currentCarInScene.copy()
    if len(currentCarInScene) <= 1:
        pass
    else:
        removeCar(vehiclePriorities, carsOutofCalc)
        #------------------------------------------------------------------------
        #------------------------------------------------------------------------



        for carIndex in range(len(currentCarInScene)):
            
            '''
                Check if car pass intersection point give it max speed 
                and if it before 7intersection point give it priority 
            '''
          


            if currentCarInScene[carIndex].getDir() == car.Directions.up_dir:
                #if car passes the intersection give it the max velocity
                if currentCarInScene[carIndex].getVehiclePositionFromGrade().y < collisionCenter[1]:
                    currentCarInScene[carIndex].setVelocity(0.6)
                    currentVechiles.remove(currentCarInScene[carIndex])

                    #carsOutofCalc contain IDs of the cars that passes the center
                    carsOutofCalc.append(currentCarInScene[carIndex].getID())
                    # print(currentCarInScene[carIndex].getVelocity())
                
                
            elif currentCarInScene[carIndex].getDir() == car.Directions.right_dir:
                if currentCarInScene[carIndex].getVehiclePositionFromGrade().x > collisionCenter[0]:
                    currentCarInScene[carIndex].setVelocity(0.6)
                    carsOutofCalc.append(currentCarInScene[carIndex].getID())
                    currentVechiles.remove(currentCarInScene[carIndex])
                    # print(currentCarInScene[carIndex].getVelocity())
                    
               






                        #pg.draw.line(screen, (0,255,0),currentVechiles[cIndex1].getVehiclePositionFromGrade(), currentVechiles[cIndex2].getVehiclePositionFromGrade(), 4)
                        #pg.display.update()




           

                    #vehiclePriorities.append((currentCarInScene[carIndex].getID(), distanceFromCenter))

                    
                    # print(vehiclePriorities[carIndex])
        # print(vehiclePriorities)

        '''
        Calc gap between all car
        '''
    '''
        for carIndex1 in range(len(vehiclePriorities)):
            for carIndex2 in range(carIndex1 + 1, len(vehiclePriorities)):
                car1InCM = currentCarInScene[carIndex1].getVehiclePositionFromGrade()
                car2InCM = currentCarInScene[carIndex2].getVehiclePositionFromGrade()
                dst_x = abs(car1InCM[0]-car2InCM[0])
                dst_y = abs(car1InCM[1]-car2InCM[1])
                dst = math.sqrt(dst_x**2+dst_y**2)

                Error_of_car_gaps[carIndex1][carIndex2] = safeDist - dst
                print(Error_of_car_gaps[carIndex1][carIndex2])
                spd = (7 / 220) * abs(Error_of_car_gaps[carIndex1][carIndex2]) 
                if spd > 0.6:
                    spd = 0.6
                elif spd <= 0:
                    spd = 0

                if Error_of_car_gaps[carIndex1][carIndex2] > 0:
                    if vehiclePriorities[carIndex1] > vehiclePriorities[carIndex2]:
                        currentCarInScene[carIndex1].setVelocity(spd)
                        currentCarInScene[carIndex2].setVelocity(currentCarInScene[carIndex2].velocity[0]-(spd/16))
                    else:
                        currentCarInScene[carIndex2].setVelocity(spd)
                        currentCarInScene[carIndex1].setVelocity(currentCarInScene[carIndex1].velocity[0]-(spd/16))
                    

                elif Error_of_car_gaps[carIndex1][carIndex2] < 0:
                    if vehiclePriorities[carIndex1] > vehiclePriorities[carIndex2]:
                        currentCarInScene[carIndex2].setVelocity(spd)
                        currentCarInScene[carIndex1].setVelocity(currentCarInScene[carIndex1].velocity[0]-(spd/16))
                    
                    else:

                        currentCarInScene[carIndex1].setVelocity(spd)
                        currentCarInScene[carIndex2].setVelocity(currentCarInScene[carIndex2].velocity[0]-(spd/16))
                    

        
       
     
        end = time.time()
        print("The time of execution of above program is :", end-start)
     '''
        

    return currentVechiles
    


def removeCar(carPriorities, carOutOfCalc):
    for carIndex in range(len(carOutOfCalc)):
        for carIndex2 in range(len(carPriorities)):
            if carOutOfCalc[carIndex] == carPriorities[carIndex2][0]:
                # remove it from carPriorities
                carPriorities.remove(carPriorities[carIndex2][0])





                


def numOfPixelToCM(numOfPixels):
    dpi = 96
    # 1 inch = 96 px
    # 1 inch = 2.54 cm
    # pixels = (96 * centi) / 2.54;
    # (pixels * 2.54)/dpi = centi
    cm = [-1, -1]
    cm[0] = (numOfPixels[0] * 2.54) / dpi
    cm[1] = (numOfPixels[1] * 2.54) / dpi
    return cm
