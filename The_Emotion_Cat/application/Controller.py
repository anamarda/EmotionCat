from resources.global_variables import OWNERS_PATH
import os 

class Controller:
    def __init__(self, _validator, _cat):
        self.validator = _validator
        self.cat = _cat
        
    def get_owners(self):
        return [f for f in os.listdir(OWNERS_PATH)]

    def start_emotion_prediction(self, name):
        self.validator.validate_name(name)
        self.cat.start(name)
        
    def register_owner(self, name):
        self.validator.validate_name(name)
        # apelat create_dataset
        print(name)
        
    def train(self, epochs, lr, decay):
        self.validator.validate_number(epochs)
        self.validator.validate_number(lr)
        self.validator.validate_number(decay)
        # facut clasa
        print(epochs)
        print(lr)
        print(decay)
