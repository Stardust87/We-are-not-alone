from livewires import games, color
import pygame
import os, random, math
from alien import Alien
from repair_kit import RepairKit


class Director(games.Sprite):
    """ create objects and control state of the game """

    image = games.load_image("textures\\blank.png")
    
    #parameters
    MENU = 1
    PLAY = 2
    KIT_TIME = games.screen.fps*10
    ALIEN_TIME = games.screen.fps*5
    ENEMIES = 10
    
    def __init__(self, game):
        """ director is invisible for the player """
        super(Director, self).__init__(image = self.image,
                                       x = -1,
                                       y = -1,
                                       is_collideable = False)
        self.game = game 
        self.state = Director.MENU
        self.kit_time = Director.KIT_TIME
        self.alien_time = games.screen.fps
        self.produced_aliens = 0
        self.win = 0

    def switch(self):
        """ game state change """
        if self.game.loaded == 0:
            if self.state == Director.MENU:
                self.game.show_menu()
            if self.state == Director.PLAY:
                self.game.play()

    def update(self):
        """ executed once per frame """
        self.switch()
        if self.state == Director.MENU:
            if games.keyboard.is_pressed(games.K_RETURN):
                #initial game state
                self.state = Director.PLAY
                Alien.count = 0
                self.game.loaded = 0
                self.win = 0
                self.produced_aliens = 0
        
        if self.state == Director.PLAY:
            self.add_repair_kit()
            self.add_alien()
            if self.produced_aliens == Director.ENEMIES and self.win == 0:
                if Alien.count == 0:
                    self.win = 1
                    games.screen.clear()
                    #message displayed after winning
                    win_message = games.Message(value = "You won!",
                                            size = 100,
                                            color = color.white,
                                            x = games.screen.width/2,
                                            y = games.screen.height/2,
                                            lifetime = games.screen.fps*4,
                                            after_death = self.game.show_menu,
                                            is_collideable = False)
                    games.screen.add(win_message)
            

    def add_repair_kit(self):
        """ add repair kit  """
        if self.kit_time > 0:
            self.kit_time -= 1
        else:
            kit = RepairKit()
            games.screen.add(kit)
            self.kit_time = Director.KIT_TIME

    def add_alien(self):
        """ add alien spaceship """
        if self.produced_aliens < Director.ENEMIES:
            if self.alien_time > 0:
                self.alien_time -= 1
            else:
                self.produced_aliens += 1
                ufo = Alien()
                games.screen.add(ufo)
                self.alien_time = Director.ALIEN_TIME