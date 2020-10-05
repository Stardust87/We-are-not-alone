from livewires import games, color
import pygame
import os, random, math
from game import Game
from flags import FLAGS
import config

#screen position
x = 300
y = 80
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)


if __name__ == "__main__": 
    # game beggining
    game = Game()
    config.games1.screen.mainloop()