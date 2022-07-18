# Import modules
import copy
import pygame as pg
import random
import time
from pygame.math import Vector2
import algo
import math 
import numpy as np


import car

# Screen size
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 800
safeDist=300
tupleScreenSize = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Traffic Jam
trafficJamNum: int = 100
# Cars in intersection per second
spawnRate = 1.2
# Max Initial Velocity
maxInitialVelocity = 3
# Num of Lanes
numOfLanes = 1
car_speed_list = np.zeros([100])
defult_car_speed=[]
Error_list=np.zeros([100,100])
speed=np.zeros([100,100])
dist_from_c_list= np.zeros([100])
dist_v2v=np.zeros([100,100])
k=0.002

###########################################   Screen Formatter     ###########################################


def quitGame():
    """
    Quit Function
    """
    pg.quit()
    quit()


def inputEventCheck():
    """
    Define exit button and ESC to close game
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quitGame()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quitGame()


#######################################################################################################

###########################################   MAIN ALGO     ###########################################

collisionCenter = (650,400)


def mainFCN():
    
    carId = 0
    # Get Center of Screen in 2D Vector
    centerOfIntersection: Vector2 = pg.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    # Start the stopwatch / counter
    startTime = time.perf_counter()  # returns the float value of time in seconds will give you a more accurate value
    # than time.clock ()
    # Creates a new copy of the Surface with the pixel format changed This is always the fastest format for blitting
    BG.convert()
    # list of cars in scene
    currentCarInScene = []
    # Loop for possible cars in intersection
    i = 2  
    while len(currentCarInScene) < trafficJamNum:
        global Error_list
        pg.draw.circle(screen, (0, 255, 0),[720, 400], 15, 3)
        
        deltaTime = clock.get_time()  # It will compute how many milliseconds have passed since the previous call.
        # Check if end event happen or not
        inputEventCheck()
        # Cars in intersection per second
        endTime = time.perf_counter()  # returns the float value of time in seconds
        # Spawn in a New Car if it is time
        if (endTime - startTime) > (1 / spawnRate) :
            # give car random initial velocity
            # 0.1 to reduce it in sim so all possible number form 0 to maxInitialVelocity-1
            #            initialVelocity = random.randrange(maxInitialVelocity) * 0.1 + 0.2
            # generate random lane for
            lineNumber = random.randrange(numOfLanes)
            # Generate New Car form car file in Car class
            newCar = car.Car(screen, lineNumber,carId, initialVelocity = 0.1)
            carId = carId + 1
            currentCarInScene.append(newCar)
            '''
            currentVechiles= algo.startAlgo(currentCarInScene, collisionCenter,screen)
            x = len(currentVechiles)
            print("----------------------------------------------")
            print(x)
            cIndex1=0
            cIndex2=1
            spd = 0.2  
            if x  in [0,1] :
                pass
             
         
            elif x > 1:
                for cIndex1 in range(x-2):
                    for cIndex2 in range(x-1):
                        car1InCM = currentVechiles[cIndex1].getVehiclePositionFromGrade()
                        car2InCM = currentVechiles[cIndex2].getVehiclePositionFromGrade()
                        dst_x = abs(car1InCM[0]-car2InCM[0])
                        dst_y = abs(car1InCM[1]-car2InCM[1])
                        dst = math.sqrt(dst_x**2+dst_y**2)
                        print("distance = "+ str(dst))
                        Error_of_car_gaps = safeDist - dst
                        spd =  spd + 0.01*Error_of_car_gaps
                        pg.draw.line(screen, (0,255,0),currentVechiles[cIndex1].getVehiclePositionFromGrade(), currentVechiles[cIndex2].getVehiclePositionFromGrade(), 4)
                        pg.display.update()
                        if spd > 0.4 :
                            spd = 0.4
                        elif spd < 0.1 :
                            spd = 0.1
                        if Error_of_car_gaps > 0:
                            #if spd > currentVechiles[cIndex1].velocity[0]:
                            currentVechiles[cIndex1].setVelocity(spd)
                      
                           '''     
            

            startTime = time.perf_counter()  # returns the float value of time in seconds
        
        # start scene
        screen.blit(BG, (0, 0))
        # Loop in Cars
        copies = copy.copy(currentCarInScene)
        
    
        for carIndex in range(len(currentCarInScene)):
            if currentCarInScene[carIndex].IsvehicleOutOfScene():
                # Remove a Car if it is off the screen
                copies.remove(currentCarInScene[carIndex])
                print("")
            else:
                currentCarInScene[carIndex].updateVehicleStates(deltaTime, currentCarInScene[carIndex].getVelocity())
                currentCarInScene[carIndex].drawVehcile(screen)
        currentCarInScene = copies
        clock.tick(120)
        pg.display.flip()
        
        currentVechiles= algo.startAlgo(currentCarInScene, collisionCenter,screen)
        
        

        #-------------------------------------------------------------------
        car_numbers = len(currentVechiles)
        cIndex1=0
        cIndex2=1
        spd = 0.2  
        if car_numbers  in [0]:
            pass
        elif car_numbers in [1] :
            currentVechiles[0].setVelocity(0.4)
        elif car_numbers  > 1:
            for cIndex1 in range(car_numbers-1):
                if currentVechiles[cIndex1].getDir() == car.Directions.up_dir:
                    dist_from_c_y = -1*abs(currentVechiles[cIndex1].getVehiclePositionFromGrade().y - collisionCenter[1]) 
                    dist_from_c_list[cIndex1]=(dist_from_c_y)
                else :
                    dist_from_c_x = -1*abs(currentVechiles[cIndex1].getVehiclePositionFromGrade().x - collisionCenter[0])
                    dist_from_c_list[cIndex1]=(dist_from_c_x)
                for cIndex2 in range(car_numbers):
                    if currentVechiles[cIndex2].getDir() == car.Directions.up_dir:
                        dist_from_c_y = -1*abs(currentVechiles[cIndex2].getVehiclePositionFromGrade().y - collisionCenter[1])
                        dist_from_c_list[cIndex2]=(dist_from_c_y)
                    else :
                        dist_from_c_x = -1*abs(currentVechiles[cIndex2].getVehiclePositionFromGrade().x - collisionCenter[0])
                        dist_from_c_list[cIndex2]=(dist_from_c_x)
                    car1InCM = currentVechiles[cIndex1].getVehiclePositionFromGrade()
                    car2InCM = currentVechiles[cIndex2].getVehiclePositionFromGrade()
                    dst_x = abs(car1InCM[0]-car2InCM[0])
                    dst_y = abs(car1InCM[1]-car2InCM[1])
                    dst = math.sqrt(dst_x**2+dst_y**2)
                    dist_v2v[cIndex1][cIndex2] = dst
                    Error_list = dist_v2v - safeDist
                    pg.draw.line(screen, (0,255,0),currentVechiles[cIndex1].getVehiclePositionFromGrade(), currentVechiles[cIndex2].getVehiclePositionFromGrade(), 4)
                   # pg.draw.circle(screen,(0,255,0),collisionCenter,5)
                    pg.draw.circle(screen,(0,255,0),(720,400),5)
                    pg.draw.line(screen, (0,255,0),(10,10),(10,310))
                    pg.display.update()
            
            speed_change = k*(Error_list)
            


            max_priority_index = np.argmax(dist_from_c_list)
            compare_list = set(dist_from_c_list)
            compare_list.remove(max(compare_list))
            max_priority_index = np.argmax(compare_list)

            for cIndex_1 in range(car_numbers-1):
                for cIndex_2 in range(car_numbers):
                    if Error_list[cIndex_1][cIndex_2] > 0:
                        if dist_from_c_list[cIndex_1] < dist_from_c_list[cIndex_2]:
                            sp = currentVechiles[cIndex_1].getVelocity() + abs(Error_list[cIndex_1][cIndex_2])
                            if sp > 0.4:
                               sp = 0.4


                            currentVechiles[cIndex_1].setVelocity(sp) 
                            
                        else:
                            sp = currentVechiles[cIndex_2].getVelocity() + abs(Error_list[cIndex_1][cIndex_2])
                            if sp > 0.4:
                               sp = 0.4

                            currentVechiles[cIndex_2].setVelocity(sp)                            
                            
                    
                    elif Error_list[cIndex_1][cIndex_2] < 0:
                        if dist_from_c_list[cIndex_1] < dist_from_c_list[cIndex_2]:
                            sp1 = 0.4
                            sp2 = currentVechiles[cIndex_1].getVelocity() - abs(Error_list[cIndex_1][cIndex_2])
                            
                            if sp1 > 0.4:
                                sp1=0.4
                            if sp2 < 0:
                                sp2=0

                            if currentVechiles[cIndex_2].getVelocity()  == 0 :
                                currentVechiles[cIndex_2].setVelocity(0.1)
                            else :
                                currentVechiles[cIndex_2].setVelocity(sp1)
                            currentVechiles[cIndex_1].setVelocity(sp2)

                        elif dist_from_c_list[cIndex_1] == dist_from_c_list[cIndex_2] :
    
                            currentVechiles[cIndex_2].setVelocity(0.4)
                            currentVechiles[cIndex_1].setVelocity(0)

                        else:
                            
                            sp1 = 0.4
                            sp2 = currentVechiles[cIndex_1].getVelocity() - abs(Error_list[cIndex_1][cIndex_2])
                            
                            if sp1 > 0.4:
                                sp1=0.4
                            if sp2 < 0:
                                sp2 = 0
                            
                            currentVechiles[cIndex_2].setVelocity(sp2)

                            if currentVechiles[cIndex_1].getVelocity() == 0 :
                                currentVechiles[cIndex_1].setVelocity(0.1)
                            else:
                                currentVechiles[cIndex_1].setVelocity(sp1)
                    currentVechiles[max_priority_index].setVelocity(0.4)

            

                
                




                    
                   





                
                    

#######################################################################################################
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


#######################################################################################################
if __name__ == '__main__':
    
    # Init PG framework
    pg.init()
    # Screen size
    screen = pg.display.set_mode(tupleScreenSize)
    # Window Caption
    pg.display.set_caption("Autonomous Uncontrolled Intersection Management")
    # Load Img
    BG = pg.image.load('./cars/ExpandedIntersection.png')
    # pg.time.Clock(): returns a float value which represents the current processor time in seconds.
    clock = pg.time.Clock()
    mainFCN()
