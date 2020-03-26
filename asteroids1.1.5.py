#kaleb Beck
#4-30-19
#aseroids 1.o

#imports
import games
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


class Ship(games.Sprite):
    image = games.load_image("images/X-wing_removebg.png")
    sound = games.load_sound("Sounds/X-wing Engine.wav")
    # Millennium Falcon
   # image = games.load_image("images/MillenniumFalcon2.1.png")
    #sound = games.load_sound("Sounds/MillenniumFalcon_Thrust.wav")
    ROTATION_STEP = 3
    VELOCITY_STEP = .03




    def __init__(self):
        super(Ship,self).__init__(image = Ship.image,
                                  x = games.screen.width/2 ,
                                  y = games.screen.height/2)

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
    
                              
        #Wrapper
        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

        if self.top > games.screen.height:
            self.bottom = 0
            
        if self.bottom < 0:
            self.top = games.screen.height
        
        
        



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
    player = Ship()


    #draw objects
    games.screen.background = bg_img
    games.screen.add(new_asteroid)
    games.screen.add(player)


    #game setup



    #start main loop
    games.screen.mainloop()
    
main()
