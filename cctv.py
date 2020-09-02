# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import imageStreamClass

def main():
	imgStream = imageStreamClass.ImageStream()
	imgStream.StartCapture()
