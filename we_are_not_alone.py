from livewires import games, color
import pygame
import os, random, math
from director import Director

#pozycja otwieranego okna gry
x = 300
y = 80
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

#okienko będzie miało wymiary 1000 x 700 pikseli
games.init(screen_width = 1000, screen_height = 700, fps = 60)
pygame.display.set_caption('WE ARE NOT ALONE')

#flagi, służące do rozróżniania obiektów
F_ROCKET = 1
F_ALIEN = 2
F_KIT = 3
F_LASER = 4
F_BALL = 5


class Game:
    """ klasa zawierająca obiekty gry """
    
    #zdefiniowanie tła
    background_image = games.load_image("tekstury\\tlo.png",
                                        transparent = False)
    
    def __init__(self):
        """ inicjalizacja zmiennych """
        #załadowanie tła
        games.screen.background = Game.background_image
        #zmienna pilnująca czy załadowano odpowiednie Sprite
        self.loaded = 0
        #dodanie dyrektora gry
        self.direct = Director(self)
        games.screen.add(self.direct)
        

    #metoda, która czyści ekran i następnie odpala ekran startowy 
    def show_menu(self):
        """ restart gry """
        #po restarcie gry ekran zostaje wyczysczony ze Sprite'ów
        games.screen.clear()
        #dyrektor też zostaje usunięty, dlatego trzeba go ponownie dodać
        games.screen.add(self.direct)
        #ładowanie menu
        self.direct.state = Director.MENU
        #wyświetlanie instrukcji
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

    #metoda startująca grę
    def play(self):
        """ rozpoczecie gry """
        games.screen.clear()
        games.screen.add(self.direct)
        self.loaded = 1

        #tworzenie gracza i dodanie go na ekran
        player = Rocket(self)
        games.screen.add(player)

class Rocket(games.Sprite):
    """ rakieta sterowana przez gracza """

    FLAG = F_ROCKET

    image = games.load_image("tekstury\\rakieta.png", transparent = True)
    #stałe parametry rakiety
    MAX_HEALTH = 100
    MAX_SPEED = 2
    VELOCITY_STEP = 0.02
    ROTATION_STEP = 2
    BRAKE_STEP = 0.06
    SHOOT_DELAY = int(games.screen.fps*0.3)
    
    def __init__(self, game, x = games.screen.width/2, y = games.screen.height/2):
        """ inicjalizacja rakiety """
        #wywołanie inicjalizatora klasy bazowej (Sprite)
        super(Rocket, self).__init__(image = self.image, x = x, y = y)
        self.health = Rocket.MAX_HEALTH
        self.vx = 0
        self.vy = 0
        self.shoot_timer = 0
        #odnośnik do klasy Game
        self.game = game

        #wyświetlanie poziomu życia gracza na ekranie
        temp = str(self.health) + '%'
        self.display = games.Text(value = temp, 
                             size = 30,
                             color = color.green,
                             left = self.right + 5,
                             top = self.top,
                             is_collideable = False)
        games.screen.add(self.display)

    def update(self):
        """ wykonuje się co klatkę """
        self.control()
        self.move()
        self.shoot()
        self.check_collision()

        #aktualizacja poziomu życia gracza
        self.display.value = str(self.health) + '%'
        self.display.left = self.right + 5
        self.display.top = self.top
        if self.health < Rocket.MAX_HEALTH/2:
            self.display.color = color.red
        else:
            self.display.color = color.green
            

    # metoda poruszająca rakietą
    def move(self):
        """ ruch rakiety """
        self.x += self.vx
        self.y += self.vy
        
        #rakieta wylatująca za ekran pojawia się z drugiej strony ekranu
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height
            
        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width


    def get_position(self):
        """ zwraca pozycje rakiety """
        return (self.x, self.y)

    def get_distance(self, ship):
        """ Odległość od innego obiektu """
        tempx = ship.x - self.x
        tempy = ship.y - self.y
        odl = math.sqrt((tempx)**2 + (tempy)**2)
        return odl
    
    #wpływ klawiszy na ruch rakiety
    def control(self):
        """ sterowanie """

        #obracanie rakiety 
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Rocket.ROTATION_STEP
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Rocket.ROTATION_STEP
            
        #przyśpieszanie    
        if games.keyboard.is_pressed(games.K_UP):
            angle = self.angle * math.pi / 180
            self.vx += Rocket.VELOCITY_STEP * math.sin(angle)
            self.vy += Rocket.VELOCITY_STEP * -math.cos(angle)

        #limity prędkości rakiety
        self.vx = min(max(self.vx, -Rocket.MAX_SPEED), Rocket.MAX_SPEED)
        self.vy = min(max(self.vy, -Rocket.MAX_SPEED), Rocket.MAX_SPEED)
        
        #hamowanie
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
        """ strzelanie laserami """
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
        else:
            #spacja odpala laser
            if games.keyboard.is_pressed(games.K_SPACE):          
                self.shoot_timer = Rocket.SHOOT_DELAY
                las = Laser(self.x, self.y, self.angle)
                games.screen.add(las)

    def change_hp(self, target):
        """ zmiana zdrowia po kolizji """
        self.health += target.value
        #gdy poziom życia gracza jest maksymalny i zbierze on zestaw naprawczy
        #to poziom życia się nie zmienia
        if self.health > Rocket.MAX_HEALTH:
            self.health = Rocket.MAX_HEALTH
        #gdy poziom życia jest mniejszy od zera gra zostaje skończona
        elif self.health <= 0:
            self.health = 0
            self.end_game()

    def end_game(self):
        """ kończenie gry """
        games.screen.clear()
        lose_message = games.Message(value = "You lost!",
                            size = 100,
                            color = color.black,
                            x = games.screen.width/2,
                            y = games.screen.height/2,
                            lifetime = games.screen.fps*4,
                            after_death = self.game.show_menu,
                            is_collideable = False)
        #gdy gracz przegrywa, na ekranie wyświetla się odpowiednia wiadomość
        games.screen.add(lose_message)
        self.collide()
            
    def check_collision(self):
        """ sprawdza i obsługuje kolizje """
        #w zależności od kolidujących obiektów podejmowane są różne akcje
        for target in self.overlapping_sprites:
            if target.FLAG == F_ALIEN or \
               target.FLAG == F_KIT or \
               target.FLAG == F_BALL:
                self.change_hp(target)
                target.collide()
                
    def collide(self):
        """ zniszcz się """
        explo = Explosion(x = self.x,y = self.y)
        games.screen.add(explo)
        self.destroy()      
         
