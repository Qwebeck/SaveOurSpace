import pygame as pg
import random
from os import path
from enums import *

vec = pg.math.Vector2

class Obstacles(pg.sprite.Sprite):
    maxObstaclesInLine = 10
    obstaclesInLine = 0
    obstaclesInLineX = 0
    obstaclesInLineY = 0
    obstaclesInLineVel = 0
    obstaclesInLineVelY = 0
    obstaclesDirection = 0
    def __init__(self,game,group,image,type ):
        self.groups = group, game.all_sprites
        self.game = game
        self.satInit = False
        super().__init__()
        #number and x coordinates of allowed satellits in one line
        #self.image = pg.transform.scale(self.game.player_img, (180, 180))
        self.obstacle_img = image
        self.image = pg.transform.scale(self.obstacle_img, (OBSTACLES_SIZE, OBSTACLES_SIZE))
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = vec(random.randint(0,self.game.WIDTH),random.randint(int(self.game.HEIGHT * 1.5),self.game.HEIGHT * 3))
        self.rect.x = self.pos.x 
        self.rect.y = self.pos.y
        self.acc = vec(0,0)
        self.direction = vec(random.randint(-10,10)/10,1)
        self.vel = vec(random.randint(0,int(self.game.rocket.lateralAcceleration)) * self.direction.x,0)
        self.radius = int(self.rect.width * .5)
        self.explosion = False
        self.frameNumber = 0
        
        self.last_update = 0
        
        
     
        
    def reset(self,exploid=False):
        size = self.rect.size[0] 
        if  ((self.rect.y + size < 0  and self.game.rocket.vel.y > 0) or (self.rect.y - size > self.game.HEIGHT and self.game.rocket.vel.y < 0 ) or self.rect.x - size > self.game.WIDTH or self.rect.x + size  < 0 or exploid ) and not self.game.rocket.inMesosphere:
            if self.game.rocket.distanceToPlanet >= ASTEROID_BELT_HEIGHT:
                self.image = pg.transform.scale(random.choice(self.game.asteroidsArray),(OBSTACLES_SIZE, OBSTACLES_SIZE))
                # Because rocket can also move up
                self.type = ObstacleType.Asteroid
            else: 
                self.type = random.choice([ObstacleType.Satellit,ObstacleType.Asteroid,ObstacleType.AidSatellit])
                if self.type == ObstacleType.Satellit:
                    self.image = pg.transform.scale(self.game.sattelitsArray[0],(OBSTACLES_SIZE, OBSTACLES_SIZE))
                else:
                    self.image = pg.transform.scale(random.choice(self.game.asteroidsArray[1:2]),(OBSTACLES_SIZE, OBSTACLES_SIZE))
        
            if self.satInit == True and self.type == ObstacleType.Satellit and Obstacles.obstaclesInLine < Obstacles.maxObstaclesInLine or self.type == ObstacleType.AidSatellit:
                Obstacles.obstaclesInLine += 1
                self.pos.x = Obstacles.obstaclesInLineX
                self.vel.x = Obstacles.obstaclesInLineVel
                self.vel.y = Obstacles.obstaclesInLineVelY
                self.pos.y = Obstacles.obstaclesInLineY + OBSTACLES_SIZE
                self.direction.x = Obstacles.obstaclesDirection
                
                self.direction.y = 1

            elif self.type == ObstacleType.Satellit or self.type == ObstacleType.AidSatellit:
                Obstacles.obstaclesInLineX = random.randint(OBSTACLES_SIZE,self.game.WIDTH-OBSTACLES_SIZE)
                Obstacles.obstaclesInLineY = random.randint(self.game.HEIGHT ,self.game.HEIGHT + 200)
                Obstacles.obstaclesDirection = random.choice([1,-1])
                self.direction.x = Obstacles.obstaclesDirection 
                self.direction.y = 1
                self.pos.x = Obstacles.obstaclesInLineX
                self.pos.y = Obstacles.obstaclesInLineY
            
                self.vel.x = random.randint(0, self.game.rocket.lateralAcceleration) * self.direction.x
                Obstacles.obstaclesInLineVel = self.vel.x
                Obstacles.obstaclesInLineVelY = -random.randint(0, self.game.rocket.lateralAcceleration)                
                self.vel.y = Obstacles.obstaclesInLineVelY
                Obstacles.obstaclesInLine = 0
                self.satInit = True
            else:
                # goes down
                if self.game.rocket.vel.y > 0:
                    randomB = self.game.HEIGHT
                    randomE = self.game.HEIGHT + 200
                    multiplier = 1
                else:
                    randomB = 0
                    randomE = 200
                    multiplier = -1 
                self.pos.x = random.randint(OBSTACLES_SIZE,self.game.WIDTH-OBSTACLES_SIZE)
                self.pos.y = random.randint( randomB,randomE) * multiplier
                self.direction.x = random.choice([1,-1])
                self.direction.y = 1
                self.vel.x = random.randint(int(0.5 * self.game.planet.freeFallAccelaration),int(self.game.planet.freeFallAccelaration)) * self.direction.x
            
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
            



    def move(self):
       
        self.vel.y =  - self.game.rocket.vel.y 

        self.pos += self.vel * self.game.dt/METERS_IN_ONE_PIXEL * SMOOTHING_CONSTANT
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y 
    
    def update(self):
        self.move()
        self.reset()
        self.collide()
        if self.explosion:
            self.explosionAnimation()

    def collide(self):
        hits = pg.sprite.spritecollide(self,self.game.asteroids,False,pg.sprite.collide_circle)
        if hits and hits[0] != self:
            hits[0].exploid()
            self.exploid()
            
    
    
    def explosionAnimation(self):
        now = pg.time.get_ticks()
        if  now - self.last_update <= self.game.dt * 1000:
            return 
        else:
            self.last_update = now

        if self.type == ObstacleType.Satellit:
            arr = self.game.explosionAnimationArray
        else:
            
            arr = self.game.meteorExplosionAnimation
        
        if self.frameNumber < len(arr):
         
            self.image = pg.transform.scale(arr[self.frameNumber],(OBSTACLES_SIZE, OBSTACLES_SIZE))
            self.frameNumber += 1
        else:
            self.frameNumber = 0
            self.reset(exploid=True)
            self.explosion = False

    def exploid(self):
        self.vel.x = 0.1 * self.vel.x
        self.vel.y = -self.vel.y
        self.explosion = True

        

        