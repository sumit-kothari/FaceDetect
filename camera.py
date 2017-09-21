import cv2
import threading
from email_test import send_email
import _thread
from time import gmtime, strftime
import os
import numpy


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


size = 4
haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'
# Part 1: Create fisherRecognizer
print('Training...')
# Create a list of images and a list of corresponding names
(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            lable = id
            images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1
(width, height) = (130, 100)

# Create a Numpy array from the two lists above
(images, lables) = [numpy.array(lis) for lis in [images, lables]]

# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
model = cv2.face.createFisherFaceRecognizer()

print(images.shape)
print(lables.shape)

model.train(images, lables)


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

        print("Found {0} faces at {1} !".format(
            len(faces), strftime("%Y-%m-%d %H:%M:%S", gmtime())))

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
            # for (x, y, w, h) in facesBox:
            #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            for (x, y, w, h) in facesBox:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                # Try to recognize the face
                prediction = model.predict(face_resize)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)

                if prediction[1] < 500:

                    cv2.putText(image, '%s - %.0f' % (names[prediction[0]], prediction[
                                1]), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

                    mail_body = "Found {0} !".format(
                        names[prediction[0]], strftime("%Y-%m-%d %H:%M:%S", gmtime()))

                    _thread.start_new_thread(send_email, (mail_body, ))
                else:
                    cv2.putText(image, 'not recognized', (x - 10, y - 10),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