class Alien(games.Sprite):
    """ statek kosmiczny obcych """

    FLAG = F_ALIEN
    #liczba aktualnie istniejących obcych
    count = 0

    #załadowanie grafiki ze statkiem obcych
    image = games.load_image("tekstury\\obcy.png",
                            transparent = True)

    #stałe parametry statku obcych
    MAX_HEALTH = 100
    MAX_SPEED = 1
    SHOOT_DELAY = 4*games.screen.fps
    VALUE = 40

    def __init__(self):
        """ inicjalizacja statku obcych """
        #losowe położenie początkowe statku
        y = random.randint(0, games.screen.height)
        super(Alien, self).__init__(image = self.image, right = 0, y = y)
        self.health = Alien.MAX_HEALTH
        self.shoot_timer = Alien.SHOOT_DELAY
        self.set_move()
        self.value = -Alien.VALUE
        Alien.count += 1

    def update(self):
        """ wykonuje się co klatkę """
        self.move()
        self.shoot()
        self.check_collision()

    def move(self):
        """ poruszanie się """

        #statek obcych wylatujący za ekran pojawia się z drugiej strony ekranu
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height
            
        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width
        
        

    def set_move(self):
        """ wybór trybu poruszania """
        #losowe nadawanie prędkości tworzonym statkom
        temp = random.uniform(Alien.MAX_SPEED*0.3, Alien.MAX_SPEED)
        self.dx = random.choice([-1, 1])*temp
        self.dy = random.choice([-1, 1])*(Alien.MAX_SPEED - abs(self.dx))

    def shoot(self):
        """ strzelanie pociskami """
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
        # gdy zmienna wynosi zero, wtedy strzał jest gotowy
        else:
            self.shoot_timer = Alien.SHOOT_DELAY
            temp = random.randrange(359)
            bal = Ball(self.x, self.y, temp)
            #dodawanie pocisku obcych na ekran
            games.screen.add(bal)

    def change_hp(self, target):
        """ zmiana zdrowia po kolizji """
        self.health += target.value
        #zabezpieczenie przed przekroczeniem limitu zdrowia
        if self.health > Alien.MAX_HEALTH:
            self.health = Alien.MAX_HEALTH
        elif self.health <= 0:
            self.health = 0
            self.collide()

    def check_collision(self):
        """ sprawdza i obsługuje kolizje """
        for target in self.overlapping_sprites:
            #kolizja statku z laserem
            if target.FLAG == F_LASER:
                self.change_hp(target)
                #zniszczenie laseru, czyli sprite'a który nakłada się na obcych
                target.collide()
    
    def collide(self):
        """ zniszcz się """
        #gdy statek zostaje zniszczony następuje eksplozja i
        #liczba statków się zmniejsza 
        Alien.count -= 1
        explo = Explosion(x = self.x,y = self.y)
        games.screen.add(explo)
        self.destroy()
        
