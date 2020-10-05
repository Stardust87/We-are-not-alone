from livewires import games, color
import pygame
import random, math
from flags import FLAGS


class Ball(games.Sprite):
    """ alien missiles """

    FLAG = FLAGS["F_BALL"]

    #two types of missiles
    image1 = games.load_image("textures\\missile.png",
                            transparent = True)
    image2 = games.load_image("textures\\big_missile.png",
                            transparent = True)
    #missile parameters
    LIFE_TIME = int(games.screen.fps*10) 
    VELOCITY = 2
    BUFFER = 20
    SMALL = 1
    LARGE = 2
    DAMAGE = 10

    
    def __init__(self, rocket_x, rocket_y, rocket_angle):
        #random size of missile
        if random.randrange(10) < 3:
            self.size = Ball.LARGE
            self.value = -Ball.LARGE*Ball.DAMAGE
        else:
            self.size = Ball.SMALL
            self.value = -Ball.SMALL*Ball.DAMAGE
        
        # angle in radians
        angle = rocket_angle * math.pi / 180
        
        # initial position
        buffer_x = Ball.BUFFER * math.sin(angle)
        buffer_y = Ball.BUFFER * -math.cos(angle)
        x = rocket_x + buffer_x
        y = rocket_y + buffer_y
        
        # speed components
        dx = Ball.VELOCITY * math.sin(angle)
        dy = Ball.VELOCITY * -math.cos(angle)

        super(Ball, self).__init__(image = Ball.image1,
                                    x = x, y = y,
                                    angle = rocket_angle,
                                    dx = dx, dy = dy)
        if self.size == Ball.LARGE:
            self.image = Ball.image2
        self.lifetime = Ball.LIFE_TIME

    def update(self):
        """ executed once per frame """
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()

    def collide(self):
        """ missile destruction """
        self.destroy()