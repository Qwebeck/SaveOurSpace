import pygame as pg 
from math import sqrt
from enums import *


def calculateAcceleration(Rocket,Planet,missileThrust = 0):
    
    acceleration = (Planet.weight * 6.67 / (10 ** 11 * (Rocket.distanceToPlanet + Planet.radius) ** 2)) - missileThrust
    
    #acceleration = 6,674 * Planet.weight / (Rocket.distanceToPlanet ** 2 * 10 ** 11) - Rocket.missileThrust
    # Cast made because of problems, that could be caused by arythmetic on floating point numbers
    # Cast to int doesn't made, because there could bi situations, where we need an output, but function will return 0, and ricket will stand in place.
    # Example of such situation- when you chnging direction on your rocket
    return acceleration

def calculateMaxMissleThrust(Rocket,Planet):
    # maxThrust is a parameter, that shows maximum acceleration, that could be produced by rocket engine.
    # Calculated next formula
    # First escape velocity / time in seconds that usually takes a launch ( 9 minutes. Source - nasa website )
    maxThrust = sqrt(( 2 * Planet.weight * 6.67 ) / ( 10 ** 11 * Planet.radius )) 
    
    return int(maxThrust)


