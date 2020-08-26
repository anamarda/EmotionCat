from resources.global_variables import ANGLE_MAX, ANGLE_MIN, LOGGER_PATH
import logging

class AngleValidator:
    def __init__(self):
        logging.basicConfig(filename=LOGGER_PATH, level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + '__init__')
        
    def check_angle(self, angle):
        logging.debug(self.__class__.__name__ + ' - ' + 'check_angle')        
        if angle > ANGLE_MAX:
            raise Exception("[ERR] " + str(angle) + " > " + str(ANGLE_MAX))
        if angle < ANGLE_MIN:
            raise Exception("[ERR] " + str(angle) + " < " + str(ANGLE_MIN))
