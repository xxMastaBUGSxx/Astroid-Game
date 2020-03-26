#Infinity Endgame
#Created by Kaleb Beck
#4/19










#imports
from superwires import games, color 
import random





# global variables
games.init(screen_width = 640, screen_height = 480, fps = 60)







#classes
class Chef(games.Sprite):
    image = games.load_image("images/Chef1.png")

    def __init__(self, y = 60, speed = 5, odds_change = 100):
        super (Chef,self).__init__(image = Chef.image,
                                   x = games.screen.width /2,
                                   y = y,
                                   dx = speed)
        self.odds_change = odds_change
        self.time_till_drop = 0
        

    def update(self):
        self.x = games.Chef.x
## makes Chef randomly change direction 
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx
            
        

    
    def check_drop(self):
        if self.time_till_drop > 0:
            self.time_till_drop -=1
        else:
            new_pizza = Pizza(x = self.x)
            games.screen.add(new_pizza)
        self.time_till_drop = random.randint(20,250)
        
    


class Pan(games.Sprite):
    image = games.load_image("images/Pan.png")
    
    def __init__(self):
        super(Pan,self).__init__(image = Pan.image,
                                 x = games.mouse.x,
                                 bottom = games.screen.height)

    def update(self):

        self.x = games.mouse.x

        if self.left < 0:
            self.left = 0
        if self.right > games.screen.width:
            self.right = games.screen.width
            
        self.check_catch()   
                

    def check_catch(self):
        for pizza in self.overlapping_sprites:
           # add to score()
           pizza.handle_caught()
        pass
    


class Pizza(games.Sprite):
    image = games.load_image("images/Pizza.png")
    speed = 10
    
    ##random pizza speed 
    def __init__(self,x,y=90, speed = random.randrange(speed)+1):
        super(Pizza,self).__init__(image = Pizza.image,x=x,y=y, dy = speed)
        pass
    def update(self):
        if self.top >games.screen.height:
            self.destroy()
            self.end_game()
        pass

    def end_game(self):
        """ End the game."""
        end_message = games.Message(value = "Game Over",
                                    size = 90,
                                    color = color.blue,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 5 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)
                                    
    def handle_caught(self):
        pass
    
class ScText(games.Text):
    pass












#main
def main():
    

# load Data
    wall_image = games.load_image("images/Halo game background.png", transparent = False)

# create objects
    the_pan = Pan()
    the_chef = Chef()
    the_pizza = Pizza(x = 250)


# draw
    games.screen.background = wall_image
    Games.screen.add(the_pan)
    Games.screeen.add(the_chef)
    Games.screen.add(the_pizza)


                                  

# game setup
    games.mouse.is_visivle = False
    games.screen.event_grab = False


#start loop
    games.screen.mainloop()




#starting point







