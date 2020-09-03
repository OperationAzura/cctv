# import the necessary packages
import time
import cv2
print('-1')
from imageStreamClass import ImageStream

def main():
	print('0')
	imgStream = imageStreamClass.ImageStream()
	print('1')
	imgStream.StartCapture()
	print('2')
	time.sleep(99999999999)
	print('3')
