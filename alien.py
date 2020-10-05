from livewires import  color
import config 
import pygame
import  random
from  explosion import Explosion
from flags import FLAGS
from ball import Ball

games = config.games1

F_rocket= FLAGS["F_ROCKET"]
F_KIT = FLAGS["F_KIT"]
F_BALL = FLAGS["F_BALL"]
F_LASER = FLAGS["F_LASER"]
class Alien(games.Sprite):
    """ alien spaceship """
    FLAG = FLAGS["F_ALIEN"]

    #actual aliens
    count = 0

    image = games.load_image("textures\\alien.png",
                            transparent = True)

    #spaceship parameters
    MAX_HEALTH = 100
    MAX_SPEED = 1
    SHOOT_DELAY = 4*games.screen.fps
    VALUE = 40

    def __init__(self):
        #random initial coords
        y = random.randint(0, games.screen.height)
        super(Alien, self).__init__(image = self.image, right = 0, y = y)
        self.health = Alien.MAX_HEALTH
        self.shoot_timer = Alien.SHOOT_DELAY
        self.set_move()
        self.value = -Alien.VALUE
        Alien.count += 1

    def update(self):
        """ executed once per frame """
        self.move()
        self.shoot()
        self.check_collision()

    def move(self):
        """ spaceship movement """

        #when spaceship goes beyond the screen, it shows on the opposite side
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height
            
        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width
        
        

    def set_move(self):
        """ motion mode choice """
        #random initial speed
        temp = random.uniform(Alien.MAX_SPEED*0.3, Alien.MAX_SPEED)
        self.dx = random.choice([-1, 1])*temp
        self.dy = random.choice([-1, 1])*(Alien.MAX_SPEED - abs(self.dx))

    def shoot(self):
        """ missile shooting """
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
        # missile is ready after shoot delay time
        else:
            self.shoot_timer = Alien.SHOOT_DELAY
            temp = random.randrange(359)
            bal = Ball(self.x, self.y, temp)
            games.screen.add(bal)

    def change_hp(self, target):
        """ hp change after collision """
        self.health += target.value
        if self.health > Alien.MAX_HEALTH:
            self.health = Alien.MAX_HEALTH
        elif self.health <= 0:
            self.health = 0
            self.collide()

    def check_collision(self):
        """ check and operate collisions """
        for target in self.overlapping_sprites:
            if target.FLAG == F_LASER:
                self.change_hp(target)
                target.collide()
    
    def collide(self):
        """ spaceship explosion """
        #actual aliens number decreases
        Alien.count -= 1
        explo = Explosion(x = self.x,y = self.y)
        games.screen.add(explo)
        self.destroy()