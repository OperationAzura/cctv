from pynput import keyboard
#import os
import cv2
import queue
from picamera.array import PiRGBArray
from picamera import PiCamera
import multiprocessing
import sys

class ImageStream(multiprocessing.Process):
    def __init__(self, title, width, height, imgQ, frameRate=32, scale=100):
        multiprocessing.Process.__init__(self)
        self.imgQ = imgQ
        self.frame = None
        self.title = title
        self.piCamera = PiCamera()
        self.piCamera.resolution = (width, height)
        self.piCamera.framerate = frameRate
        self.width = width
        self.height = height
        self.frameRate = frameRate
        self.rawCapture = PiRGBArray(self.piCamera, size=(width, height))


    #StartCapture Starts aquiring image objects from the camera feed
    def run(self):
        for self.frame in self.piCamera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            try:
                self.imgQ.put(self.frame.array,False)
            except:
                #set limited q size
                #clear q if full
                print('double pooping still')
                pass
            self.rawCapture.truncate(0)

    #SetTitle sets the title
    def SetTitle(self, title):
        self.title = title

    #GetTitle gets the title
    def GetTitle(self, ):
        return self.title

    #SetWidth sets the width
    def SetWidth(self, width):
        self.width = width

    #__del__ destuctor to release resources
    def __del__(self):
        self.piCamera.close()

    def printToFile(self, s):
        f = None
        try:
            f = open('log.log', 'a')
        except:
            try:
                f = open('log.log', 'x')
            except:
                Print('logging is messed up')
        if f != None:
            f.write(s)
            f.write('\n')
            f.close()

if __name__ == "__main__":
    import screeninfo

    screen = screeninfo.get_monitors()[0]
    sWidth, sHeight = screen.width, screen.height
    width = 640
    height = 480
    title = 'frame'
    imgQ = multiprocessing.Queue
    print('running from class file')
    x = ImageStream(title=title, width=width, height=height, imgQ=imgQ)
    print('ImageStream Object created')
    x.start()
    print('after StartCapture')
    x.join()
