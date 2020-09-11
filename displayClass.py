import time
import cv2
from imageStreamClass import ImageStream
import queue
import multiprocessing
import sys

class Display(multiprocessing.Process):
    def __init__(self, title, width, height, imgQ,  scale=100):
        multiprocessing.Process.__init__(self)
        self.imgQ = imgQ
        self.origionalImage = None
        self.croppedImage = None
        self.image = None
        self.title = title
        self.scale = scale
        self.width = width
        self.height = height
        self.centerX = int(width / 2)
        self.centerY = int(height / 2)
        self.radiusX = int(scale*self.centerX/100)
        self.radiusY = int(scale*self.centerY/100)
        self.minX = self.centerX - self.radiusX
        self.maxX = self.centerX + self.radiusX
        self.minY = self.centerY - self.radiusY
        self.maxY = self.centerY + self.radiusY

    #run overides the threading run function and
    #displays the 
    def run(self):
        while True:
            #get image from queue
            try:
                self.origionalImage = self.imgQ.get(False)
                #print('xxxxxxxxLen: ',len(self.origionalImage))
                #print('origIMGTYPE: ', type(self.origionalImage))
            except: # no new image
                print('xxxorigionalImage = .getfals')
                #os.exit(1)
            try:
                self.ApplyMag()
            except Exception as e:
                print('err: ', str(e))
                self.image = self.origionalImage
                print('BUTTfram error?')
            print('len: ', len(self.origionalImage))
            print('len: ', len(self.image))
            #self.image = self.origionalImage
            self.image = cv2.rotate(self.image, cv2.ROTATE_180 )
            self.DisplayImageWindow()

    def SetMagnification(self, scaleChange):
        self.scale += scaleChange
        print('scale: ', self.scale)
        self.radiusX = int(self.scale * self.centerX / 100)
        self.radiusY = int(self.scale * self.centerY / 100)
        self.minX = self.centerX - self.radiusX
        self.maxX = self.centerX + self.radiusX
        self.minY = self.centerY - self.radiusY
        self.maxY = self.centerY + self.radiusY
        
    def ApplyMag(self):
        self.croppedImage = self.origionalImage[self.minY : self.maxY, self.minX : self.maxX]
        self.image = cv2.resize(self.croppedImage, (self.width, self.height)) 
    
    #DisplayImageWindow displays the image 
    def DisplayImageWindow(self):
        cv2.namedWindow(self.title, cv2.WINDOW_NORMAL)
        #cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
        cv2.setWindowProperty(self.title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        try:
            cv2.imshow(self.title, self.image)
        except Exception as e:
            print('ex!!!!!! ',str(e))
            print('still pooping')
            os.exit()
        k = cv2.waitKey(50)
        if k == 27:         # wait for ESC key to exit
            print('esc key hit')
            cv2.destroyAllWindows()
            #self.piCamera.close()
            sys.exit(0)
        elif k == 82 :
            self.SetMagnification( 5)
            print('up arrorw: ', k)
        elif k == 84:
            self.SetMagnification( -5)
            print('dow arrow: ', k)

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
        pass
if __name__ == "__main__":
    import screeninfo
    from imageStreamClass import ImageStream

    screen = screeninfo.get_monitors()[0]
    sWidth, sHeight = screen.width, screen.height
    width = 640
    height = 480
    title = 'frame'
    imgQ = multiprocessing.Queue()
    print('running from display class file')
    x = ImageStream(title=title, width=width, height=height, imgQ=imgQ)
    y = Display(title, sWidth, sHeight, imgQ)
    print('ImageStream Object created')
    x.start()
    time.sleep(1)
    print('pause before starting display')
    y.start()
    print('after StartCapture')
    x.join()
    y.join()
