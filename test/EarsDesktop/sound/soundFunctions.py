from enum import Enum

class TYPE_FUNCTION(Enum):
    SINUS = 1
    SQUARE = 2
    SAWTOOTH = 3
    TRIANGLE = 4
    WHITE_NOISE = 5
    PINK_NOISE = 6

    def __str__(self):
        if self.value == 1:
            return "Sinu"
        elif self.value == 2:
            return "Square"
        elif self.value == 3:
            return "Sawtoooth"
        elif self.value == 4:
            return "Triangle"
        elif self.value == 5:
            return "White Noise"
        elif self.value == 6:
            return "Pink Noise"

    
# TODO : Generate type function as enum
class soundFunction(object):
    pass