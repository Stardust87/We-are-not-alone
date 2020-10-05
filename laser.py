from livewires import games, color
import pygame
import math
from flags import FLAGS

class Laser(games.Sprite):
    """ player's projectile """

    FLAG = FLAGS["F_LASER"]

    image = games.load_image("textures\\laser.png",
                            transparent = True)
    #laser parameters
    LIFE_TIME = int(games.screen.fps*4)
    VELOCITY = 8
    BUFFER = 25
    DAMAGE = 50

    
    def __init__(self, rocket_x, rocket_y, rocket_angle):
        # angle in radians
        angle = rocket_angle * math.pi / 180
        
        # initial position
        buffer_x = Laser.BUFFER * math.sin(angle)
        buffer_y = Laser.BUFFER * -math.cos(angle)
        x = rocket_x + buffer_x
        y = rocket_y + buffer_y
        
        # speed components
        dx = Laser.VELOCITY * math.sin(angle)
        dy = Laser.VELOCITY * -math.cos(angle)

        super(Laser, self).__init__(image = self.image,
                                    x = x, y = y,
                                    angle = rocket_angle,
                                    dx = dx, dy = dy)
        
        self.lifetime = Laser.LIFE_TIME
        self.value = -Laser.DAMAGE

    def update(self):
        """ executed once per frame """
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()
        

    def collide(self):
        """ laser destruction """
        self.destroy()