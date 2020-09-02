#Zoom is the function to magnify the image
def Zoom():

import cv2
video = cv2.VideoCapture(0)
while True:
    check, frame = video.read()
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
  video.release()
  cv2.destroyAllWindows

python python-3.x opencv
share improve this question
edited Jun 15 '18 at 6:52
asked Jun 15 '18 at 6:45
hayasiiiint
5511 silver badge66 bronze badges

    2
    Show your effort otherwise question is going to be closed. – Shree Jun 15 '18 at 6:48
    done. I've edited it now. @Shree – hayasiiiint Jun 15 '18 at 6:54

add a comment
2 Answers
Active
Oldest
Votes
6

You can use this solution. It makes the job -> croping + zoom + array up and array down.

import cv2

        def show_webcam(mirror=False):
            scale=10

            cam = cv2.VideoCapture(0)
            while True:
                ret_val, image = cam.read()
                if mirror: 
                    image = cv2.flip(image, 1)


                #get the webcam size
                height, width, channels = image.shape

                #prepare the crop
                 centerX,centerY=int(height/2),int(width/2)
                radiusX,radiusY= int(scale*height/100),int(scale*width/100)

                minX,maxX=centerX-radiusX,centerX+radiusX
                minY,maxY=centerY-radiusY,centerY+radiusY

                cropped = image[minX:maxX, minY:maxY]
                resized_cropped = cv2.resize(cropped, (width, height)) 

                cv2.imshow('my webcam', resized_cropped)
                if cv2.waitKey(1) == 27: 
                    break  # esc to quit

                #add + or - 5 % to zoom

                if cv2.waitKey(1) == 0: 
                    scale += 5  # +5

                if cv2.waitKey(1) == 1: 
                    scale = 5  # +5

            cv2.destroyAllWindows()


        def main():
            show_webcam(mirror=True)


        if __name__ == '__main__':
            main()

