import cv2
import threading

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


facesBox = None
gray = None


class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stopped = False

    def run(self):
        global facesBox

        while (~(gray is None)):
            if self.stopped:
                return

            facesBox = self.predict(gray)

    def predict(self, gray):
        if self.stopped:
            return

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        print("Found {0} faces!".format(len(faces)))

        return faces

    def stop(self):
        self.stopped = True


class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.this_thread = MyThread()
        self.this_thread.start()

    def __del__(self):
        self.this_thread.stop()
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()

        global gray

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if facesBox is not None:
            # Draw a rectangle around the faces
            for (x, y, w, h) in facesBox:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
