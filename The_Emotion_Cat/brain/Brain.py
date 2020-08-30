import cv2
import os
import imutils
import time
import pickle
import face_recognition
import numpy as np
from threading import Thread
from imutils.video import VideoStream
from brain.utils.model import create_model
from resources.global_variables import *

class Brain:
    def __init__(self):
        self.crt_emotion = STARTING_EMOTION
        self.model_weighs_path = MODEL_WEIGHS_PATH
        self.owner = None
        self.stopped = False
        self.restart = False
        self.destroy = False
        
    def set_owner(self, name):
        self.owner = name     
        
    def start(self):   
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self
        
    def update(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        model = create_model()
        model.load_weights(self.model_weighs_path)

        # prevents openCL usage and unnecessary logging messages
        cv2.ocl.setUseOpenCL(False)

        emotion_dict = {
            0: ANGRY_STR, 
            1: DISGUSTED_STR, 
            2: FEARFUL_STR, 
            3: HAPPY_STR, 
            4: NEUTRAL_STR, 
            5: SAD_STR, 
            6: SURPRISED_STR
                }

        print("[INFO] starting video stream...")
        vs = VideoStream(src=0, usePiCamera=True).start()
        time.sleep(CAMERA_SLEEP)

        data = pickle.loads(open(FACE_ENCODINGS_PATH, "rb").read())
        detector = cv2.CascadeClassifier(HAAR_PATH)

        while True:
            if self.stopped is True:
                if self.destroy is False:
                    cv2.destroyAllWindows()
                    vs.stop()
                    self.destroy = True
            else:
                if self.restart is True:
                    del vs
                    vs = VideoStream(src=0, usePiCamera=True).start()
                    time.sleep(CAMERA_SLEEP)
                    self.restart = False
                    
                # Find haar cascade to draw bounding box around face
                frame = vs.read()
                frame = imutils.resize(frame, width=FRAME_WIDTH)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # detect faces in the grayscale frame
                face_rectangles = detector.detectMultiScale(
                    gray, 
                    scaleFactor=SCALE_FACTOR, 
                    minNeighbors=MIN_NEIGHBORS,
                    flags=cv2.CASCADE_SCALE_IMAGE)

                # OpenCV returns bounding box coordinates in (x, y, w, h) order
                # but we need them in (top, right, bottom, left) order, so we
                # need to do a bit of reordering
                boxes = [(y, x + w, y + h, x) for (x, y, w, h) in face_rectangles]

                # compute the facial embeddings for each face bounding box
                encodings = face_recognition.face_encodings(rgb, boxes)
                names = []

                for encoding in encodings:
                    matches = face_recognition.compare_faces(data["encodings"],encoding)
                    name = UNKNOWN_FACE
                    if True in matches:
                        # find the indexes of all matched faces then initialize a
                        # dictionary to count the total number of times each face
                        # was matched
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        # loop over the matched indexes and maintain a count for
                        # each recognized face face
                        for i in matchedIdxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1

                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)
                    
                    # update the list of names
                    names.append(name)
                    
                emotions = []
                try:
                    for ((x, y, w, h), name) in zip(boxes, names): 
                        if name != self.owner:
                            emotions.append("")
                            continue
                        try:
                            roi_gray = gray[y:y + h, x:x + w]
                            #cropped_img = cv2.resize(roi_gray, (48, 48))
                            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                            prediction = model.predict(cropped_img)
                            maxindex = int(np.argmax(prediction))
                            emotions.append(emotion_dict[maxindex])
                        except Exception as e:
                            print(e)
                            emotions.append("")
                            continue
                    
                    for ((top, right, bottom, left), name, emotion) in zip(boxes, names, emotions):
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        y = top - 15 if top - 15 > 15 else top + 15
                        
                        if name != self.owner:
                            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                                0.75, (0, 255, 0), 2)
                        else:
                            cv2.putText(frame, name + " is " + emotion, (left, y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                            self.crt_emotion = emotion

                    cv2.imshow("Frame", frame)
                except Exception as e:
                    print(e)
                    
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stopped = True
                    break
        
        cv2.destroyAllWindows()
        vs.stop()

    def get_emotion(self):
        return "Sad" if self.crt_emotion == "" else self.crt_emotion
        
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        
    def restart(self):
        self.stopped = False
        self.restart = True
        self.destroy = False
