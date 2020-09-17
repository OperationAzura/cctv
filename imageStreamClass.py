import time
import os
import cv2
import queue
from picamera.array import PiRGBArray
from picamera import PiCamera
import multiprocessing
import sys

class ImageStream(multiprocessing.Process):
    def __init__(self, title, width, height, origImgSend, frameRate=10):
        multiprocessing.Process.__init__(self)
        print('building imageStreamClass')
        self.origImgSend = origImgSend
        self.frame = None
        self.title = title
        self.piCamera = None 
        self.width = width
        self.height = height
        self.frameRate = frameRate
        self.rawCapture = PiRGBArray(self.piCamera, size=(width, height))


    #StartCapture Starts aquiring image objects from the camera feed
    def run(self):
        self.piCamera = PiCamera()
        self.piCamera.resolution = (self.width, self.height)
        self.piCamera.framerate = self.frameRate
        time.sleep(0.1)
        for self.frame in self.piCamera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            try:
                self.origImgSend.send(self.frame.array)
                #self.origImgSend2.send(self.frame.array[len(int(self.Frame.array)/2):])
            except Exception as e:
                print('exception: ', str(e))
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

def PrintToFile( s, name):
    f = None
    try:
        f = open(name + '.log', 'a')
    except:
        try:
            f = open(name + '.log', 'x')
        except:
            print('logging is messed up')
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
    imgQ = multiprocessing.Queue()
    print('running from class file')
    x = ImageStream(title=title, width=width, height=height, imgQ=imgQ)
    print('ImageStream Object created')
    x.start()
    print('after Start')
    r = imgQ.get()
    count = 0
    while True:
        r = imgQ.get()
        print('r: ',count)
        count = count +1
    x.join()
    print('after join')
