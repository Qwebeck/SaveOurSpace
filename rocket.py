import pygame as pg
from enums import *
from physics import *


vec = pg.math.Vector2





class Rocket(pg.sprite.Sprite):
    def __init__(self, game, x, y,fuel, weight, missileThrustMultiplier, allowed_collisions,lateralAcceleration,distanceToPlanet, initialVelocity, image ):
        self.groups = game.all_sprites,game.player_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.inMesosphere = False
        self.game = game
        self.score = 0
        self.MTmultiplier = missileThrustMultiplier
        self.image = pg.transform.scale(image, (ROCKET_W, ROCKET_H))
        self.rect = self.image.get_rect()
        #self.image = pg.image.load('rocket1.jpg')
        #self.rect = self.image.get_rect().scale(30,30)

        self.vel = vec(0, initialVelocity)
        self.pos = vec(x, y)
        self.rect.x = x
        self.rect.y = y
        
        self.fuel = fuel
        self.weight = weight
        self.game_over = False
        # parameter that descibes how fast the roket will go in different sides
        self.lateralAcceleration = lateralAcceleration
        self.velocityReduced = True

        self.allowed_collisions = allowed_collisions
        self.armour = 100
        self.collisions = 0
        self.distanceToPlanet = distanceToPlanet
        
        self.maxMissileThrust = 1
        self.missileThrust = 0
       
        self.acceleration = vec(0, 0)
        self.started = True 
        self.keys = None
        self.landing = False
        self.landed = False
        self.result = None
        self.last_update = 0
        self.frameNumber = 0
        
    # because there are conflicts in main constructor. You can't create planet object without created rocket and vice versa
    def initMaxMissileThrust(self,freeFallAccelaration):
        # Maximal allowed accelaration is acceleration of free fall on planet times . predefind upper boundary
        self.maxMissileThrust = calculateMaxMissleThrust(self,self.game.planet)
        
        self.maxMissileThrust = self.game.planet.freeFallAccelaration * self.MTmultiplier
        
        # Because rocket should wait untill user will press first key
        self.missileThrust = 0.8 * self.maxMissileThrust


    def move(self):
        #Lesser because of pygame cordinate system, which increases from up to down
        
        if self.landed:
             return
        
        if self.pos.x < 0:
            self.pos.x = self.game.WIDTH - 1
        elif self.pos.x > self.game.WIDTH:
            self.pos.x = 1

        
        
        # Function return acceleration in meters per second square
        self.acceleration.y = calculateAcceleration(self,self.game.planet,self.missileThrust)

        self.vel += self.acceleration * self.game.dt
        # Converting distance covered in meters to pixels
        
        coveredDistance = ( self.vel * self.game.dt ) / METERS_IN_ONE_PIXEL 
        # Rocket can move from side to side in any point of screen
        self.pos.x += coveredDistance.x * SMOOTHING_CONSTANT
        
        self.rect.x = self.pos.x


      
        
        # To make better impression of movement in the center of screen rocket will stop 
        if self.rect.y < self.game.HEIGHT * POSITION_CONSTANT  or self.distanceToPlanet <= self.game.HEIGHT * POSITION_CONSTANT *  METERS_IN_ONE_PIXEL:
            self.pos.y += coveredDistance.y
            self.rect.y = self.pos.y
            
        if self.game.planetAppeared:
            self.distanceToPlanet = self.rect.y - self.game.planet.rect.y
        else:
            self.distanceToPlanet -= coveredDistance.y * METERS_IN_ONE_PIXEL
        
        
 
    
    # Here check for keys user pressed 
    def processKeys(self):
        if self.keys[pg.K_LEFT]:
            self.acceleration.x = -self.lateralAcceleration
            
        elif self.keys[pg.K_RIGHT]:
            self.acceleration.x = self.lateralAcceleration
            
        elif self.keys[pg.K_UP]:
            self.change_thrust(Command.IncreaseThrust)
            
        elif self.keys[pg.K_DOWN]:
            self.change_thrust(Command.DecreaseThrust)
            
        elif self.keys[pg.K_SPACE]:
            
            self.landing = True
            
        else:
            pass
        self.keys = None

    def update(self):

        if self.armour <= 0:
            self.explosionAnimation()
        
        if self.game_over or self.landed:
            return
        self.processKeys()
        if not self.landing and self.started: 
            self.move()
        else:
            self.land()
        self.collide()

    def change_thrust(self, state):
        if state == Command.IncreaseThrust and self.missileThrust < self.maxMissileThrust:
            # Every time thrust will increase on 10 % of maxMissleThrust
            self.missileThrust += 0.05 * self.maxMissileThrust 
        elif state == Command.DecreaseThrust and self.missileThrust - 0.05 * self.maxMissileThrust > 0  :
            self.missileThrust -= 0.05 * self.maxMissileThrust
        elif state == Command.DecreaseThrust :
            self.missileThrust = 0    
  
    def explosionAnimation(self):
        # Stops background moving 
        self.game_over = True
        now = pg.time.get_ticks()
        if  now - self.last_update <= self.game.dt * 1000:
            return 
        else:
            self.last_update = now

        arr = self.game.explosionAnimationArray    
        if self.frameNumber < len(arr):
         
            self.image = pg.transform.scale(arr[self.frameNumber],(ROCKET_H, ROCKET_H))
            self.frameNumber += 1
        else:
            self.kill() 
        
    def collide(self):
        for obstacle in self.game.asteroids:
            if self.rect.colliderect(obstacle):
                if obstacle.type == ObstacleType.Asteroid and not obstacle.explosion:
                    self.collisions += 1
                    self.armour = round(1 - self.collisions/self.allowed_collisions,1) * 100
                elif obstacle.type == ObstacleType.Satellit and not obstacle.explosion:     
                    self.score += 1  
                obstacle.exploid()

    def onPlanetSurface(self):
        # if speed is smaller than ten meters per second than success
        self.landed = True
        if self.vel.y < 10 * self.armour:
            self.distanceToPlanet = 0
            self.result = Result.Success
            self.vel = vec(0,0)
            self.rect.y = self.game.planet.rect.y - self.rect.size[1]
            self.game_over = True
            self.game.afterMenu = False
        else:
            self.game.afterMenu = False
            self.game_over = True
            self.distanceToPlanet = 0
            self.result = Result.Fail
            self.rect.y = self.game.planet.rect.y - self.rect.size[1]
            self.explosionAnimation()



   

    
