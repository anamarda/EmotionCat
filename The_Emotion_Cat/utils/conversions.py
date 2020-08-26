from resources.global_variables import *

def from_degrees_to_pulse(value):
    return int(PULSE_VAR1 + PULSE_VAR2 * value)
    
def from_radians_to_degrees(value):
    return math.floor(value * DEGREES_VAR / PI)

def from_degrees_to_radians(value):
    return value * PI / DEGREES_VAR