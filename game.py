import pygame as pg 
import pygame as pg
from os import path
from rocket import *
from enums import *
from physics import *
from planet import *
from obstacles import *
import sys
class Game:
    def __init__(self):
        pg.init()
        self.WIDTH, self.HEIGHT = 800, 1000
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pg.time.Clock()
        self.playing = False
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.planet_group = pg.sprite.Group()
        self.trees = pg.sprite.Group()
        self.game_over = False
        self.dt = 0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.afterMenu = True
       
        self.load_data()
        
        self.background = self.spaceImage 
        self.background_rect = self.background.get_rect()
        self.second_background = self.spaceImage
        self.second_background_rect = self.second_background.get_rect()
        # Second background start just after first one 
        self.second_background_rect.y = self.background_rect.bottom

    
    def init_entities(self):
        #Rocket should be created first, because later there will be references to it in Game class 
        self.planetAppeared = False
        self.rocket = Rocket(self,x = self.WIDTH/2,
                                  y = POSITION_CONSTANT * self.HEIGHT,
                                  # weight is used to calculate how hard should  
                                  missileThrustMultiplier=self.rocketStats[self.selectedRocket]['missle'],
                                  allowed_collisions=self.rocketStats[self.selectedRocket]['allowed_collisions'],
                                  # lateral Acceleration should be given in meters per second
                                  lateralAcceleration=self.rocketStats[self.selectedRocket]['lateral_acc'],
                                  distanceToPlanet=self.planetStats[self.selectedPlanet]['initialHeight'],
                                  initialVelocity= 100,
                                  image=self.availableRocketsArray[self.selectedRocket]
                                  )
                               
        self.planet = Planet(game = self,
                             weight= self.planetStats[self.selectedPlanet]['weight'],
                             color = self.planetStats[self.selectedPlanet]['color'],
                             radius = self.planetStats[self.selectedPlanet]['radius'],
                             image = self.planetArray[self.selectedPlanet]
                             ) 
        
        self.planet_group.add(self.planet)
        self.rocket.initMaxMissileThrust(self.planet.freeFallAccelaration)
        
        for i in range(self.planetStats[self.selectedPlanet]['numberOfAster']):
            if self.planetStats[self.selectedPlanet]['initialHeight'] > ASTEROID_BELT_HEIGHT:
                m = Obstacles(self,self.asteroids,random.choice(self.asteroidsArray),
                            type=ObstacleType.Asteroid)
            else:
                m = Obstacles(self,self.asteroids,random.choice(self.asteroidsArray),
                        type=ObstacleType.Satellit)

            self.asteroids.add(m)
            self.background = self.spaceImage


        
    def load_data(self):
        self.explosionAnimationArray = []
        self.meteorExplosionAnimation = []
        self.availableRocketsArray = []
        self.asteroidsArray = []
        self.sattelitsArray =  []
        self.planetArray = []
        
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder,"images")
        self.planetStats = [
            {'initialHeight':20000,'radius':6371000*2, 'weight':5.972 * 10 ** 24, 'color': BLUE,'describeWeight':'Very heavy','describeHeight':'Very high', 'describeAsteroids': 'Some big number', 'numberOfAster':10},
            {'initialHeight':10000,'radius':6371000, 'weight':10.972 * 10 ** 24, 'color':RED,'describeWeight':'Normal','describeHeight':'Not very high', 'describeAsteroids':'Even bigger number', 'numberOfAster':20},

        ]
        
        self.rocketStats = [
            {'allowed_collisions':20,'lateral_acc':20,'missle': 2, 'describeArmour':'Strong armour','describeManevrity':'Low maneuverability','decribeBrakingAbility':'Perfect'},
            {'allowed_collisions':10,'lateral_acc':20,'missle': 4,'describeArmour':'Medium armour','describeManevrity':'Medium maneuverability','decribeBrakingAbility':'Medium'},
            {'allowed_collisions':5,'lateral_acc':30,'missle': 7, 'describeArmour':'Poor armour','describeManevrity':'High maneuverability','decribeBrakingAbility':'Poor'}
        ]
        self.selectedPlanet = 0
        self.selectedRocket = 0
        self.startedAncillary = False
        self.fireTraceArray = {
            'weakTrace':pg.image.load(path.join(self.img_folder,"spaceEffects_001.png")).convert_alpha(),
            'strongTrace':pg.image.load(path.join(self.img_folder,"spaceEffects_002.png")).convert_alpha()
        }
         
        for i in [1,2]:
            filename = "Planet{}.jpg".format(i)
            img = pg.transform.scale(pg.image.load(path.join(self.img_folder,filename)).convert_alpha(),(self.WIDTH,int(0.1 * self.HEIGHT)))
            img.set_colorkey((0,0,0))
            self.planetArray.append(img)

        for i in range(10,16):
            filename = "spaceEffects_0{}.png".format(i)
            img = pg.image.load(path.join(self.img_folder,filename)).convert_alpha()
            img.set_colorkey((0,0,0))
            self.meteorExplosionAnimation.append(img)

        for i in range(9):
            filename = "regularExplosion0{}.png".format(i)
            img = pg.image.load(path.join(self.img_folder,filename)).convert_alpha()
            img.set_colorkey((0,0,0))
            self.explosionAnimationArray.append(img)
        for i in [1,2,3]:
            filename = "spaceMeteors_00{}.png".format(i)
            filename1 = "spaceBuilding_0{}.png".format(i)
            filename2 = "spaceRockets_00{}.png".format(i)
            img = pg.image.load(path.join(self.img_folder,filename)).convert_alpha()
            img1 = pg.image.load(path.join(self.img_folder,filename1)).convert_alpha()
            img2 = pg.image.load(path.join(self.img_folder,filename2)).convert_alpha()
            img.set_colorkey((0,0,0))
            img1.set_colorkey((0,0,0))
            img2.set_colorkey((0,0,0))
            self.asteroidsArray.append(img)
            self.sattelitsArray.append(img1)
            self.availableRocketsArray.append(pg.transform.scale(img2,(ROCKET_W,ROCKET_H)))
        

        self.spaceImage = pg.image.load(path.join(self.img_folder,"Stars.jpg")).convert_alpha()

    def run(self):
        self.playing = True
        self.showMenu()
        self.init_entities()
        while self.playing:
            if self.afterMenu == True:
                #Number of miliseconds from last farme
                self.dt = self.clock.tick(60) / 1000
                for event in pg.event.get():
                    
                    if event.type == pg.QUIT:
                    
                        self.playing = False
                if not self.rocket.landed:
                    
                    self.rocket.keys = pg.key.get_pressed()
                    self.screen.fill((0,0,0))  
                    self.update()
                self.draw()
            if self.rocket.game_over:
                self.process_keys_end_game()
    
    def draw_trace(self):
        if self.rocket.missileThrust == 0:
            return
        elif self.rocket.missileThrust <= 0.5:
            image = self.fireTraceArray['weakTrace']
        else:
            image = self.fireTraceArray['strongTrace']
        # self.rocket.missileThrust/self.rocket.maxMissileThrust multiplier that shows how big is power of of thrust
        trace = pg.transform.scale(image, (ROCKET_W, int(self.rocket.missileThrust/self.rocket.maxMissileThrust *ROCKET_H)))
        trace_rect = trace.get_rect()
        trace_rect.x = self.rocket.rect.x
        trace_rect.y = self.rocket.rect.center[1] + ROCKET_H/2
        self.screen.blit(trace,trace_rect)

    def move_background(self,menu = False):
        
        if menu:
            new_pos = 20 * self.clock.tick(60) / 1000 /METERS_IN_ONE_PIXEL * SMOOTHING_CONSTANT
            if self.background_rect.bottom < 0:
                self.background_rect.y = self.second_background_rect.bottom
            if self.second_background_rect.bottom < 0:
                self.second_background_rect.y = self.background_rect.bottom
            self.background_rect.y -= int(new_pos)
            self.second_background_rect.y -= int(new_pos)
            
            self.screen.blit(self.background,self.background_rect)
            self.screen.blit(self.second_background,self.second_background_rect)

            return
        else:
            new_pos = self.rocket.vel.y * self.dt/METERS_IN_ONE_PIXEL * SMOOTHING_CONSTANT
        # In such way i prevent black holes, that could appear between two backgrounds ,
        
        # Int cast made because when we make operations on numerical we can get 
        # a different speed for two different objects even while adding the same number
        
        self.background_rect.y -= int(new_pos)
        self.second_background_rect.y -= int(new_pos)
        
        # self.rocket.vel > 0 -- means that object is moving up
 
        

        if self.background_rect.bottom < 0 and self.rocket.vel.y > 0:
            self.background_rect.y = self.second_background_rect.bottom
        
        elif self.background_rect.top > self.HEIGHT and self.rocket.vel.y < 0:
            
            self.background_rect.y = self.second_background_rect.y -self.background_rect.size[1]

        if self.second_background_rect.bottom < 0 and (menu or self.rocket.vel.y > 0 ):
            self.second_background_rect.y = self.background_rect.bottom 
        elif self.second_background_rect.top > self.HEIGHT and self.rocket.vel.y < 0:
            
            self.second_background_rect.y = self.background_rect.y -self.background_rect.size[1]
            
    
    def draw_background(self):
        
        self.screen.blit(self.background,self.background_rect)
        self.screen.blit(self.second_background,self.second_background_rect)

    # global function to draw everythin that should be drowna
    def draw(self):
        # self.screen.blit(self.background,(0,0))
     
        self.draw_background()
        if not self.planetAppeared and not self.rocket.game_over:
            self.move_background()
            self.draw_trace()
            self.asteroids.draw(self.screen)
        
        
        
        
        if self.rocket.distanceToPlanet <= self.HEIGHT * METERS_IN_ONE_PIXEL * 2:
            self.rocket.inStratosphere = True 

        if self.rocket.distanceToPlanet <= self.HEIGHT * METERS_IN_ONE_PIXEL:
             self.planet_group.draw(self.screen)
             self.planetAppeared = True
             self.rocket.inStratosphere = True  
        
        self.player_group.draw(self.screen)    
        self.draw_data()
        
        pg.display.flip()

    # support function to render and draw test on prefined different positions
    def draw_text(self, text, size, color, x, y, font):
      
        font = pg.font.Font(font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    
    def showMenu(self):
        running = True
        params = {'planet':False,'rocket':False}
        current_param = 0
        while running:
            last_update = pg.time.get_ticks()
            stats = self.planetStats[self.selectedPlanet]
            self.move_background(menu = True)
            self.draw_text("Navigate with right/left arrows", 
                            21, 
                            YELLOW,
                            0.45 * self.WIDTH,
                            0.6 * self.HEIGHT, 
                            FONT_NAME)
            self.draw_text("Press Enter to submit", 
                            21, 
                            YELLOW,
                            0.62 * self.WIDTH,
                            0.65 * self.HEIGHT, 
                            FONT_NAME)  
            self.draw_text("Press Escape to exit", 
                            21, 
                            YELLOW,
                            0.62 * self.WIDTH,
                            0.7 * self.HEIGHT, 
                            FONT_NAME)     
            if not params['planet']:
                self.draw_text("Choose a planet", 
                            35, 
                            YELLOW,
                            0.2 * self.WIDTH,
                            0.1 * self.HEIGHT, 
                            FONT_NAME)    
                self.draw_text("Planet weight:", 
                            30, 
                            YELLOW,
                            0.1 * self.WIDTH,
                            0.2 * self.HEIGHT, 
                            FONT_NAME)
                self.draw_text(str(self.planetStats[self.selectedPlanet]['describeWeight']), 
                            30, 
                            YELLOW,
                            0.1 * self.WIDTH,
                            0.25 * self.HEIGHT, 
                            FONT_NAME)
                self.draw_text("Start height:", 
                            30, 
                            YELLOW,
                            0.1 * self.WIDTH,
                            0.3 * self.HEIGHT, 
                            FONT_NAME)
                self.draw_text(str(self.planetStats[self.selectedPlanet]['describeHeight']), 
                            30, 
                            YELLOW,
                            0.1 * self.WIDTH,
                            0.35 * self.HEIGHT, 
                            FONT_NAME)
                self.draw_text("Asteroids:", 
                            30, 
                            YELLOW,
                            0.5 * self.WIDTH,
                            0.2 * self.HEIGHT, 
                            FONT_NAME)
                self.draw_text(str(self.planetStats[self.selectedPlanet]['describeAsteroids']), 
                            30, 
                            YELLOW,
                            0.5 * self.WIDTH,
                            0.25 * self.HEIGHT, 
                            FONT_NAME)

                self.process_keys_in_menu('planet',params)

            elif not params['rocket']:
                self.draw_text("Choose a rocket", 
                            35, 
                            YELLOW,
                            0.2 * self.WIDTH,
                            0.1 * self.HEIGHT, 
                            FONT_NAME)   
                self.draw_text("Manevreability: ", 
                            30, 
                            YELLOW,
                            0.05 * self.WIDTH,
                            0.2 * self.HEIGHT, 
                            FONT_NAME)
                self.draw_text(str(self.rocketStats[self.selectedRocket]['describeManevrity']), 
                            30, 
                            YELLOW,
                            0.1 * self.WIDTH,
                            0.25 * self.HEIGHT, 
                            FONT_NAME)
                self.draw_text("Armour: ", 
                            30, 
                            YELLOW,
                            0.05 * self.WIDTH,
                            0.3 * self.HEIGHT, 
                            FONT_NAME)
                self.draw_text(str(self.rocketStats[self.selectedRocket]['describeArmour']), 
                            30, 
                            YELLOW,
                            0.1 * self.WIDTH,
                            0.35 * self.HEIGHT, 
                            FONT_NAME)
                
               
                       
                running =  self.process_keys_in_menu('rocket',params)

            planet = self.planetArray[self.selectedPlanet]
            
            rocket = pg.transform.scale(self.availableRocketsArray[self.selectedRocket],(2 * ROCKET_W,2 * ROCKET_H))
            
            
            self.screen.blit(planet,(0,0.9 * self.HEIGHT))
            y = 0.2 * self.HEIGHT if params['planet'] else  0.8 * self.HEIGHT
            
            self.screen.blit(rocket,(0.9 * self.WIDTH,y))
            self.afterMenu = True
            pg.display.flip()

    def process_keys_in_menu(self,parametr,params=[],*args):
        for event in pg.event.get():    
            if event.type == pg.QUIT:
                    self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                
                if event.key == pg.K_RIGHT:
                    if parametr == 'planet':
                        self.selectedPlanet = (self.selectedPlanet + 1 ) % len(self.planetStats)
                        return True
                    elif parametr == 'rocket':
                        self.selectedRocket = (self.selectedRocket + 1 ) % len(self.availableRocketsArray)
                        return True
                if event.key == pg.K_LEFT:
                    if parametr == 'planet':
                        if self.selectedPlanet > 0 : self.selectedPlanet -= 1  
                        else : self.selectedPlanet = len(self.planetStats) - 1   
                        return True
                    elif parametr == 'rocket':
                        if self.selectedRocket > 0 : self.selectedRocket -= 1 
                        else : self.selectedRocket = len(self.availableRocketsArray) - 1 
                    return True
                if event.key == pg.K_RETURN:
                    params[parametr] = True
            
                    if params['planet'] and params['rocket']:
                    # Starts game here
                        self.background = self.spaceImage
                        return False
        return True
    
    
    def quit(self):
        pg.quit()
        sys.exit()
    # draw stats that rocket have at this moment  
    def draw_data(self):
        if not self.rocket.game_over:
            
            
            self.draw_text("Score :", 
                            21, 
                            YELLOW,
                            0.05 * self.WIDTH,
                            0.1 * self.HEIGHT, 
                            FONT_NAME)
            self.draw_text(str(self.rocket.score), 
                            21, 
                            YELLOW,
                            0.1 * self.WIDTH,
                            0.15 * self.HEIGHT, 
                            FONT_NAME)
            self.draw_text("Armour :", 
                            21, 
                            YELLOW,
                            0.05 * self.WIDTH,
                            0.2 * self.HEIGHT, 
                            FONT_NAME)
            self.draw_text(str(self.rocket.armour), 
                            21, 
                            YELLOW,
                            0.1 * self.WIDTH,
                            0.25 * self.HEIGHT, 
                            FONT_NAME)
            if self.rocket.cured:
                self.draw_text("+ armour", 
                            21, 
                            YELLOW,
                            0.1 * self.WIDTH,
                            0.3 * self.HEIGHT, 
                            FONT_NAME)

            self.draw_text("Distance to Planet :", 
                            21, 
                            YELLOW,
                            0.6 * self.WIDTH,
                            0.1 * self.HEIGHT, 
                            FONT_NAME)
            self.draw_text(str(int(self.rocket.distanceToPlanet)) +" m" ,21,
                            YELLOW, 
                            0.65 * self.WIDTH,
                            0.15 * self.HEIGHT, 
                            FONT_NAME)
            self.draw_text("Velocity:", 
                            21, 
                            YELLOW,
                            0.6 * self.WIDTH,
                            0.2 * self.HEIGHT, 
                            FONT_NAME)
            

            self.draw_text(str(abs(int(self.rocket.vel.y))) +" m/s" ,21,
                            YELLOW, 
                            0.65 * self.WIDTH,
                            0.25 * self.HEIGHT, 
                            FONT_NAME)
            self.draw_text("Save landing:", 
                            21, 
                            YELLOW,
                            0.65 * self.WIDTH,
                            0.3 * self.HEIGHT, 
                            FONT_NAME)
            

            self.draw_text(str(abs(int(10 * self.rocket.armour))) +" m/s" ,21,
                            YELLOW, 
                            0.6 * self.WIDTH,
                            0.35 * self.HEIGHT, 
                            FONT_NAME)
            
        if self.rocket.vel.y < 0 :
            self.draw_text("You are going up" ,30,
                        (155,155,155), 
                         0.4 * self.WIDTH,
                         0.8 * self.HEIGHT, 
                         FONT_NAME)


        if self.rocket.landed and self.rocket.result == Result.Success: 
            self.draw_text("A long time ago  ", 
                                30, 
                                YELLOW,
                                0.1 * self.WIDTH,
                                0.2 * self.HEIGHT, 
                                FONT_NAME)
            self.draw_text("in a galaxy far, far away .... ", 
                                30, 
                                YELLOW,
                                0.1 * self.WIDTH,
                                0.25 * self.HEIGHT, 
                                FONT_NAME)
            self.draw_text("Was borned a great hero, ", 
                                30, 
                                YELLOW,
                                0.1 * self.WIDTH,
                                0.3 * self.HEIGHT, 
                                FONT_NAME)
            self.draw_text("whose mission was to Save Our Space ! ", 
                                30, 
                                YELLOW,
                                0.1 * self.WIDTH,
                                0.35 * self.HEIGHT, 
                                FONT_NAME)
            self.draw_text("Enter - again ", 
                                30, 
                                YELLOW,
                                0.55 * self.WIDTH,
                                0.4 * self.HEIGHT, 
                                FONT_NAME)
            self.draw_text("Escape - close ", 
                                30, 
                                YELLOW,
                                0.6 * self.WIDTH,
                                0.45 * self.HEIGHT, 
                                FONT_NAME)
        elif (self.rocket.landed and self.rocket.result == Result.Fail) or self.rocket.game_over:
            self.draw_text("You failed ", 
                                30, 
                                YELLOW,
                                0.4 * self.WIDTH,
                                0.8 * self.HEIGHT, 
                                FONT_NAME)
            self.draw_text("Enter - again ", 
                                30, 
                                YELLOW,
                                0.4 * self.WIDTH,
                                0.2 * self.HEIGHT, 
                                FONT_NAME)
            self.draw_text("Escape - close ", 
                                30, 
                                YELLOW,
                                0.4 * self.WIDTH,
                                0.3 * self.HEIGHT, 
                                FONT_NAME)
    
    def process_keys_end_game(self):
        for event in pg.event.get():    
            if event.type == pg.QUIT:
                    self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_RETURN:
                    self.rocket.game_over = False
                    self.rocket.landed = False
                    self.planetAppeared = False
                    self.inStratosphere = False
                    self.rocket.kill()
                    for sprite in self.asteroids:
                            sprite.kill()
                    self.showMenu()
                    self.init_entities()
                    
                

    def update(self):  
       self.planet_group.update()
       self.asteroids.update()
       self.rocket.update()
       #self.all_sprites.update()
      
g = Game()

g.run()