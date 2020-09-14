import time
import os
import cv2
from imageStreamClass import ImageStream
import queue
import multiprocessing
import sys

class Display(multiprocessing.Process):
    def __init__(self, title, width, height, imgRecv):
        print('building displayClass')
        multiprocessing.Process.__init__(self)
        self.imgRecv = imgRecv
        self.image = None
        self.title = title
        self.width = width
        self.height = height
        

    #run overides the threading run function and
    #displays the 
    def run(self):
        print('runing didsplay')
        while True:
            self.image = self.imgRecv.recv()
            self.DisplayImageWindow()
            
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
