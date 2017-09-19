import cv2
import sys
import threading


# Get user supplied values
# imagePath = sys.argv[1]
cascPath = "haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)


facesBox = None
image = None


class MyThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.stopped = False

    def run(self):
        global facesBox

        while (~(image is None)):
            if self.stopped:
                return

            facesBox = self.predict(image)

    def predict(self, image):
        if self.stopped:
            return

        gray = image
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )

        print("Found {0} faces!".format(len(faces)))

        return faces

    def stop(self):
        self.stopped = True


video_capture = cv2.VideoCapture(0)


this_thread = MyThread()
this_thread.start()


while True:
    ret, image = video_capture.read()

    if facesBox is not None:
        # Draw a rectangle around the faces
        for (x, y, w, h) in facesBox:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Faces found", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        this_thread.stop()
        break
