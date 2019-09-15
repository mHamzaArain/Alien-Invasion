class GameStats():
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # Start game in an inactive state.
        self.game_active = False    # when game starts or no ship left
        
        # High score should never be reset and track high score among all played levels.
        self.high_score = 0
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit  
        self.score = 0 # this track the score 
        self.level = 1  # this track the level 