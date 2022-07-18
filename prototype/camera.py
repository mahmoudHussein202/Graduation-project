from ast import arg
import numpy as np
import argparse
import cv2

#argument and save in dictionary
ap=argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="Enter path of image")
args=vars(ap.parse_args())

#loading and converting image into numpy array
image = cv2.imread(args["image"])
cv2.imshow("BGR color space",image)
cv2.waitKey(0)