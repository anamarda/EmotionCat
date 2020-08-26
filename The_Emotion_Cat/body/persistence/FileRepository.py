import logging
import os
from resources.global_variables import LOGGER_PATH, ADDRESSES_FILE_PATH

class FileRepository:
    def __init__(self):    
        logging.basicConfig(filename=LOGGER_PATH, level=logging.DEBUG)
        logging.debug(self.__class__.__name__ + ' - ' + '__init__')
        
        self.filename = ADDRESSES_FILE_PATH
        self.addresses_dict = {}
        self.__read_from_file()
        
    def __read_from_file(self):
        logging.debug(self.__class__.__name__ + ' - ' + '__read_from_file')
        with open (self.filename) as f:
            lines = f.readlines()
            lines = lines[1:]
            for line in lines:
                cols = line.strip().split(',')
                channel = cols[0]
                start = cols[1]
                stop = cols[2]
                self.addresses_dict[channel] = [start, stop]
    
    def get_addresses_dict(self):
        logging.debug(self.__class__.__name__ + ' - ' + 'get_addresses_dict')
        return self.addresses_dict
