import time
import cv2
from imageStreamClass import PrintToFile
import queue
import multiprocessing
import sys

class WorkProcess(multiprocessing.Process):
    def __init__(self, title, width, height, screenWidth, screenHeight, origImgRecv, imgSend,  scale=100):
        multiprocessing.Process.__init__(self)
        self.origImgRecv = origImgRecv
        self.imgSend = imgSend
        self.origionalImage = []
        self.croppedImage = None
        self.image = None
        self.title = title
        self.scale = scale
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.centerX = int(width / 2)
        self.centerY = int(height / 2)
        self.radiusX = int(scale*self.centerX/100)
        self.radiusY = int(scale*self.centerY/100)
        self.minX = self.centerX - self.radiusX
        self.maxX = self.centerX + self.radiusX
        self.minY = self.centerY - self.radiusY
        self.maxY = self.centerY + self.radiusY

    def run(self):
        while True:
            #start = time.clock()
            try:
                self.origionalImage = self.origImgRecv.recv()
            except Exception as e:
                PrintToFile(str(e), 'wErr')

            try:
                s = time.clock()
                self.ApplyMag()
                PrintToFile(str((time.clock() - s) * 1000)+' : ApplyMag', 'amBench')
            except Exception as e:
                PrintToFile(str(e), 'wErr')
            else:
                try:
                    s = time.clock()
                    self.imgSend.send(self.image)
                    PrintToFile(str((time.clock() - s) * 1000 ) + ' : imageSend', 'imgSendBench')
                except Exception as e:
                    PrintToFile(str(e), 'wErr')
            #PrintToFile(str((time.clock() - start) * 1000), 'wBench')

    def SetMagnification(self, scaleChange):
        self.scale += scaleChange
        self.radiusX = int(self.scale * self.centerX / 100)
        self.radiusY = int(self.scale * self.centerY / 100)
        self.minX = self.centerX - self.radiusX
        self.maxX = self.centerX + self.radiusX
        self.minY = self.centerY - self.radiusY
        self.maxY = self.centerY + self.radiusY
        
    def ApplyMag(self):
        s = time.clock()
        self.croppedImage = self.origionalImage[self.minY : self.maxY, self.minX : self.maxX]
        PrintToFile(str((time.clock() - s) * 1000),'cropB')
        s = time.clock()
        self.image = cv2.resize(self.croppedImage, (self.screenWidth, self.screenHeight))  
        PrintToFile(str((time.clock() - s) * 1000), 'reB')

if __name__ == "__main__":
    import screeninfo
    from imageStreamClass import ImageStream
    from displayClass import Display

    screen = screeninfo.get_monitors()[0]
    sWidth, sHeight = screen.width, screen.height
    print('w: '+str(sWidth)+' : h: ' +str(sHeight) )
    width = 720
    height = 480
    frameRate = 20
    scale = 100
    

    title = 'frame'
    #SETUP PIES to communicate between processes
    origImgRecv, origImgSend = multiprocessing.Pipe(False)
    origImgRecv2, origImgSend2 = multiprocessing.Pipe(False)
    imgRecv, imgSend = multiprocessing.Pipe(False)

    imgStream = ImageStream(title=title, width=width, height=height, origImgSend=origImgSend, origImgSend2=origImgSend2, frameRate=frameRate)
    work = WorkProcess(title=title, width=width, height=height, screenWidth=sWidth, screenHeight=sHeight, origImgRecv=origImgRecv, imgSend=imgSend, scale=scale)
    display = Display(title=title, width=sWidth, height=sHeight, imgRecv=imgRecv)

    work.start()
    time.sleep(0.1)
    print('work started')
    imgStream.start()
    time.sleep(0.1)
    print('imgStream started')
    display.start()
    print('display started')

    imgStream.join()
    print('imgStream.join')
    work.join()
    print('work.join')
    display.join()
    print('display.join')
