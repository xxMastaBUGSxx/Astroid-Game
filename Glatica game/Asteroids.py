#kaleb beck
#4-24-19
#Astroids

#Read Keys
#Demonstrates


from superwires import games

games.init(screen_width = 640, screen_height = 480, fps= 50)


class Ship(games.Sprite):
    ship_image = games.load_image("images\MillenniumFalcon2.1.png")
    


    def __init__(self):
        super(Ship,self).__init__(image = Ship.ship_image,
                                  x = games.screen.width/2,
                                  y = games.screen.height/2)

    def update(self):
        if games.keyboard.is_pressed(games.K_w) or games.keyboard.is_pressed(games.K_UP):
            self.y-=32

        if games.keyboard.is_pressed(games.K_s) or games.keyboard.is_pressed(games.K_DOWN):
            self.y+=32


        if games.keyboard.is_pressed(games.K_a) or games.keyboard.is_pressed(games.K_LEFT):
            self.angle-=32

        if games.keyboard.is_pressed(games.K_d) or games.keyboard.is_pressed(games.K_RIGHT):
            self.angle+=32
            if games.keyboard.is_pressed(games.K_1):
                self.angle=0
            if games.keyboard.is_pressed(games.K_2):
                self.angle=90
            if games.keyboard.is_pressed(games.K_3):
                self.angle=180
            if games.keyboard.is_pressed(games.K_4):
                self.angle=360

            
                

            
                                  


def main():

    #load Data
    nebula_image = games.load_image("images\MIlky way.jpg " , transparent = False)
    explosion_files = [ "images/Explosion1.png" ,
                        "images/Explosion2.png" ,
                        "images/Explosion3.png" ,
                        "images/Explosion4.png" , 
                        "images/Explosion5.png"]

    #missile_sound = games.load_sound("sounds/LaserEffect.wav")
   # games.music.load("sounds/Theme.wav)
    
                        

                                  
                                  

    #create objects
    the_ship = Ship()
    explosion = games.Animation(images = explosion_files,
                                x = games.screen.width/2,
                                y = games.screen.height/2,
                                n_repeats=0,
                                repeat_interval = 10)
                                    

    #draw
    games.screen.background = nebula_image
    games.screen.add(the_ship)
    games.screen.add(explosion)
    #games setup


    

    #start loop
    games.screen.mainloop()
main()
