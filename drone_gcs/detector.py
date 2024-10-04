import cv2 as cv
import numpy as np
from ultralytics import YOLO as yl
from threading import Thread

class Detector:
    '''
    Use this class to process the image detection algorithm for determining
    drone position.
    '''
    
    def __init__(self, data):
        '''
        Initiation method for this class. Make sure the path to training model
        is correct. To simplify, put the training model file in the same folder
        as this class. 
        '''
        self.__isRunning = False
        self.__image = None
        self.__xpos = -1
        self.__ypos = -1
        self.__data = data
        model_path = "best.pt" #change this into other path if necessary
        self.__model = yl(model_path)

    def setFrame(self, frame):
        self.__image = frame

    def setImage(self, image):
        '''
        Function to set image file to be processed in object detection algorithm.
        Provide the image (as opencv capture object), and the size of the image in
        width and height. 
        '''
        self.__image = image

    def getPosResult(self):
        '''
        Use this function to get the processed image and the x-y position of the drone.
        '''
        return self.__xpos, self.__ypos

    def __detect(self):
        while self.__isRunning:
            success, self.__image = self.__data.getImage()
            if success:
                results = list(self.__model(self.__image))
                self.__data.setProcImage(True,self.__image)
                if len(results) > 0:
                    result = results[0]
                    boxes = result.boxes.xyxy.cpu().numpy()
                    if len(boxes) > 0:
                        x1, y1, x2, y2 = boxes[0][:4]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                        center_x, center_y = int((x1 + x2) / 2), int((y1 + y2) / 2)

                        self.__xpos = (-1) * center_x * 0.8026 + 249.45
                        self.__ypos = (-1) * center_y * 0.5916 + 138.72

                        cv.rectangle(self.__image, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        cv.circle(self.__image, (center_x, center_y), 5, (0, 0, 255), -1)
                        self.__data.setProcImage(True,self.__image)
                        

    def start_detect(self):
        '''
        Call this function to start the drone detection process.
        This function will run __detect() in new thread.
        '''
        self.__isRunning = True
        Thread(target=self.__detect, args=()).start()

    def stop_detect(self):
        '''
        Do not forget to call this function to end the object detection process.
        This function is important because the detection thread can only be ended by
        calling this function.
        '''
        self.__isRunning = False
        
