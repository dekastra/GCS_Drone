import cv2 as cv
from threading import Thread


class GetVideo:
    def __init__(self, data, source=0):
        self.is_running = False
        self.__data = data
        self.__stream = None
        self.__source = source

    def start_fetch(self):
        self.is_running = True
        self.__stream = cv.VideoCapture(self.__source)
        if not self.__stream.isOpened():
            self.__stream.open(self.__source)
        self.__stream.set(cv.CAP_PROP_BUFFERSIZE, 1)
        Thread(target=self.get_frame, args=()).start()

    def get_frame(self):
        while self.is_running == True:
            ret, img = self.__stream.read()
            if ret:
                self.__data.set_image(img)

    def stop_fetch(self):
        self.is_running = False
        self.__stream.release()


class ShowVideo:
    def __init__(self, data, title="Video"):
        self.is_running = False
        self.__data = data
        self.__title = title

    def start(self):
        self.is_running = True
        Thread(target=self.show, args=()).start()

    def show(self):
        while self.is_running:
            if self.__data.get_image() is not None:
                cv.imshow(self.__title, self.__data.get_image())
            if cv.waitKey(1) == ord('q'):
                self.is_running = False
                break

    def stop(self):
        self.is_running = False
        cv.destroyAllWindows()


class VideoData:
    def __init__(self):
        self.__image = None

    def set_image(self, image):
        self.__image = image

    def get_image(self):
        return self.__image