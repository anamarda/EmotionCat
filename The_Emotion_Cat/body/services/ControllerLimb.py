import concurrent.futures
import logging
from body.domain.implementations.Leg import Leg
from body.domain.implementations.Tail import Tail
from body.domain.implementations.Head import Head
from resources.global_variables import *

class ControllerLimb:
    def __init__(self, _repo, _bus, _validator):
        logging.basicConfig(filename=LOGGER_PATH,level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + '__init__')
        
        self.repo = _repo
        self.bus = _bus
        self.validator = _validator
        
        self.addresses_dict = self.repo.get_addresses_dict() 
        self.channels = []
        self.limb_dict = {}
      
        self.__set_dict()
   
    def __set_leg_channels(self):
        logging.debug(self.__class__.__name__ + ' - ' + '__set_channels')
        
        channel1_str = self.addresses_dict[LEG_RIGHT_FRONT_UP][0]
        channel1_int = int(channel1_str, HEX_BASE)
        channel2_str = self.addresses_dict[LEG_RIGHT_FRONT_DOWN][0]
        channel2_int = int(channel2_str, HEX_BASE)         
        self.channels.append([channel1_int, channel2_int])

        channel1_str = self.addresses_dict[LEG_LEFT_FRONT_UP][0]
        channel1_int = int(channel1_str, HEX_BASE)
        channel2_str = self.addresses_dict[LEG_LEFT_FRONT_DOWN][0]
        channel2_int = int(channel2_str, HEX_BASE)
        self.channels.append([channel1_int, channel2_int])

        channel1_str = self.addresses_dict[LEG_RIGHT_BACK_UP][0]
        channel1_int = int(channel1_str, HEX_BASE)
        channel2_str = self.addresses_dict[LEG_RIGHT_BACK_DOWN][0]
        channel2_int = int(channel2_str, HEX_BASE)
        self.channels.append([channel1_int, channel2_int])

        channel1_str = self.addresses_dict[LEG_LEFT_BACK_UP][0]
        channel1_int = int(channel1_str, HEX_BASE)
        channel2_str = self.addresses_dict[LEG_LEFT_BACK_DOWN][0]
        channel2_int = int(channel2_str, HEX_BASE)
        self.channels.append([channel1_int, channel2_int])
        
    def __set_tail_channels(self):
        logging.debug(self.__class__.__name__ + ' - ' + '__set_channels')
        
        channel1_str = self.addresses_dict[TAIL][0]
        channel1_int = int(channel1_str, HEX_BASE)        
        self.channels.append([channel1_int])
        
    def __set_head_channels(self):
        logging.debug(self.__class__.__name__ + ' - ' + '__set_channels')
        
        channel1_str = self.addresses_dict[HEAD_UP][0]
        channel1_int = int(channel1_str, HEX_BASE) 
        channel2_str = self.addresses_dict[HEAD_DOWN][0]
        channel2_int = int(channel2_str, HEX_BASE)        
        self.channels.append([channel1_int, channel2_int])
         
    def __set_dict(self):
        logging.debug(self.__class__.__name__ + ' - ' + '__set_leg_dict_sequential')
    
        self.__set_leg_channels()
        self.__set_tail_channels()
        self.__set_head_channels()
    
        leg_right_front = Leg(
            self.channels[0][0], 
            LEG_RIGHT_FRONT_UP_START_ANGLE, 
            self.channels[0][1], 
            LEG_RIGHT_FRONT_DOWN_START_ANGLE, 
            "leg_right_front", 
            self.bus,
            self.validator
                )
        self.limb_dict['leg_right_front'] = leg_right_front
        
        leg_left_front = Leg(
            self.channels[1][0], 
            LEG_LEFT_FRONT_UP_START_ANGLE, 
            self.channels[1][1], 
            LEG_LEFT_FRONT_DOWN_START_ANGLE, 
            "leg_left_front",
            self.bus,            
            self.validator
                )
        self.limb_dict['leg_left_front'] = leg_left_front
        
        leg_right_back = Leg(
            self.channels[2][0], 
            LEG_RIGHT_BACK_UP_START_ANGLE, 
            self.channels[2][1], 
            LEG_RIGHT_BACK_DOWN_START_ANGLE, 
            "leg_right_back",
            self.bus,
            self.validator
                )
        self.limb_dict['leg_right_back'] = leg_right_back
        
        leg_left_back = Leg(
            self.channels[3][0], 
            LEG_LEFT_BACK_UP_START_ANGLE, 
            self.channels[3][1], 
            LEG_LEFT_BACK_DOWN_START_ANGLE, 
            "leg_left_back", 
            self.bus,
            self.validator
                )
        self.limb_dict['leg_left_back'] = leg_left_back 
        
        tail = Tail(
            self.channels[4][0], 
            TAIL_START_ANGLE, 
            "tail", 
            self.bus,
            self.validator
                )
        self.limb_dict['tail'] = tail 
        
        head = Head(
            self.channels[5][0], 
            HEAD_UP_START_ANGLE, 
            self.channels[5][1], 
            HEAD_DOWN_START_ANGLE, 
            "head", 
            self.bus,
            self.validator
                )
        self.limb_dict['head'] = head         
        
    def move_limb(self, limb, param_list):
        logging.debug(self.__class__.__name__ + ' - ' + limb)
        self.limb_dict[limb].move(param_list)
    '''    
    def ik_move_leg_right_front(self, coordX, coordY):
        logging.debug(self.__class__.__name__ + ' - ' + 'ik_move_leg_right_front')
        self.limb_dict['leg_right_front'].move([coordX, coordY])
        
    def ik_move_leg_left_front(self, coordX, coordY):
        logging.debug(self.__class__.__name__ + ' - ' + 'ik_move_leg_left_front')
        self.limb_dict['leg_left_front'].move([coordX, coordY])
        
    def ik_move_leg_right_back(self, coordX, coordY):
        logging.debug(self.__class__.__name__ + ' - ' + 'ik_move_leg_right_back')
        self.limb_dict['leg_right_back'].move([coordX, coordY])
        
    def ik_move_leg_left_back(self, coordX, coordY):
        logging.debug(self.__class__.__name__ + ' - ' + 'ik_move_leg_left_back')
        self.limb_dict['leg_left_back'].move([coordX, coordY])

    def move_tail(self, angle, steps):
        logging.debug(self.__class__.__name__ + ' - ' + 'move_tail')
        self.limb_dict['tail'].move([angle, steps])
        
    def move_head(self, angle1, angle2, steps):
        logging.debug(self.__class__.__name__ + ' - ' + 'move_head')
        self.limb_dict['head'].move([angle1, angle2, steps])
    '''
