class GuiException(Exception):
    def __init__(self, _message):
        '''
        Constructor.
        
        Paramaters
        -----------
            - _message: string, the error message
        '''
        self.message = _message
    
    def get_message(self):
        '''
        Getter of the message field.
        
        Return
        -------
            - string, the error message
        '''
        return self.message

class Validator():
    def __init__(self):
        pass
    
    def validate_name(self, name):
        '''
        String validation.
        
        Paramaters
        -----------
            - name: string
        
        Raise
        ------
            - GuiException, if the name is None or the null string
        '''
        if name == "" or name == None:
            raise GuiException("Invalid name.")
        
    def validate_number(self, number):
        '''
        Float nuber validation.
        
        Paramaters
        -----------
            - number: string
        
        Raise
        ------
            - GuiException, if the number can not be converted into 
                float. 
        '''
        try:
            float(number)
        except Exception:
            raise GuiException("Invalid number.")
