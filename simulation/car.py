import pygame as pg
import random
from pygame.surface import Surface, SurfaceType


class Directions:
    """
    Stores the Matrices for each cardinal direction
    Determines if two given directions are perpendicular or opposite
    """

    """""
        from bottom to up (up)          (0,-1)
        from up to bottom (bottom)      (0,1)
        from right to left (left)       (-1,0)
        from left to right (right)      (1,0)
        
    """""
    up_dir = (0, -1)
    bottom_dir = (0, 1)
    left_dir = (-1, 0)
    right_dir = (1, 0)
    directions = [up_dir, right_dir]


class Assets():
    """
    load the images into Pygame
    """
    blue = pg.image.load('./cars/BlueCar.png')
    sblue = pg.image.load('./cars/BlueSudan.png')
    yellow = pg.image.load('./cars/YellowTruck.png')
    brown = pg.image.load('./cars/BrownCar.png')
    grey = pg.image.load('./cars/GreyCar.png')
    red = pg.image.load('./cars/RedCar.png')
    purple = pg.image.load('./cars/PurpleCar.png')
    green = pg.image.load('./cars/GreenCar.png')
    cars = [blue, sblue, yellow, brown, grey, red, purple, green]


# Class initialization
class Car:
    initVelocityIfNotGiven = 0.25
    initAccelerationIfNotGiven = 0.0001

    def __init__(self, screen, lane, ID, initialVelocity=initVelocityIfNotGiven,
                 initAcceleration=initAccelerationIfNotGiven):
        """
        Stores all the information about a certain vehicle in the scene
        """
        # Vehicle Properties
        self.ID = ID
        self.lane = lane
        # Give car Random Direction
        self.direction = random.choice(Directions.directions)

        # Vehicle graphics
        # Get Random Vehicle Img
        vehicleImg = random.choice(Assets.cars)
        # Transparent Background
        self.vehicleImg = vehicleImg.convert_alpha()
        # Choose position Randomly
        self.position = self.generatePositionFromLane(lane=lane, direction=self.direction)
        # Rotate Img for corrct way
        self.vehicleImg = self.rotateVehicleImg(self.vehicleImg)
        # Dynamics

        # Modify Velocity and Acceleration
        self.velocity = pg.math.Vector2(self.direction[0] * initialVelocity, self.direction[1] * initialVelocity)
        self.acceleration = pg.math.Vector2(self.direction[0] * initAcceleration, self.direction[1] * initAcceleration)
        # Scale Cars
        self.vehicleLength = self.vehicleImg.get_height()
        self.vehicleWidth = self.vehicleImg.get_width()
        self.vehicleImg = pg.transform.scale(self.vehicleImg, (int(self.vehicleWidth / 2), int(self.vehicleLength / 2)))

    def getID(self):
        return int(self.ID)

    def generatePositionFromLane(self, lane, direction):
        """
        Generate X and Y of Vehicle
        """

        """
            Points of intersection :
                from down to up x = 790+(41/2)                  // LANE1 FORM START (790) + (CAR WIDTH/2)
                                y = 900                         // OUT OF SCREEN BOUNDARIES 
                                        
                from up to down x = 670+(41/2)                  // LANE2 FORM START (790) + (CAR WIDTH/2)
                                y = -100                        // OUT OF SCREEN BOUNDARIES  
                                
                from right to left x = -100                     // OUT OF SCREEN BOUNDARIES  
                                 , y = 363+(41/2)              // LANE2 FORM START (363) + (CAR WIDTH/2)
                                 
                from left to right x = 1540                    // OUT OF SCREEN BOUNDARIES 
                                 , y = 470-(41/2))            // LANE1 FORM START (470) + (CAR WIDTH/2)
        """
        img = self.vehicleImg.get_rect()
        if direction == Directions.up_dir:
            if lane == 0:
                return pg.math.Vector2(747, 1000)
        elif direction == Directions.right_dir:
            if lane == 0:
                return pg.math.Vector2(-100, 435)
        else:
            None

    def getDir(self):
        return self.direction

    def rotateVehicleImg(self, oldImgToRotate):
        """
        all anchor points in  top left
        so lef direction by default have right coordinate
        ------                                        ---------
        |X   |    ---->  Rotate 90 degrees   ---->    |      X|
        |    |                                        |       |
        ------                                        ---------
        Algo :
        Find the width and height of the image.
        Subtract half the width from 'x'
        Subtract half the height from 'y'
        Blit the image to new 'x' and new 'y'
        """
        if self.direction == Directions.up_dir:
            rotatedImg = pg.transform.rotate(oldImgToRotate, 270)
        elif self.direction == Directions.bottom_dir:
            rotatedImg = pg.transform.rotate(oldImgToRotate, 90)
        elif self.direction == Directions.right_dir:
            rotatedImg = pg.transform.rotate(oldImgToRotate, 180)
        elif self.direction == Directions.left_dir:
            return oldImgToRotate
        imgAttribute = rotatedImg.get_rect()  # return current x y w h
        self.position.x -= imgAttribute.width / 2
        self.position.y -= imgAttribute.height / 2
        return rotatedImg

    def IsvehicleOutOfScene(self):
        """
        SCREEN_WIDTH X= 1440
        SCREEN_HEIGHT Y= 800
        """
        if self.direction == Directions.up_dir:
            return self.position.y < 50

        elif self.direction == Directions.right_dir:
            return self.position.x > 1400

    def IsVehicleInScene(self):
        if self.direction == Directions.up_dir:
            return self.position.y >= -100
        elif self.direction == Directions.bottom_dir:
            return self.position.y <= 900
        elif self.direction == Directions.right_dir:
            return self.position.x <= 1540
        elif self.direction == Directions.left_dir:
            return self.position.x >= -100

    def drawVehcile(self, screen):
        screen.blit(self.vehicleImg, (self.position.x, self.position.y))
        # if self.direction == Directions.up_dir:
        # st(self.vehicleImg.get_width())

    def updateVehicleStates(self, dt, speed):
        # Makesure sign of velocity in each direction
        # print(self.direction)
        if self.direction == Directions.right_dir:
            self.velocity = pg.math.Vector2(speed, 0)
        elif self.direction == Directions.left_dir:
            self.velocity = pg.math.Vector2(-1 * speed, 0)
        elif self.direction == Directions.up_dir:
            self.velocity = pg.math.Vector2(0, 1 * speed)
        elif self.direction == Directions.bottom_dir:
            self.velocity = pg.math.Vector2(0, -1 * speed)
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def getVehiclePositionFromGrade(self):
        return self.position

    def getCarLength(self):
        return self.vehicleLength()

    def setVelocity(self, speed):
        if self.direction == Directions.right_dir:
            self.velocity = pg.math.Vector2(speed, 0)
        elif self.direction == Directions.left_dir:
            self.velocity = pg.math.Vector2(-1 * speed, 0)
        elif self.direction == Directions.up_dir:
            self.velocity = pg.math.Vector2(0, -1 * speed)
        elif self.direction == Directions.bottom_dir:
            self.velocity = pg.math.Vector2(0, speed)
    
    
    

    def setAcceleration(self, acc):
        self.acceleration = acc

    def getVelocity(self):
        if self.direction == Directions.right_dir or self.direction == Directions.left_dir:
            return self.velocity[0]

        elif self.direction == Directions.up_dir or self.direction == Directions.bottom_dir:
            return self.velocity[1]

    def getAcceleration(self):
        return self.acceleration

  
            
