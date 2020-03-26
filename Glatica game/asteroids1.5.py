#kaleb Beck
#4-30-19
#aseroids 1.o

#imports
from superwires import games,color
import random
import math




#Global info
games.init(screen_width =640, screen_height = 480, fps = 60)








#classes

class Game(object):
    """The game itself."""
    def __init__(self):
        #set level
        self.level = 0
        # load sound for level advance
        self.sound = games.load_sound("sounds/new_level.wav")
        #create score
        self.score = games.Text(value = 0,
                   size = 30,
                   color = color.white,
                   top = 5,
                   right = games.screen.width -10,
                   is_collideable = False)
        games.screen.add(self.score)
        # create player's ship
        self.player = Ship(game = self,
                           x = games.screen.width/2,
                           y = games.screen.height/2)
        games.screen.add(self.player)
    def play(self):
        games.music.load("sounds/Theme.wav")
        games.music.play(-1)

        bg_img = games.load_image("images/MIlky way.jpg")
        games.screen.background = bg_img

        self.advance()

        games.screen.mainloop()

    def advance(self):
        """Advance to the next game level."""
        self.level += 1
        # amount of space arund ship to preserve when creating asteroids
        BUFFER = 150

         #create new asteroids 
        for i in range(self.level):
        #calculate an x and y at least BUFFER distance from the ship
        #choose minimum distance along x-axis and y-axis
            x_min = random.randrange(BUFFER)
            y_min = BUFFER - x_min

        # chooses distance along x-axis and y-axis vased on minimum distance 
            x_distance = random.randrange(x_min, games.screen.width - x_min)
            y_distance = random.randrange(x_min, games.screen.width - y_min)
            #choose distance along x-axis and y-axis based on minimum distance
            x = self.player.x + x_distance
            y = self.player.y + y_distance
            #wrap around screen, if necessary
            x%= games.screen.width
            y%=games.screen.height
            
            new_asteroid = Asteroid(game = self,x = x, y = y, size = Asteroid.LARGE)
            games.screen.add(new_asteroid)
        
        #display level number
        level_message = games.Message(value = "Level"  + str(self.level),
                                      size=40,
                                      color = color.yellow,
                                      x = games.screen.width/2,
                                      y = games.screen.width/10,
                                      lifetime = 3 * games.screen.fps,
                                      is_collideable = False)
        games.screen.add(level_message)

        # play new level sound(except at first level)
        if self.level > 1:
            self.sound.play()
            

    def end(self):
        """ End the game."""
        #show 'Game Oveer' for 5 seconds
        end_message = games.Message(value = "Game Over",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 5 * games.screen.fps,
                                    after_death = games.screen.quit,
                                    is_collideable = False)
        games.screen.add(end_message)
        


        



class Wrapper(games.Sprite):
    


    def update(self):
        """ Wrap sprite around screen. """    
        if self.top > games.screen.height:
            self.bottom = 0

        if self.bottom < 0:
            self.top = games.screen.height

        if self.left > games.screen.width:
            self.right = 0

        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        self.destroy()

class Collider(Wrapper):
    
    def update(self):
        """ Check for overlapping sprites."""
        super(Collider,self).update()

        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()

    def die(self):
        #create explotion
        new_explosion = Explosion(obj_x = self.x, obj_y = self.y)
        games.screen.add(new_explosion)
        #add to screen
        self.destroy()

    

