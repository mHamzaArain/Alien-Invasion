import pygame.font # to write on game screen

class Button():

    def __init__(self, ai_settings, screen, msg):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50   # width, height
        self.button_color = (0, 255, 0)     # button color
        self.text_color = (255, 255, 255)   # text color on button 
        self.font = pygame.font.SysFont(None, 48) # None -> defalut font style & fontSize -> 48 pixel
        
        # Build the button's rect object, and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height) # button's rect initialized at top-left of screen
        self.rect.center = self.screen_rect.center  # To set button on the centre of the screen
        
        # The button message only needs to be prepped once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image, and center text on the button."""
        # font.render() -> turns text into image.
        # True/False -> anti-aliasing -> makes edges smoother if it is True.
        # text_color -> Color of text
        # button_color -> bg of button 
        self.msg_image = self.font.render(msg, True, self.text_color, 
            self.button_color)

        # To make text  on bottom center on button widget.    
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        # Draw blank button, then draw message.
        self.screen.fill(self.button_color, self.rect)         # [].fill([], []) to draw rectangular portion of button
        self.screen.blit(self.msg_image, self.msg_image_rect)  # [].blit([], []) to draw text on button image 