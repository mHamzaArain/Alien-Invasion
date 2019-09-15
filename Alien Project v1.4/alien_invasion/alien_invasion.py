#######################################Importing Modules

#######Importing Main modules for game.
# pygame = for making game.
# from pygame.sprite import Group = like list(i.e; no.of bullets, aliens, fleet)
#     with funtions when we have to work with group.
import pygame   
from pygame.sprite import Group       

#######Importing other classes (self made)
from settings import Settings       # background, speed, basic control 
from game_stats import GameStats    # track the stats of game
from scoreboard import Scoreboard   # responsible to show on game display
from button import Button           # Button to play game
from ship import Ship               # Ship attributes 
import game_functions as gf         # Additional functionalities

def run_game():
    '''This function consist of two parts:
        1. Initializing ship, (Group = alien fleet , bullets), background,
            scoreboard, stats & settings (possess basic contol)
        2. Updating simultamuously locatiion of ship, alien fleet, bullets,
            events & events.
    '''
    #Part 1:  Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()

    # Game display on full screen & Display on text as title 
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)     # Full screen
    # screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")    # title
    
    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")
    
    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)                  # this init. score, # of shios, level
    sb = Scoreboard(ai_settings, screen, stats)     # instance to draw score related on screen
    
    # Make a ship, a group of bullets and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group() # empty group to hold aliens in game.
    
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # Part 2: Updating simultamuously locatiion of ship, alien fleet, bullets, events & events.

    # Start the main loop for the game.
    while True:
        # Checck keyboard/mouse events.
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
            aliens, bullets)
        
        # becomes false when no ship left to invade
        if stats.game_active: 
            # update ship logically but not screen.
            ship.update()   # update ship logically

            # update bullets logically but not screen.
            gf.update_bullets(ai_settings, screen, stats, # update bullets
             sb, ship, aliens, bullets)

            # update alien fleet logically but not screen. 
            gf.update_aliens(ai_settings, screen, stats, # update alien position
             sb, ship, aliens, bullets)
                
        # update ship, bullets, alien fleet, score on screen. 
        gf.update_screen(ai_settings, screen, stats,
         sb, ship, aliens, bullets, play_button)
            
run_game()