class Asteroid(Wrapper):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    images = {SMALL:games.load_image("images/asteroid_small.bmp"),
              MEDIUM:games.load_image("images/asteroid_med.bmp") ,
              LARGE:games.load_image("images/asteroid_big.bmp")}
    SPEED = 2
    SPAWN = 2
    POINTS = 30
    total = 0

    def __init__(self,game,x,y,size):
        Asteroid.total += 1
        super(Asteroid, self).__init__(image = Asteroid.images[size],
                                       x = x,
                                       y = y,
                                       dx = random.choice([1,-1]) * Asteroid.SPEED * random.random()/size,
                                       dy = random.choice([1,-1]) * Asteroid.SPEED * random.random()/size)
        self.size = size
        self.game = game

                                    
        #wrapping/batch file
 
            
    def die(self):
        # if asteroid isn't small, replace with two smaller asteroids
        Asteroid.total -=1
        #add score
        self.game.score.value += int(Asteroid.POINTS/self.size)
        self.game.score.right = games.screen.width - 10

        
        if self.size != Asteroid.SMALL:
            for i in range(Asteroid.SPAWN):
                new_asteroid = Asteroid(game = self.game,
                                        x = self.x,
                                        y = self.y,
                                        size = self.size - 1)
                games.screen.add(new_asteroid)
        self.destroy()
        
        if Asteroid.total == 0:
            self.game.advance()
        super(Asteroid,self).die()



class Ship(Collider):
    image = games.load_image("images/Spaceship_A-removebg.png")
    sound = games.load_sound("Sounds/X-wing Engine2.wav")
    # Millennium Falcon
    #image = games.load_image("images/MilenniumFalcon2.2.png")
    #sound = games.load_sound("Sounds/MillenniumFalcon_Thrust.wav")
    ROTATION_STEP = 4
    VELOCITY_STEP = .03
    MISSILE_DELAY = 15
    VELOCITY_MAX = 3




    def __init__(self,game,x,y):
        super(Ship,self).__init__(image = Ship.image,x = x,y = y)
        self.game = game
        self.missile_wait = 0
   
        
    def update(self):
        super(Ship,self).update()
        if games.keyboard.is_pressed(games.K_LEFT) or games.keyboard.is_pressed(games.K_a):
            self.angle -= Ship.ROTATION_STEP
                              
        if games.keyboard.is_pressed(games.K_RIGHT) or games.keyboard.is_pressed(games.K_d):
            self.angle += Ship.ROTATION_STEP
                              
        if games.keyboard.is_pressed(games.K_UP) or games.keyboard.is_pressed(games.K_w):
            Ship.sound.play()
            angle = self.angle * math.pi/180
            self.dx += Ship.VELOCITY_STEP * math.sin(angle)
            self.dy += Ship.VELOCITY_STEP * -math.cos(angle)
            self.dx = min(max(self.dx,-Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
            self.dy = min(max(self.dy,-Ship.VELOCITY_MAX), Ship.VELOCITY_MAX)
        if self.missile_wait >0:
            self.missile_wait-=1
            
    
        if games.keyboard.is_pressed(games.K_SPACE)and self.missile_wait == 0:
            new_missile = Missile(self.x, self.y, self.angle)
            games.screen.add(new_missile)
            self.missile_wait = Ship.MISSILE_DELAY
            
      

    
    def die(self):
        """Destroy ship and end the game."""
        self.game.end()
        super(Ship,self).die()
        
    

    

class Missile (Collider):
    image = games.load_image("images/X-wing_Laser.png")
    sound = games.load_sound("sounds/Rebel Laser Turbo1.wav")
    BUFFER = 100
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
        self.angle = ship_angle

        
        
    def update(self):
        super(Missile,self).update()
        # if lifetime is up, destroy the missile 
        self.lifetime-=1
        if self.lifetime ==0:
            self.destroy()




       
            
    

class Explosion(games.Animation):
    sound = games.load_sound("sounds/Explosion Large 2.wav")
    exp_images = [ "images/Explosion1.png" ,
                        "images/Explosion2.png" ,
                        "images/Explosion3.png" ,
                        "images/Explosion4.png" , 
                        "images/Explosion5.png"]

    def __init__(self,obj_x,obj_y):
        super(Explosion,self).__init__(images= Explosion.exp_images,
                                    x = obj_x, y =obj_y,
                                    repeat_interval = 4,
                                    n_repeats = 1,
                                    is_collideable = False)
        Explosion.sound.play()
    


#main
def main():
    astrocrash = Game()
    astrocrash.play()
                                    
                                
main()
