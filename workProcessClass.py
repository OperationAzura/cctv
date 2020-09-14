import cv2
from imageStreamClass import PrintToFile
import queue
import multiprocessing
import sys

class WorkProcess(multiprocessing.Process):
    def __init__(self, title, width, height, screenWidth, screenHeight, origImgRecv, imgSend,  scale=100):
        multiprocessing.Process.__init__(self)
        print('building workProcess class')
        self.origImgRecv = origImgRecv
        self.imgSend = imgSend
        self.origionalImage = None
        self.croppedImage = None
        self.image = None
        self.title = title
        self.scale = scale
        self.screeWidth = screenWidth
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
        print('running workProcess')
        while True:
            try:
                self.origImgRecv.recv_bytes_into(self.origionalImage)
            except Exception as e:
                PrintToFile(str(e))

            try:
                self.ApplyMag()
            except Exception as e:
                PrintToFile('Error with ApplyMag in workProcess')
                PrintToFile(str(e))
            else:
                try:
                    imgSend.send_bytes(self.Image)
                except Exception as e:
                    PrintToFile('Error in imgSend.send_bytes')
                    PrintToFile(str(e))



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
        self.image = cv2.resize(self.croppedImage, (self.screenWidthn, self.screenHeight))  

if __name__ == "__main__":
    import screeninfo
    from imageStreamClass import ImageStream
    from displayClass import Display

    screen = screeninfo.get_monitors()[0]
    sWidth, sHeight = screen.width, screen.height
    width = 640
    height = 480
    frameRate = 10
    scale = 100
    

    title = 'frame'
    #SETUP PIES to communicate between processes
    origImgRecv, origImgSend = multiprocessing.Pipe(False)
    imgRecv, imgSend = multiprocessing.Pipe(False)

    imgStream = ImageStream(title=title, width=width, height=height, origImgSend=origImgSend, frameRate=frameRate)
    work = WorkProcess(title=title, width=width, height=height, screenWidth=sWidth, screenHeight=sHeight, origImgRecv=origImgRecv, imgSend=imgSend, scale=scale)
    display = Display(title=title, width=sWidth, height=sHeight, imgRecv=imgRecv)

