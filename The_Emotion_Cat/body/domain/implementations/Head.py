import time
import logging
import threading
from resources.global_variables import *
from utils.conversions import *
from body.domain.interfaces.ILimb import ILimb
# 836 = 0 degrees
# 1250 = 45 degrees
# 1664 = 90 degrees

class Head:
    def __init__(self, _channel1, _init_angle1, _channel2, _init_angle2, _message, _bus, _validator):
        logging.basicConfig(filename=LOGGER_PATH,level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + '__init__' + ' : ' + _message)
         
        self.channel1 = _channel1
        self.channel2 = _channel2
        self.crt_angle1 = _init_angle1
        self.crt_angle2 = _init_angle2
        self.message = _message        
        self.bus = _bus
        self.validator = _validator  
      
        self.__go_to_neutral_position()
        
    def __go_to_neutral_position(self):
        logging.debug(self.__class__.__name__ + ' - ' + '__init__' + ' ' + str(self.crt_angle1) + ", " + str(self.crt_angle2) + ' ' + self.message)
        
        pulse1 = from_degrees_to_pulse(self.crt_angle1)
        pulse2 = from_degrees_to_pulse(self.crt_angle2)
     
        self.bus.write_word_data(ADDR, self.channel1, 0)                   # chl 0 start time = 0us
        self.bus.write_word_data(ADDR, self.channel1 + OFFSET, pulse1)          # chl 0 end time = 1.5ms
        time.sleep(NEUTRAL_TRANS_PAUSE)

        self.bus.write_word_data(ADDR, self.channel2, 0)                   # chl 0 start time = 0us
        self.bus.write_word_data(ADDR, self.channel2 + OFFSET, pulse2)          # chl 0 end time = 1.5ms
        time.sleep(NEUTRAL_TRANS_PAUSE)
        
    def __move_upper_head(self, angle, steps):
        if self.crt_angle1 < angle:
            for angle_aux in range(self.crt_angle1, angle, steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, self.channel1 + OFFSET, pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle1 = angle
        else:
            for angle_aux in range(self.crt_angle1, angle, -steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, self.channel1 + OFFSET, pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle1 = angle
                
    def __move_lower_head(self, angle, steps):
        if self.crt_angle2 < angle:
            for angle_aux in range(self.crt_angle2, angle, steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, self.channel2 + OFFSET, pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle2 = angle
        else:
            for angle_aux in range(self.crt_angle2, angle, -steps):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, self.channel2 + OFFSET, pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle2 = angle
        
    def move(self, param_list):
        logging.debug(self.__class__.__name__ + ' - ' + 'move' + ' ' + self.message)
        
        angle1 = param_list[0]
        angle2 = param_list[1]
        steps = param_list[2]
        
        try:
            self.validator.check_angle(angle1)
            self.validator.check_angle(angle2)

            t_upper = threading.Thread(target=self.__move_upper_head, args=[angle1, steps])
            t_lower = threading.Thread(target=self.__move_lower_head, args=[angle2, steps])
            
            t_upper.daemon = True
            t_lower.daemon = True
            
            t_upper.start()
            t_lower.start()
            
            t_upper.join()
            t_lower.join()          
        except Exception as e:
            print(e)
