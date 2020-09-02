from pynput import keyboard
import threading 
import queue

class ImageStream(object):
    def __init__(self, title='frame', width=1280, height=720, frameRate=32, scale=10):
        self.q = queue.Queue()
        self.frame = None
        self.origionalImage = None
        self.croppedImage = None
        self.image = None
        self.title = title
        self.piCam = PiCamera()
        self.piCamera.resolution = (width, height)
        self.piCamera.framerate = frameRate
        self.scale = scale
        self.width = width
        self.height = height
        #set
        self.centerX = int(height / 2)
        self.centerY = int(height / 2)
        self.radiusX = int(scale*width/100)
        self.radiusY = int(scale*height/100)
        self.minX = self.centerX - self.radiusX
        self.maxX = self.centerX + self.radiusX
        self.minY = self.centerY - self.radiusY
        self.maxY = self.centerY + self.radiusY
        self.frameRate = frameRate
        self.rawCapture = PiRGBArray(self.piCamera, size=(width, height))
        self.StartKeyListener()


    #StartCapture Starts aquiring image objects from the camera feed
    def StartCapture(self):
        for self.frame in self.piCamera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            self.image = frame.array
            self.HandleInput()
            self.ApplyMag()
            self.DisplayImageWindow()
            # show the frame
            #image = cv2.cv.rotate(image, cv2.ROTATE_180 )
            self.rawCapture.truncate(0)

    def SetMagnification(self, scaleChange):
        self.scale += scaleChange
        self.radiusX = int(self.scale * self.width / 100)
        self.radiusY = int(self.scale * self.height/ 1 00)
        self.minX = self.centerX - self.radiusX
        self.maxX = self.centerX + self.radiusX
        self.minY = self.centerY - self.radiusY
        self.maxY = self.centerY + self.radiusY
        
    def ApplyMag(self):
        self.croppedImage = self.image[self.minX : self.maxX, self.minY : self.maxY]
        self.image = cv2.resize(self.croppedImage, (self.width, self.height)) 

    
    #DisplayImageWindow displays the image 
    def DisplayImageWindow(self):
        cv2.imshow(self.title, self.image)

    def StartKeyListener(self):
        def on_press(key):
            try:
                k = key.char  # single-char keys
            except:
                k = key.name  # other keys
            if k in ['up', 'down']:  # keys of interest
                self.q.put_nowait(k)

        listener = keyboard.Listener(on_press=on_press)
        listener.start()
       
    def HandleInput(self):
        k = q.get_nowait()
        if k == 'up':
            self.SetMagnification(1)
        elif k == 'down':
            self.SetMagnification(-1)

    #SetTitle sets the title
    def SetTitle(self, title):
        self.title = title

    #GetTitle gets the title
    def GetTitle(self, ):
        return self.title

    #SetWidth sets the width
    def SetWidth(self, width):
        self.width = width

