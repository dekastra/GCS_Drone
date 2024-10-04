import cv2 as cv
from threading import Thread


class GetVideo:
    def __init__(self, data, source=0):
        self.isRunning = False
        self.__data = data
        self.__stream = None
        self.__source = source

    def start_fetch(self):
        self.isRunning = True
        self.__stream = cv.VideoCapture(self.__source)
        if not self.__stream.isOpened():
            self.__stream.open(self.__source)
        self.__stream.set(cv.CAP_PROP_BUFFERSIZE, 1)
        Thread(target=self.get_frame, args=()).start()

    def get_frame(self):
        while self.isRunning == True:
            ret, img = self.__stream.read()
            if ret:
                self.__data.setImage(True,img)

    def stop_fetch(self):
        self.isRunning = False
        self.__stream.release()


class ShowVideo:
    def __init__(self, data, title="Video"):
        self.isRunning = False
        self.__data = data
        self.__title = title

    def start(self):
        self.isRunning = True
        Thread(target=self.show, args=()).start()

    def show(self):
        while self.isRunning:
            if self.__data.getProcImage() is not None:
                cv.imshow(self.__title, self.__data.getProcImage())
            if cv.waitKey(1) == ord('q'):
                self.isRunning = False
                break

    def stop(self):
        self.isRunning = False
        cv.destroyAllWindows()


class VideoData:
    def __init__(self):
        self.__image = None
        self.__procimg = None
        self.__imgexist = False
        self.__procexist = False

    def setImage(self,exist,image):
        self.__image = image
        self.__imgexist = exist

    def getImage(self):
        return self.__imgexist, self.__image

    def setProcImage(self,exist, image):
        self.__procimg = image
        self.__procexist = exist

    def getProcImage(self):
        return self.__procexist, self.__procimg

