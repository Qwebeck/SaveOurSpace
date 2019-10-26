from enum import Enum, auto


class Command(Enum):
    IncreaseThrust=auto()
    DecreaseThrust = auto()

class ObstacleType(Enum):
    Satellit = auto()
    Asteroid = auto()
    # Return armour to rocket if picked
    AidSatellit = auto()

class UnderneathBackground(Enum):
    Main = auto()
    Ancillary = auto()

class Result(Enum):
    Success = auto()
    Fail = auto()

FONT_NAME = 'StarJediHollow-A4lL.ttf'
METERS_IN_ONE_PIXEL = 0.1
OBSTACLES_SIZE = 30

# Height below what doesn't appeare satellits
ASTEROID_BELT_HEIGHT = 15000 

ROCKET_W = 20
ROCKET_H = 70
# const to smooth movement of objects on screen
SMOOTHING_CONSTANT = 0.5
# POSITION_CONSTANT will be later multiplied by height of screen. 
# This constants allows us to describe where on screen rocket should stay 
POSITION_CONSTANT = 0.2 
YELLOW = (255,255,0)
RED = (255,255,0)
BLUE = (255,255,0)