class Laser(games.Sprite):
    """ pocisk gracza """

    FLAG = F_LASER

    image = games.load_image("tekstury\\laser_1.png",
                            transparent = True)
    #stałe parametry lasera
    LIFE_TIME = int(games.screen.fps*4) #czas życia lasera
    VELOCITY = 8
    BUFFER = 25
    DAMAGE = 50

    
    def __init__(self, rocket_x, rocket_y, rocket_angle):
        """ inicjalizacja lasera """
        
        # zamiana kąta na radiany
        angle = rocket_angle * math.pi / 180
        
        # obliczanie pozycji startowej
        buffer_x = Laser.BUFFER * math.sin(angle)
        buffer_y = Laser.BUFFER * -math.cos(angle)
        x = rocket_x + buffer_x
        y = rocket_y + buffer_y
        
        # obliczanie predkosci skladowych
        dx = Laser.VELOCITY * math.sin(angle)
        dy = Laser.VELOCITY * -math.cos(angle)

        # tworzenie lasera
        super(Laser, self).__init__(image = self.image,
                                    x = x, y = y,
                                    angle = rocket_angle,
                                    dx = dx, dy = dy)
        
        self.lifetime = Laser.LIFE_TIME
        self.value = -Laser.DAMAGE

    def update(self):
        """ wykonuje się co klatkę """
        #po przekroczeniu czasu życia lasera, zostaje on zniszczony
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()
        

    def collide(self):
        """ zniszcz się """
        self.destroy()
    

class Ball(games.Sprite):
    """ pociski obcych """

    FLAG = F_BALL

    #obcy będą dysponować dwoma typami pocisków
    image1 = games.load_image("tekstury\\pocisk.png",
                            transparent = True)
    image2 = games.load_image("tekstury\\duzy_pocisk.png",
                            transparent = True)
    #stałe parametry lasera
    LIFE_TIME = int(games.screen.fps*10) #czas życia pocisku
    VELOCITY = 2
    BUFFER = 20
    SMALL = 1
    LARGE = 2
    DAMAGE = 10

    
    def __init__(self, rocket_x, rocket_y, rocket_angle):
        """ inicjalizacja pocisku """

        #losowanie wielkości
        if random.randrange(10) < 3:
            self.size = Ball.LARGE
            self.value = -Ball.LARGE*Ball.DAMAGE
        else:
            self.size = Ball.SMALL
            self.value = -Ball.SMALL*Ball.DAMAGE
        
        # zamiana kąta na radiany
        angle = rocket_angle * math.pi / 180
        
        # obliczanie pozycji startowej
        buffer_x = Ball.BUFFER * math.sin(angle)
        buffer_y = Ball.BUFFER * -math.cos(angle)
        x = rocket_x + buffer_x
        y = rocket_y + buffer_y
        
        # obliczanie predkosci skladowych
        dx = Ball.VELOCITY * math.sin(angle)
        dy = Ball.VELOCITY * -math.cos(angle)

        # tworzenie pocisku
        super(Ball, self).__init__(image = Ball.image1,
                                    x = x, y = y,
                                    angle = rocket_angle,
                                    dx = dx, dy = dy)
        if self.size == Ball.LARGE:
            self.image = Ball.image2
        self.lifetime = Ball.LIFE_TIME

    def update(self):
        """ wykonuje się co klatkę """
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()

    def collide(self):
        """ zniszcz się """
        self.destroy()
    

