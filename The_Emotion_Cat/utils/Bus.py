import smbus
import time
import logging
from resources.global_variables import * 

class Bus:
    def __init__(self):
        logging.basicConfig(filename=LOGGER_PATH, level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + '__init__')
        
        self.bus = smbus.SMBus(1)  # the chip is on bus 1 of the available I2C buses
        self.addr = ADDR           # I2C address of the PWM chip.

        self.bus.write_byte_data(
            self.addr, 
            BUS_CONFIG_OFFSET1, 
            BUS_CONFIG_DATA1
                )                   # enables word writes
                
        self.bus.write_byte_data(
            self.addr, 
            BUS_CONFIG_OFFSET2, 
            BUS_CONFIG_DATA2
                )                   # configure the chip for multi-byte write

        time.sleep(0.1)
    
    def get_bus(self):
        logging.debug(self.__class__.__name__ + ' - ' + 'get_bus')
        return self.bus