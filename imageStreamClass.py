from pynput import keyboard
#import os
import cv2
import queue
from picamera.array import PiRGBArray
from picamera import PiCamera
import threading
import sys

#sys.stdout =  open('l.l','w')
#sys.stderr = open('err.log', 'w')
#print('redirected')

class ImageStream(threading.Thread):
    def __init__(self, title='frame', width=1280, height=720, frameRate=32, scale=50):
        threading.Thread.__init__(self)
        print('redirect3')
        self.printToFile('constructor')
        self.q = queue.Queue()
        self.frame = None
        self.origionalImage = None
        self.croppedImage = None
        self.image = None
        self.title = title
        self.piCamera = PiCamera()
        self.piCamera.resolution = (width, height)
        self.piCamera.framerate = frameRate
        self.scale = scale
        self.width = width
        self.height = height
        #set
        print('width: ', width)
        print('height: ', height)
        self.centerX = int(height / 2)
        self.centerY = int(height / 2)
        self.radiusX = int(scale*width/100)
        print('radiusX: ', self.radiusX)
        self.radiusY = int(scale*height/100)
        print('radiusY: ', self.radiusY)
        self.minX = self.centerX - self.radiusX
        print("minX: ", self.minX)
        self.maxX = self.centerX + self.radiusX
        print('maxX: ', self.maxX)
        self.minY = self.centerY - self.radiusY
        print('miny: ', self.minY)
        self.maxY = self.centerY + self.radiusY
        print('maxY: ',self.maxY)
        self.frameRate = frameRate
        self.rawCapture = PiRGBArray(self.piCamera, size=(width, height))
        self.StartKeyListener()
        self.printToFile('end constructor')


    #StartCapture Starts aquiring image objects from the camera feed
    def run(self):
        self.printToFile('startcapture')
        for self.frame in self.piCamera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            self.origionalImage = self.frame.array
            #self.HandleInput()
            #self.ApplyMag()
            self.image = self.origionalImage
            #self.DisplayImageWindow()
            # show the frame
            self.image = cv2.rotate(self.image, cv2.ROTATE_180 )
            self.DisplayImageWindow()
            self.rawCapture.truncate(0)
        self.printToFile('done captureing')

    def SetMagnification(self, scaleChange):
        self.printToFile('setMagnification')
        self.scale += scaleChange
        self.radiusX = int(self.scale * self.width / 100)
        self.radiusY = int(self.scale * self.height/ 100)
        self.minX = self.centerX - self.radiusX
        self.maxX = self.centerX + self.radiusX
        self.minY = self.centerY - self.radiusY
        self.maxY = self.centerY + self.radiusY
        self.printToFile('done setting magnification')
        
    def ApplyMag(self):
        self.printToFile('appyMag')
        self.croppedImage = self.origionalImage[self.minX : self.maxX, self.minY : self.maxY]
        self.image = cv2.resize(self.croppedImage, (self.width, self.height)) 
        self.printToFile('done apply mag')
    
    #DisplayImageWindow displays the image 
    def DisplayImageWindow(self):
        
        cv2.namedWindow(self.title, cv2.WND_PROP_FULLSCREEN)
        #cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(self.title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        self.printToFile('start displayImage')
        cv2.imshow(self.title, self.image)
        k = cv2.waitKey(1)
        if k == 27:         # wait for ESC key to exit
            print('esc key hit')
            cv2.destroyAllWindows()
            self.piCamera.close()
            sys.exit(0)
        self.printToFile('end displayImage')

    def StartKeyListener(self):
        self.printToFile('startKeyListener')
        def on_press(key):
            try:
                k = key.char  # single-char keys
            except:
                k = key.name  # other keys
            if k in ['up', 'down']:  # keys of interest
                self.q.put_nowait(k)

        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        self.printToFile('end keylistener')
       
    def HandleInput(self):
        self.printToFile('handleInput')
        k = ''
        try:
            k = self.q.get_nowait()
        except:
            pass
        if k is 'up':
            self.SetMagnification(1)
        elif k is 'down':
            self.SetMagnification(-1)
        self.printToFile('done handleinput')

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
    print('running from class file')
    x = ImageStream()
    print('ImageStream Object created')
    x.start()
    print('after StartCapture')
    x.join()
