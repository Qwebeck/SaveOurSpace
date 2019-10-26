from enum import Enum, auto


class Command(Enum):
    IncreaseThrust=auto()
    DecreaseThrust = auto()
 
class FuelConsumption(Enum):
    Low = auto()
    Medium = auto()
    High = auto()  

class Sensitivity(Enum):
    Low = auto()
    Medium = auto()
    High = auto()

class Weather(Enum):
    Sunny = auto()
    Rainy = auto()

class ObstacleType(Enum):
    Satellit = auto()
    Asteroid = auto()

class UnderneathBackground(Enum):
    Main = auto()
    Ancillary = auto()

class Result(Enum):
    Success = auto()
    Fail = auto()

FONT_NAME = 'StarJediHollow-A4lL.ttf'
METERS_IN_ONE_PIXEL = 0.01
OBSTACLES_SIZE = 30
INITIAL_DISTANCE = 10000
ASTEROID_BELT_HEIGHT = 1000 
NUMBER_OF_OBSTACLES = 8
ROCKET_W = 20
ROCKET_H = 70
# const to smooth movement of objects on screen
SMOOTHING_CONSTANT = 0.3
POSITION_CONSTANT = 0.2
YELLOW = (255,255,0)
RED = (255,255,0)
BLUE = (255,255,0)