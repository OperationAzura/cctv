from pynput import keyboard
#import os
import cv2
import queue
from picamera.array import PiRGBArray
from picamera import PiCamera
import threading
import sys

class ImageStream(threading.Thread):
    def __init__(self, title='frame', width=1280, height=720, frameRate=32, scale=100):
        threading.Thread.__init__(self)
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
        self.centerX = int(width / 2)
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
        #self.StartKeyListener()


    #StartCapture Starts aquiring image objects from the camera feed
    def run(self):
        for self.frame in self.piCamera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            self.origionalImage = self.frame.array
            #self.HandleInput()
            try:
                self.ApplyMag()
            except:
                print('fram error?')
            self.image = cv2.rotate(self.image, cv2.ROTATE_180 )
            self.image = cv2.putText(self.image, 'width: ' + str(self.widthX) + ' height: ' + str(self.height),(self.centerX - 500,self.centerY - 500), cv2.FONT_HERSHEY_SIMPLEX, 2,(2,255,2),3)
            self.image = cv2.putText(self.image, 'radiusX: ' + str(self.radiusX) + ' radiusY: ' + str(self.radiusY),(self.centerX - 500,self.centerY - 450), cv2.FONT_HERSHEY_SIMPLEX, 2,(2,255,2),3)
            self.image = cv2.putText(self.image, 'minX: ' + str(self.minX) + ' minY: ' + str(self.minY),(self.centerX - 500,self.centerY - 400), cv2.FONT_HERSHEY_SIMPLEX, 2,(2,255,2),3)
            self.image = cv2.putText(self.image, 'maxX: ' + str(self.maxX) + ' maxY: ' + str(self.maxY),(self.centerX - 500,self.centerY - 400), cv2.FONT_HERSHEY_SIMPLEX, 2,(2,255,2),3)
            self.DisplayImageWindow()
            self.rawCapture.truncate(0)

    def SetMagnification(self, scaleChange):
        self.scale += scaleChange
        print('scale: ', self.scale)
        self.radiusX = int(self.scale * self.width / 100)
        self.radiusY = int(self.scale * self.height/ 100)
        self.minX = self.centerX - self.radiusX
        self.maxX = self.centerX + self.radiusX
        self.minY = self.centerY - self.radiusY
        self.maxY = self.centerY + self.radiusY
        
    def ApplyMag(self):
        self.croppedImage = self.origionalImage[self.minX : self.maxX, self.minY : self.maxY]
        self.image = cv2.resize(self.croppedImage, (self.width, self.height)) 
    
    #DisplayImageWindow displays the image 
    def DisplayImageWindow(self):
        cv2.namedWindow(self.title, cv2.WINDOW_NORMAL)
        #cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(self.title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        cv2.imshow(self.title, self.image)
        k = cv2.waitKey(50)
        if k == 27:         # wait for ESC key to exit
            print('esc key hit')
            cv2.destroyAllWindows()
            self.piCamera.close()
            sys.exit(0)
        elif k == 82 :
            self.SetMagnification( 5)
            print('up arrorw: ', k)
        elif k == 84:
            self.SetMagnification( -5)
            print('dow arrow: ', k)

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
    import screeninfo

    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height

    print('running from class file')
    x = ImageStream(width=width, height=height)
    print('ImageStream Object created')
    x.start()
    print('after StartCapture')
    x.join()
