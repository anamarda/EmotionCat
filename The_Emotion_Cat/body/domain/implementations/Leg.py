#!/usr/bin/python
import time
import math
import logging
import threading
from resources.global_variables import *
from utils.conversions import *
from body.domain.interfaces.ILimb import ILimb
# 836 = 0 degrees
# 1250 = 45 degrees
# 1664 = 90 degrees


class Leg(ILimb):
    def __init__(
            self, 
            _channel1, _init_angle1, 
            _channel2, _init_angle2, 
            _message, _bus, _validator):
        logging.basicConfig(filename=LOGGER_PATH,level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + 
                        '__init__' + ' : ' + _message)
         
        self.channel1 = _channel1
        self.channel2 = _channel2
        self.crt_angle1 = _init_angle1
        self.crt_angle2 = _init_angle2
        self.message = _message        
        self.bus = _bus
        self.validator = _validator  
      
        self.__go_to_neutral_position()

    def __go_to_neutral_position(self):
        logging.debug(self.__class__.__name__ + ' - ' + 
                        '__init__' + self.message)
        
        pulse1 = from_degrees_to_pulse(self.crt_angle1)
        pulse2 = from_degrees_to_pulse(self.crt_angle2)

        self.bus.write_word_data(ADDR, self.channel1, 0)                   
        self.bus.write_word_data(ADDR, self.channel1 + OFFSET, pulse1)          
        time.sleep(NEUTRAL_TRANS_PAUSE)

        self.bus.write_word_data(ADDR, self.channel2, 0)                   
        self.bus.write_word_data(ADDR, self.channel2 + OFFSET, pulse2)          
        time.sleep(NEUTRAL_TRANS_PAUSE)

    def __correct_angles(self, q1, q2):
        if self.message in ['leg_right_front', 'leg_right_back']:
            return q1, q2
        if self.message in ['leg_left_front', 'leg_left_back']:
            return CORRECTING_VAR-q1, CORRECTING_VAR-q2

    def __move_upper_leg(self, angle1):
        if self.crt_angle1 < angle1:
            for angle_aux in range(self.crt_angle1, angle1, LEG_TRANS_STEP):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel1 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle1 = angle1
        else:
            for angle_aux in range(self.crt_angle1, angle1, -LEG_TRANS_STEP):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel1 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle1 = angle1
        
    def __move_lower_leg(self, angle2):
        if self.crt_angle2 < angle2:
            for angle_aux in range(self.crt_angle2, angle2, LEG_TRANS_STEP):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel2 + OFFSET, 
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle2 = angle2
        else:
            for angle_aux in range(self.crt_angle2, angle2, -LEG_TRANS_STEP):
                pulse_aux = from_degrees_to_pulse(angle_aux)
                self.bus.write_word_data(ADDR, 
                                        self.channel2 + OFFSET,
                                        pulse_aux) 
                time.sleep(TRANS_PAUSE)
                self.crt_angle2 = angle2
        
    def move_leg_with_given_angles(self, teta1, teta2):
        logging.debug(self.__class__.__name__ + ' - ' + 
                        'move_leg_with_given_angles' + ' ' + self.message)
        
        try:
            self.validator.check_angle(teta1)
            self.validator.check_angle(teta2)
            
            angle1 = int(teta1)
            angle2 = int(teta2)

            t_upper = threading.Thread(target=self.__move_upper_leg, 
                                        args=[angle1])
            t_lower = threading.Thread(target=self.__move_lower_leg, 
                                        args=[angle2])
            
            t_upper.daemon = True
            t_lower.daemon = True
            
            t_upper.start()
            t_lower.start()
            
            t_upper.join()
            t_lower.join()          
        except Exception as e:
            print(e)
    
    def move(self, param_list):
        '''
        This function uses the inverse kinematics to calculate 
        the angles for reaching a given location.
        
        Parameters
        -----------
            - x : a number on the Ox axis which specifies the 
                    end-effector location
            - y : a number on the Oy axis which specifies the 
                    end-effector location
        '''
        logging.debug(
            self.__class__.__name__ + ' - ' + 
            'move' + ' ' + self.message
                )
        
        x = param_list[0]
        y = param_list[1]
        
        try:          
            gamma = from_degrees_to_radians(LEG_ANGLE)
            a1 = THIGH_LENGTH
            a2 = CALF_LENGTH
            
            r = math.sqrt(x*x+y*y)
            phi1 = math.acos((a1*a1+r*r-a2*a2)/(IK_VAR*a1*r))
            phi2 = math.atan(y/x)
            q1 = phi2-phi1
            phi3 = math.acos((a1*a1+a2*a2-r*r)/(IK_VAR*a1*a2))
            q2 = phi3 - gamma
                        
            q1 = from_radians_to_degrees(q1)
            q2 = from_radians_to_degrees(q2)        
            
            self.validator.check_angle(q1)
            self.validator.check_angle(q2)
            
            q1, q2 = self.__correct_angles(q1, q2)         
            self.move_leg_with_given_angles(q1, q2)
        except Exception as e:
            print("(" + str(x) + " " + str(y) + ") --- error")
            
