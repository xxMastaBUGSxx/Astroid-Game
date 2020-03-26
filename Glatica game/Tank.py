# Tank 2-Player Battle Game

import sys, time, random, math, pygame
from pygame.locals import *
#from My_Library.py import *

class Bullet():
    def __init__(self, position):
        self.alive = True
        self.color = (250, 20, 20)
        self.position = Point(position.x, position.y)
        self.velocity = Point(0, 0)
        self.rect = Rect(0, 0, 4, 4)
        self.owner = ""

    def update(self, ticks):
        self.position.x -= self.velocity.x * 10.0
        self.position.y -= self.velocity.y * 10.0
        if self.position.x < 0 or self.position.x > 800 \
           or self.position.y < 0 or self.position.y > 600:
            self.alive = False
        self.rect = Rect(self.position.x, self.position.y, 4, 4)

    def draw(self, surface):
        pos = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(surface, self.color, pos, 4, 0)

def fire_cannon(tank):
    position = Point(tank.turret.X, tank.turret.Y)
    bullet = Bullet(position)
    angle = tank.turret.rotation + 90
    bullet.velocity = angular_velocity(angle)
    bullets.append(bullet)
    play_sound(shoot_sound)
    return bullet

def player_fire_cannon():
    bullet = fire_cannon(player)
    bullet.owner = "player"
    bullet.color = (30, 250, 30)

def player2_fire_cannon():
    bullet = fire_cannon(player2)
    bullet.owner = "player2"
    bullet.color = (250, 30, 30)

class Tank(MySprite):
    def __init__(self, tank_file, turret_file):
        MySprite.__init__(self)
        self.load(tank_file, 50, 60, 4)
        self.speed = 0.0
        self.scratch = None
        self.float_pos = Point(0, 0)
        self.velocity = Point(0, 0)
        self.turret = MySprite()
        self.turret = MySprite()
        self.turret.load(turret_file, 32, 64, 4)
        self.fire_timer = 0

    def update(self,ticks):
        # update chassis
        MySprite.update(self, ticks, 100)
        self.rotation = wrap_angle(self.rotation)
        self.scratch = pygame.transform.rotate(self.image, -self.rotation)
        angle = wrap_angle(self.rotation-90)
        self.velocity = angular_velocity(angle)
        self.float_pos.x += self.velocity.x * 2
        self.float_pos.y += self.velocity.y * 2

        # warp tank around screen edges (keep it simple)
        if self.float_pos.x < -50: self.float_pos.x = 800
        elif self.float_pos.x > 800: self.float_pos.x = -50
        if self.float_pos.y < -60: self.float_pos.y = 600
        elif self.float_pos.y > 600: self.float_pos.y = -60

        # transfer float position to integer position for drawing
        self.X = int(self.float_pos.x)
        self.Y = int(self.float_pos.y)

        # update turret
        self.turret.position = (self.X, self.Y)
        self.turret.last_frame = 0
        self.turret.update(ticks, 100)
        self.turret.rotation = wrap_angle(self.turret.rotation)
        angle = wrap_angle(self.turret.rotation)
        self.turret.scratch = pygame.transform.rotate(self.turret.image, -angle)

    def draw(self, surface):
        # draw the chassis
        width, height = self.scratch.get_size()
        center = Point(width/2, height/2)
        surface.blit(self.scratch, (self.X-center.x, self.Y-center.y))        
        # draw the turret
        width, height = self.turret.scratch.get_size()
        center = Point(width/2, height/2)
        surface.blit(self.turret.scratch, (self.turret.X-center.x,
                                           self.turret.Y-center.y))

    def __str__(self):
        return MySprite.__str__(self) + "," + str(self.velocity)

# this function initializes the game
def game_init():
    global screen, backbuffer, font, timer, player_group, player, \
           player2, bullets

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    backbuffer = pygame.Surface((800, 600))
    pygame.display.set_caption("Tank Battle Game")
    font = pygame.font.Font(None, 30)
    timer = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    # create player tank
    player = Tank("tank.png", "turret.png")
    player.float_pos = Point(400, 300)

    # create second player tank
    player2 = Tank("enemy_tank.png", "enemy_turret.png")
    player2.float_pos = Point(random.randint(50, 760), 50)

    # create bullets
    bullets = list()

# this function initializes the audio system
def audio_init():
    global shoot_sound, boom_sound

    # initialize the audio mixer
    pygame.mixer.init()

    # load sound files
    shoot_sound = pygame.mixer.Sound("shoot.wav")
    boom_sound = pygame.mixer.Sound("boom.wav")

# this function uses any available channel to play a sound clip
def play_sound(sound):
    channel = pygame.mixer.find_channel(True)
    channel.set_volume(0.5)
    channel.play(sound)

# main program begins
game_init()
audio_init()
game_over = False
player_score = 0
player2_score = 0
last_time = 0
action1 = False
action2 = False
action3 = False
action4 = False
action5 = False
action6 = False

# main loop
while True:
    timer.tick(30)
    ticks = pygame.time.get_ticks()

    # event section
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                action1 = True
            if event.key == pygame.K_RIGHT:
                action2 = True
            if event.key == pygame.K_a:
                action3 = True
            if event.key == pygame.K_d:
                action4 = True
            if event.key == pygame.K_UP:
                action5 = True
            if event.key == pygame.K_w:
                action6 = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                action1 = False
            if event.key == pygame.K_RIGHT:
                action2 = False
            if event.key == pygame.K_a:
                action3 = False
            if event.key == pygame.K_d:
                action4 = False
            if event.key == pygame.K_UP:
                action5 = False
            if event.key == pygame.K_w:
                action6 = False

    if action1 == True:
        player.rotation -= 4.0
        player.turret.rotation -= 4.0
    if action2 == True:
        player.rotation += 4.0
        player.turret.rotation += 4.0
    if action3 == True:
        player2.rotation -= 4.0
        player2.turret.rotation -= 4.0
    if action4 == True:
        player2.rotation += 4.0
        player2.turret.rotation += 4.0
    if action5 == True:
        if ticks > player.fire_timer + 1000:
            player.fire_timer = ticks
            player_fire_cannon()
    if action6 == True:
        if ticks > player2.fire_timer + 1000:
            player2.fire_timer = ticks
            player2_fire_cannon()


    # update section
    if not game_over:
        # move tank
        player.update(ticks)

        # update player two
        player2.update(ticks)

        # update bullets
        for bullet in bullets:
                bullet.update(ticks)
                if bullet.owner == "player":
                    if pygame.sprite.collide_rect(bullet, player2):
                        player_score += 1
                        bullet.alive = False
                        play_sound(boom_sound)
                elif bullet.owner == "player2":
                    if pygame.sprite.collide_rect(bullet, player):
                        player2_score += 1
                        bullet.alive = False
                        play_sound(boom_sound)

    # drawing section
    backbuffer.fill((100, 100, 20))

    for bullet in bullets:
        bullet.draw(backbuffer)

    player.draw(backbuffer)

    player2.draw(backbuffer)

    screen.blit(backbuffer, (0, 0))

    if not game_over:
        print_text(font, 0, 0, "PLAYER 1: " + str(player_score))
        print_text(font, 650, 0, "PLAYER 2: " + str(player2_score))
    else:
        print_text(font, 0, 0, "GAME OVER")

    pygame.display.update()

    # remove expired bullets
    for bullet in bullets:
        if bullet.alive == False:
            bullets.remove(bullet)
