import time
import os
import cv2
import queue
from picamera.array import PiRGBArray
from picamera import PiCamera
import multiprocessing
import sys




###
###make sure sends are all set!
###



class ImageStream(multiprocessing.Process):
    def __init__(self, title, width, height, origImgSend, frameRate=10):
        multiprocessing.Process.__init__(self)
        self.origImgSend = origImgSend
        self.frame = None
        self.title = title
        self.piCamera = None # PiCamera()
        #self.piCamera.resolution = (width, height)
        #self.piCamera.framerate = frameRate
        self.width = width
        self.height = height
        self.frameRate = frameRate
        self.rawCapture = PiRGBArray(self.piCamera, size=(width, height))


    #StartCapture Starts aquiring image objects from the camera feed
    def run(self):
        self.piCamera = PiCamera()
        self.piCamera.resolution = (self.width, self.height)
        self.piCamera.framerate = self.frameRate
        print('runnning in run even?')
        #print('wtf! ', self.piCamera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True))
        #self.__del__()
        print('trying sleep')
        time.sleep(0.1)
        #print(type((self.piCamera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True))))
        for self.frame in self.piCamera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            #self.PrintToFile('wtf')
            try:
                #print('at least this right?')
                self.imgQ.put(self.frame.array)
                #print('put worktin')
            except Exception as e:
                print('exception: ', str(e))
                #set limited q size
                #clear q if full
                #print('double pooping still')
                #self.piCamera.close()
                #os.exit(0)
            #print('end of try: ')
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

    def PrintToFile(self, s):
        f = None
        try:
            f = open('log.log', 'a')
        except:
            try:
                f = open('log.log', 'x')
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
