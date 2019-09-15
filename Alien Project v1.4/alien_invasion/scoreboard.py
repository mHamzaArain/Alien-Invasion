import pygame.font                  # font
from pygame.sprite import Group     # work with group(i.e; ships, aliens, bullets)s

from ship import Ship

class Scoreboard():
    """A class to report scoring information."""

    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        # Font settings for scoring information.
        self.text_color = 56, 232, 12               # text color
        self.font = pygame.font.SysFont(None, 48)   # deafult font, fontSize = 48

        # Prepare the initial score images.
        self.prep_score()                   # to turn text to display image on screen
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        # This tells to round the nearest values of 10, 100, 1000, etc
        # round([], []) -. round decimal to set number of decimal place
        # -1 arg -> roound the nearest values (i.e; 10, 100, 1000, etc)
        # int() _> make decimal point less
        rounded_score = int(round(self.stats.score, -1))    # make score an int value
        
        # format does 1000000 into 1,000,000 & convert into string
        score_str = "{:,}".format(rounded_score)            # convert it into string
        
        # font_render -> convert font into image
        # score_str -> Convert string into image 
        # True -> anti-alising(clear edges of text)
        # text_color -> text color 
        # bg_color -> background to show string image 
        self.score_image = self.font.render(score_str, True, self.text_color,
            self.ai_settings.bg_color)
            
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()       # score image rectangular obj
        self.score_rect.right = self.screen_rect.right - 20 # from right to 30 pixel left place (current)score
        self.score_rect.top = 20                            # from top down to place (current)score 
        
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        # This tells to round the nearest values of 10, 100, 1000, etc
        # round([], []) -. round decimal to set number of decimal place
        # -1 arg -> roound the nearest values (i.e; 10, 100, 1000, etc)
        # int() _> make decimal point less
        high_score = int(round(self.stats.high_score, -1))
        
        # format does 1000000 into 1,000,000 & convert into string 
        high_score_str = "{:,}".format(high_score)

        # font_render -> convert font into image
        # score_str -> Convert string into image 
        # True -> anti-alising(clear edges of text)
        # text_color -> text color 
        # bg_color -> background to show string image
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.ai_settings.bg_color)
                
        # Center the high score at the top-middle of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx     # place in middle of x axis
        self.high_score_rect.top = self.score_rect.top              # place in top 
        
    def prep_level(self):
        """Turn the level into a rendered image."""
        # font_render -> convert font into image
        # str(stats.level) -> Convert string into image 
        # True -> anti-alising(clear edges of text)
        # text_color -> text color 
        # bg_color -> background to show string image 
        self.level_image = self.font.render(str(self.stats.level), True,
                self.text_color, self.ai_settings.bg_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right       # To place level on right side
        self.level_rect.top = self.score_rect.bottom + 10   # 10 pixel beneath the the bottom of score 
        
    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()    # make ships as list as group
        for ship_number in range(self.stats.ships_left):     # no. of ships left -> game_stats.py -> settings.py
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width # show image with margin of 10 pixel left-side of image
            ship.rect.y = 10                                 # 10 pixxel down from top of screen
            self.ships.add(ship)                             # adding each ships
        
    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)             # display score 
        self.screen.blit(self.high_score_image, self.high_score_rect)   # display high score
        self.screen.blit(self.level_image, self.level_rect)             # display current level
        # Draw ships.
        self.ships.draw(self.screen)                                    # Show all ships remaining