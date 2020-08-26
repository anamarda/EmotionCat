from utils.actions import angry
from utils.actions import disgusted
from utils.actions import fearful
from utils.actions import happy
from utils.actions import neutral
from utils.actions import sad
from utils.actions import surprised
from resources.global_variables import LOGGER_PATH
import logging
import time

class DecisionMaker:
    def __init__(self, _mover):
        logging.basicConfig(filename=LOGGER_PATH,level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + '__init__')
        
        self.mover = _mover
        
        self.emotion_dict = {
            "Angry" : angry,
            "Disgusted" : disgusted,
            "Fearful" : fearful,
            "Happy" : happy,
            "Neutral" : neutral,
            "Sad" : sad,
            "Surprised" : surprised,
                }

    def mirror_emotion(self, emotion):
        logging.debug(self.__class__.__name__ + ' - ' + 'mirror_emotion')
        move_list = self.emotion_dict[emotion]()
        self.mover.move(move_list)
    
