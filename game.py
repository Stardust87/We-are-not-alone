from livewires import games, color
import pygame
from director import Director
from rocket import Rocket

class Game:
    """ class containing game elements """
    
    background_image = games.load_image("textures\\background.png",
                                        transparent = False) 

    def __init__(self):
        games.screen.background = Game.background_image
        self.loaded = 0
        self.direct = Director(self)
        games.screen.add(self.direct)
        

    def show_menu(self):
        """ restarting game """
        games.screen.clear()
        games.screen.add(self.direct)
        self.direct.state = Director.MENU
        #instructions displayed on splash screen
        message1 = games.Text(value = "Move with arrows.", 
                             size = 80,
                             color = color.white,
                             x = games.screen.width/2,
                             y = games.screen.height/4,
                             is_collideable = False)
        games.screen.add(message1)

        message2 = games.Text(value = "Shoot with space.",
                             size = 80,
                             color = color.white,
                             x = games.screen.width/2,
                             y = games.screen.height*1/2,
                             is_collideable = False)
        games.screen.add(message2)

        message3 = games.Text(value = "Press enter to start.",
                             size = 80,
                             color = color.white,
                             x = games.screen.width/2,
                             y = games.screen.height*3/4,
                             is_collideable = False)
        games.screen.add(message3)
        self.loaded = 1

    def play(self):
        """ creating new game and adding new player """
        games.screen.clear()
        games.screen.add(self.direct)
        self.loaded = 1

        player = Rocket(self)
        games.screen.add(player)