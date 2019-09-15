import pygame
from pygame.sprite import Sprite
import os

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien, and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # To find exact image of alien.
        # os.walk -> deeply browse each path, file & folder
        # os.getcd -> current working diecttory
        finalPath = ''
        for path, folder, file in os.walk(os.getcwd()):
            # Considering each path whose ends with img(i.e; img folder)
            if path.endswith('img'):
                # join path e.g;  "C:\Users\Hamza Arain\Desktop\Alien Project v1.3\Ch12_Firing_fromShip\img" + "/"  + "ship.bmp"  
                finalPath = os.path.join(path, 'alien.bmp')
                break

        # Load the alien image, and set its rect attribute as rect make retangular object. 
        self.image = pygame.image.load(finalPath)
        self.rect = self.image.get_rect() 

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width   # image width
        self.rect.y = self.rect.height  # image height

        # Store the alien's exact position.
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right: # right side of screen
            return True
        elif self.rect.left <= 0: # left side of screen
            return True
        
    def update(self):
        """Move the alien right or left."""
        self.x += (self.ai_settings.alien_speed_factor *  # self.c -> track exact  position and then move it to the left side
                        self.ai_settings.fleet_direction) # fleet_direction -> change direction by changing sign +/-, -ve -> L side & +ve -> R side.
        self.rect.x = self.x

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)