import os           # to fspecify the path of image file to set on background 
import pygame

class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width =  1360
        self.screen_height = 768
        # self.bg_color = (230, 230, 230)

        finalPath = ''
        for path, folder, file in os.walk(os.getcwd()):
            # Considering each path whose ends with img(i.e; img folder)
            if path.endswith('img'):
                # join path e.g;  "C:\Users\Hamza Arain\Desktop\Alien Project v1.3\Ch12_Firing_fromShip\img"    +   "ship.bmp(i.e; image file)"  
                finalPath = os.path.join(path, 'starfield.bmp')
                break
        bg_color = pygame.image.load(finalPath)
        self.bg_color = pygame.transform.scale(bg_color, (self.screen_width, self.screen_height))

        # Ship settings.
        self.ship_limit = 3
            
        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 192, 3
        self.bullets_allowed = 3
        
        # Alien settings.
        self.fleet_drop_speed = 10
            
        # speed_scae->increase n of times e.g; if 2, it will increase 2 times as previous speed of prevoius level when next level is up.
        self.speedup_scale = 1.5
        # How quickly the alien point values increase.
        self.score_scale = 1.5
    
        self.initialize_dynamic_settings() # init. only in biginning of game to set speed of (ship, alien, bullet) & direction of right side 

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5 # ship movement speed
        self.bullet_speed_factor = 3 # bullet movement speed
        self.alien_speed_factor = 1 # alien movement speed
        
        # Scoring for each alien down.
        self.alien_points = 50
    
        # fleet_direction of 1 represents right, -1 represents left.
        # 1 or -1 has sense as for right -> adding in x coordinate, left -> minus in c coordinate 
        self.fleet_direction = 1 # firstly move right 
        
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        # speed up movement of(ship, bullet, alien) by xing it with speedup_scale(e.g; 2)
        self.ship_speed_factor *= self.speedup_scale    # e.g; ship_speed_factor = 1 * 2 = 2 
        self.bullet_speed_factor *= self.speedup_scale  # e.g; bullet_speed_factor = 1 * 2 = 2
        self.alien_speed_factor *= self.speedup_scale   # e.g; alien_speed_factor = 1 * 2 = 2
        
        self.alien_points = int(self.alien_points * self.score_scale)