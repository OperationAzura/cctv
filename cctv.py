# import the necessary packages
import time
import cv2
print('-1')
from imageStreamClass import ImageStream
import sys
sys.stdout = open('x.x', 'w')

def main():
	print('0')
	imgStream = ImageStream()
	print('1')
	imgStream.StartCapture()
	print('2')
	time.sleep(99999999999)
	print('3')
