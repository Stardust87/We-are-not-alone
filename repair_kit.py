from livewires import games, color
import pygame
import  random
from flags import FLAGS


class RepairKit(games.Sprite):
    """ repair kit for the player """

    FLAG = FLAGS["F_KIT"]

    image = games.load_image("textures\\kit.png",
                            transparent = False)

    #kit parameters
    LIFE_TIME = games.screen.fps*8
    VALUE = 30

    def __init__(self):
        #random initial position
        x = random.randint(20, games.screen.width - 20)
        y = random.randint(20, games.screen.height - 20)
        super(RepairKit, self).__init__(image = self.image,
                                       x = x,
                                       y = y)
        self.lifetime = RepairKit.LIFE_TIME
        self.value = RepairKit.VALUE

    def update(self):
        """ executed once per frame """

        if self.lifetime > 0:
            self.lifetime -= 1
        else:
            self.destroy()

    def collide(self):
        """ repair kit destruction """
        self.destroy()