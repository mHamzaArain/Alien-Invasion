import pygame
from pygame.sprite import Sprite
import os

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the ship, and set its starting position."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image, and get its rect.
        # self.image = pygame.image.load(r'C:\Users\Hamza Arain\Desktop\Alien Project v1.3\Ch12_Firing_fromShip\img/ship.bmp')
        myPath = ''
        for path, folder, file in os.walk(os.getcwd()):
            if path.endswith('img'):
                myPath = os.path.join(path, 'ship.bmp')
                break
            
        self.image = pygame.image.load(myPath)    
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)
        
        # Movement flags.
        self.moving_up = False          # up
        self.moving_down = False        # down
        self.moving_right = False       # right
        self.moving_left = False        # left
        
    def center_ship(self):
        """Center the ship on the screen when previously ship destroyed."""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """Update the ship's position, based on movement flags."""
        # Update the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
            
        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)