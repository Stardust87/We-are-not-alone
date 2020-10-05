from livewires import games, color
import pygame

class Explosion(games.Animation):
    """ animated explosion """
    
    #seria obrazków animacji
    anim_frames = ['textures\\explosion1.png',
                   'textures\\explosion2.png',
                   'textures\\explosion3.png',
                   'textures\\explosion4.png',
                   'textures\\explosion5.png']

    def __init__(self, x, y):
        super(Explosion, self).__init__(images = Explosion.anim_frames,
            x = x,
            y = y,
            n_repeats = 1, #number of animation repeating
            repeat_interval = 6,  #how many frames needed to change image
            is_collideable = False)