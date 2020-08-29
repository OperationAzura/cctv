# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#from PySide import QtGui
#app = QtGui.QApplication([])
#screen_resolution = app.desktop().screenGeometry()
#width = screen_resolution.width() / 2
#height = screen_resolution.height() / 2
#print('w: ', width)
#print('h: ', height)
# initialize the camera and grab a reference to the raw camera capture
width = 1824
height = 984
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width, height))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	# show the frame
	image = cv2.cv.rotate(image, cv2.ROTATE_180 )
	cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
	cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	cv2.imshow("frame", image)
	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
