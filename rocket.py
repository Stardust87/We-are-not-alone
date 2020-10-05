from livewires import games, color
import pygame
import math
from laser import Laser
from flags import FLAGS
from explosion import Explosion

F_ALIEN = FLAGS["F_ALIEN"]
F_KIT = FLAGS["F_KIT"]
F_BALL = FLAGS["F_BALL"]

class Rocket(games.Sprite):
    """ rocket controlled by player """
    FLAG = FLAGS["F_ROCKET"]
    image = games.load_image("textures\\rocket.png", transparent = True)
    #rocket parameters
    MAX_HEALTH = 100
    MAX_SPEED = 2
    VELOCITY_STEP = 0.02
    ROTATION_STEP = 2
    BRAKE_STEP = 0.06
    SHOOT_DELAY = int(games.screen.fps*0.3)
    
    def __init__(self, game, x = games.screen.width/2, y = games.screen.height/2):
        super(Rocket, self).__init__(image = self.image, x = x, y = y)
        self.health = Rocket.MAX_HEALTH
        self.vx = 0
        self.vy = 0
        self.shoot_timer = 0
        self.game = game

        #displaying player's life bar on screen
        temp = str(self.health) + '%'
        self.display = games.Text(value = temp, 
                             size = 30,
                             color = color.green,
                             left = self.right + 5,
                             top = self.top,
                             is_collideable = False)
        games.screen.add(self.display)

    def update(self):
        """  executed once per frame """
        self.control()
        self.move()
        self.shoot()
        self.check_collision()

        #player's life bar update
        self.display.value = str(self.health) + '%'
        self.display.left = self.right + 5
        self.display.top = self.top
        if self.health < Rocket.MAX_HEALTH/2:
            self.display.color = color.red
        else:
            self.display.color = color.green
            

    def move(self):
        """ rocket movement """
        self.x += self.vx
        self.y += self.vy
        
        #when rocket goes beyond the screen, it shows on the opposite side
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height
            
        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width


    def get_position(self):
        """ rocket position """
        return (self.x, self.y)

    def get_distance(self, ship):
        """ distance from different game object """
        tempx = ship.x - self.x
        tempy = ship.y - self.y
        odl = math.sqrt((tempx)**2 + (tempy)**2)
        return odl
    
    def control(self):
        """ controls """

        #rotation
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Rocket.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Rocket.ROTATION_STEP
            
        #acceleration 
        if games.keyboard.is_pressed(games.K_UP):
            angle = self.angle * math.pi / 180
            self.vx += Rocket.VELOCITY_STEP * math.sin(angle)
            self.vy += Rocket.VELOCITY_STEP * -math.cos(angle)

        #speed limits
        self.vx = min(max(self.vx, -Rocket.MAX_SPEED), Rocket.MAX_SPEED)
        self.vy = min(max(self.vy, -Rocket.MAX_SPEED), Rocket.MAX_SPEED)
        
        #braking
        if games.keyboard.is_pressed(games.K_DOWN):
            if self.vx > 3*Rocket.BRAKE_STEP:
                self.vx -= Rocket.BRAKE_STEP * self.vx
            elif self.vx < -3*Rocket.BRAKE_STEP:
                self.vx += Rocket.BRAKE_STEP * -self.vx
            else:
                self.vx = 0
                
            if self.vy > 3*Rocket.BRAKE_STEP:
                self.vy -= Rocket.BRAKE_STEP * self.vy
            elif self.vy < -3*Rocket.BRAKE_STEP:
                self.vy += Rocket.BRAKE_STEP * -self.vy
            else:
                self.vy = 0

    def shoot(self):
        """ laser shooting """
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
        else:
            if games.keyboard.is_pressed(games.K_SPACE):          
                self.shoot_timer = Rocket.SHOOT_DELAY
                las = Laser(self.x, self.y, self.angle)
                games.screen.add(las)

    def change_hp(self, target):
        """ hp change after collision """
        self.health += target.value
        #repair kit add helath only if rocket has less than max health value 
        if self.health > Rocket.MAX_HEALTH:
            self.health = Rocket.MAX_HEALTH
        elif self.health <= 0:
            self.health = 0
            self.end_game()

    def end_game(self):
        """ game ending after player's failure """
        games.screen.clear()
        lose_message = games.Message(value = "You lost!",
                            size = 100,
                            color = color.black,
                            x = games.screen.width/2,
                            y = games.screen.height/2,
                            lifetime = games.screen.fps*4,
                            after_death = self.game.show_menu,
                            is_collideable = False)
        games.screen.add(lose_message)
        self.collide()
            
    def check_collision(self):
        """ check and operate collisions """
        #differnt colliding object causes different response actions
        for target in self.overlapping_sprites:
            if target.FLAG == F_ALIEN or \
               target.FLAG == F_KIT or \
               target.FLAG == F_BALL:
                self.change_hp(target)
                target.collide()
                
    def collide(self):
        """ rocket explosion """
        explo = Explosion(x = self.x,y = self.y)
        games.screen.add(explo)
        self.destroy()