class RepairKit(games.Sprite):
    """ zestaw naprawczy """

    FLAG = F_KIT

    image = games.load_image("tekstury\\apteczka.png",
                            transparent = False)

    # stałe parametry 
    LIFE_TIME = games.screen.fps*8
    VALUE = 30

    def __init__(self):
        """ inicjalizacja zestawu naprawczego """

        #losowa pozycja 
        x = random.randint(20, games.screen.width - 20)
        y = random.randint(20, games.screen.height - 20)
        super(RepairKit, self).__init__(image = self.image,
                                       x = x,
                                       y = y)
        self.lifetime = RepairKit.LIFE_TIME
        self.value = RepairKit.VALUE

    def update(self):
        """ wykonuje się co klatkę """

        #niszczenie zestawu naprawczego
        if self.lifetime > 0:
            self.lifetime -= 1
        else:
            self.destroy()

    def collide(self):
            """ zniszcz się """
            self.destroy()
    
class Explosion(games.Animation):
    """ animowana eksplozja """
    
    #seria obrazków animacji
    anim_frames = ['tekstury\\eksplozja1.png',
                   'tekstury\\eksplozja2.png',
                   'tekstury\\eksplozja3.png',
                   'tekstury\\eksplozja4.png',
                   'tekstury\\eksplozja5.png']

    def __init__(self, x, y):
        """ inicjalizacja eksplozji """

        super(Explosion, self).__init__(images = Explosion.anim_frames,
            x = x,
            y = y,
            n_repeats = 1, #ile razy ma być powtórzona animacja
            repeat_interval = 6, #co ile klatek następuje zmiana obrazka
            is_collideable = False)


class Director(games.Sprite):
    """ tworzy obiekty i kontroluje stan gry """

    image = games.load_image("tekstury\\blank.png")
    
    #stałe parametry
    MENU = 1
    PLAY = 2
    KIT_TIME = games.screen.fps*10
    ALIEN_TIME = games.screen.fps*5
    ENEMIES = 10
    
    def __init__(self, game):
        """ dyrektor jest niewidzialny dla gracza """
        super(Director, self).__init__(image = self.image,
                                       x = -1,
                                       y = -1,
                                       is_collideable = False)
        #uchwyt do klasy Game
        self.game = game 
        self.state = Director.MENU
        self.kit_time = Director.KIT_TIME
        self.alien_time = games.screen.fps
        self.produced_aliens = 0
        self.win = 0

    def switch(self):
        """ zmiana stanu gry """
        # wywołanie funkcji ładujących przy zmianie trybu
        #zmienna loaded zapobiega wywoływaniu funkcji co klatkę
        if self.game.loaded == 0:
            if self.state == Director.MENU:
                self.game.show_menu()
            if self.state == Director.PLAY:
                self.game.play()

    def update(self):
        """ wykonuje się co klatkę """
        self.switch()
        #naciśnięcie enter rozpoczyna grę
        if self.state == Director.MENU:
            if games.keyboard.is_pressed(games.K_RETURN):
                #stan gry na początku
                self.state = Director.PLAY
                Alien.count = 0
                self.game.loaded = 0
                self.win = 0
                self.produced_aliens = 0
        
        if self.state == Director.PLAY:
            #dodanie zestawu naprawczego i statku obcych
            self.add_repair_kit()
            self.add_alien()
            if self.produced_aliens == Director.ENEMIES and self.win == 0:
                #gdy liczba obcych na ekranie wynosi 0, gracz zwycięża
                if Alien.count == 0:
                    self.win = 1
                    games.screen.clear()
                    win_message = games.Message(value = "You won!",
                                            size = 100,
                                            color = color.white,
                                            x = games.screen.width/2,
                                            y = games.screen.height/2,
                                            lifetime = games.screen.fps*4,
                                            after_death = self.game.show_menu,
                                            is_collideable = False)
                    #po wygraniu na ekranie pojawia się odpowiedni komunikat
                    games.screen.add(win_message)
            

    def add_repair_kit(self):
        """ dodawanie zestawu naprawczego """
        if self.kit_time > 0:
            self.kit_time -= 1
        else:
            kit = RepairKit()
            games.screen.add(kit)
            self.kit_time = Director.KIT_TIME

    def add_alien(self):
        """ dodawanie statku kosmitów """
        #jeżeli nie została przekroczona maksymalna liczba obcych
        #wtedy dodaje statek na ekran
        if self.produced_aliens < Director.ENEMIES:
            if self.alien_time > 0:
                self.alien_time -= 1
            else:
                self.produced_aliens += 1
                ufo = Alien()
                games.screen.add(ufo)
                self.alien_time = Director.ALIEN_TIME
        
if __name__ == "__main__":  
    #tworzenie gry
    gra = Game()

    #funkcja rozpoczynająca grę
    games.screen.mainloop()


