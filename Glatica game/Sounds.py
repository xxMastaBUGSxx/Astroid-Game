from superwires import games

games.init(screen_width = 640, screen_height = 480, fps = 50)
missile_sound = games.load_sound("sounds/LaserEffect.wav")
games.music.load("sounds/Theme.wav")

chice = None
while choice!="0":

    print(
        """
    Sound and Music

    0 - Quit
    1 - Play Laser sound
    2 - Loop Laser sound
    3 - Stop Laser sound
    4 - Play theme music
    5 - Loop theme music
    6 - Stop theme music
    """
        )
    choice = input("Choice:")
    print()
    #exit
    if choice == "0":
        print("Good-bye.")

        #play Laser sound
    elif choice == "1":
        missile_sound.play()
        print("Playing Laser sound")
        #loop Laser sound
    elif choice == "2":
        loop = int(inplut("Loop how many extra times?(-1 = forever):"))
        missile_sound.play(loop)
        print("Looping missile sound.")
        #play theme music
    elif choice == 3:
        missile_sound.stop()
        print("Stopping Laser music.")

    elif choice ==4:
        
    
    

    
