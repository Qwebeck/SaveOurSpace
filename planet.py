import pygame as pg 
from physics import *
class Planet(pg.sprite.Sprite):
    def __init__(self,game,weight,color,radius,image):
        super().__init__()
        self.game = game
        self.weight = weight        
        self.radius = radius
        self.freeFallAccelaration = calculateAcceleration(self.game.rocket,self)
        self.image = image
        
        self.rect = self.image.get_rect()
        self.rect.y = self.game.HEIGHT * 0.8 + self.rect.size[1]
        # self.rect.y = game.HEIGHT - self.rect.size[1]
        # self.rect.y = 

    def collision(self):
        for rocket in self.game.player_group:
            if self.rect.colliderect(rocket):
                rocket.onPlanetSurface()
                

    def update(self): 
        self.collision()
    

    