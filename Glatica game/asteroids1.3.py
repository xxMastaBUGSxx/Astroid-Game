#kaleb Beck
#4-30-19
#aseroids 1.o

#imports
from superwires import games
import random
import math



#Global info
games.init(screen_width =640, screen_height = 480, fps = 60)








#classes

class Asteroid(games.Sprite):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL:games.load_image("images/asteroid_small.bmp"),
              MEDIUM:games.load_image("images/asteroid_med.bmp") ,
              LARGE:games.load_image("images/asteroid_big.bmp")}
    SPEED = 2
    SPAWN = 2

    def __init__(self,x,y,size):
        super(Asteroid, self).__init__(image = Asteroid.images[size],
                                       x = x,
                                       y = y,
                                       dx = random.choice([1,-1]) * Asteroid.SPEED * random.random()/size,
                                       dy = random.choice([1,-1]) * Asteroid.SPEED * random.random()/size)
        self.size = size
        #wrapping/batch file
    def update(self):
        if self.right < 0:
            self.left = games.screen.width
            
            
        if self.left < 0:
            self.rght = games.screen.width
            
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height
            
    def die(self):
        # if asteroid isn't small, replace with two smaller asteroids
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(x = self.x,y = self.y,size = self.size - 1)
                games.screen.add(new_asteroid)
        self.destroy() 



class Ship(games.Sprite):
    image = games.load_image("images/X-wing_removebg.png")
    sound = games.load_sound("Sounds/X-wing Engine2.wav")
    # Millennium Falcon
   # image = games.load_image("images/MillenniumFalcon2.1.png")
    #sound = games.load_sound("Sounds/MillenniumFalcon_Thrust.wav")
    ROTATION_STEP = 7
    VELOCITY_STEP = .03
    MISSILE_DELAY = 25




    def __init__(self):
        super(Ship,self).__init__(image = Ship.image,
                        x = games.screen.width/2 ,
                        y = games.screen.height/2)
        self.missile_wait = 0
    def die(self):
        self.destroy()
        
    def update(self):
        if games.keyboard.is_pressed(games.K_LEFT) or games.keyboard.is_pressed(games.K_a):
            self.angle -= Ship.ROTATION_STEP
                              
        if games.keyboard.is_pressed(games.K_RIGHT) or games.keyboard.is_pressed(games.K_d):
            self.angle += Ship.ROTATION_STEP
                              
        if games.keyboard.is_pressed(games.K_UP) or games.keyboard.is_pressed(games.K_w):
            Ship.sound.play()
            angle = self.angle * math.pi/180
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)
            self.dx += Ship.VELOCITY_STEP * -math.cos(angle)
        if self.missile_wait >0:
            self.missile_wait-=1
            
    
        if games.keyboard.is_pressed(games.K_SPACE)and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    
        
        #Wrapper
        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height

    

class Missile (games.Sprite):
    image = games.load_image("images/X-wing_Laser.png")
    sound = games.load_sound("sounds/Rebel Laser Turbo1.wav")
    BUFFER = 40
    VELOCITY_FACTOR = 7
    LIFETIME = 40
        
        
    def __init__(self,ship_x,ship_y,ship_angle):
        Missile.sound.play()
        angle = ship_angle * math.pi/180




        # calculate missile's starting position
        buffer_x = Missile.BUFFER * math.sin(angle)
        buffer_y = Missile.BUFFER * -math.cos(angle)

        x = ship_x + buffer_x
        y = ship_y + buffer_y

        dx = Missile.VELOCITY_FACTOR * math.sin(angle)
        dy = Missile.VELOCITY_FACTOR * -math.cos(angle)
        super(Missile,self).__init__(image = Missile.image,x = x,y = y, dx = dx, dy = dy)
        self.lifetime = Missile.LIFETIME

        
        
    def update(self):
        if self.right < 0:
            self.left = games.screen.width
            
            
        if self.left < 0:
            self.rght = games.screen.width
            
        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height
        # if lifetime is up, destroy the missile 
        self.lifetime-=1
        if self.lifetime ==0:
            self.destroy()




       
            
    def die(self):
        self.destroy()




#main
def main():

    #load data
    bg_img = games.load_image("images/MIlky way.jpg")


    #create objects
    for i in range(8):
        x =random.randrange(games.screen.width)
        y = random.randrange(games.screen.height)
        size = random.choice([Asteroid.SMALL, Asteroid.MEDIUM, Asteroid.LARGE])
        new_asteroid = Asteroid(x = x, y = y, size = size)
        games.screen.add(new_asteroid)
    

    #create ship
    player = Ship()
    shot = Missile(100,100,0)


    #draw objects
    games.screen.background = bg_img
    games.screen.add(new_asteroid)
    games.screen.add(player)
    games.screen.add(shot)


    #game setup



    #start main loop
    games.screen.mainloop()
    
main()
