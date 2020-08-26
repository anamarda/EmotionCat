import time 

class Cat:
    def __init__(self, _decision_maker, _emotion_detector):
        self.decision_maker = _decision_maker
        self.emotion_detector = _emotion_detector
        
        self.emotion_detector.start()
        
    def start(self):
        while True:
            detected_emotion = self.emotion_detector.get_emotion()
            print("[INFO] Detected emotion: " + detected_emotion)
            self.decision_maker.mirror_emotion(detected_emotion)
            self.decision_maker.mirror_emotion("Neutral")
            time.sleep(0.5)
            print(self.emotion_detector.stopped)
            if self.emotion_detector.stopped:
                print("===========DA")
                return
