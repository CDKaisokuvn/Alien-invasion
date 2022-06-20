class Settings:
    """A class to store all settings for the game.
    """

    def __init__(self):
        """Initialize the game's settings
        """
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3

        # Bullet settings
        self.bullet_color = (60, 60, 60)
        self.bullet_height = 15
        self.bullet_width = 3

        # Alien settings
        self.fleet_drop_speed = 10
        # fleet direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1
        self.initialize_dynamic_settings()
        self.speedup_scale = 1.1
        self.score_up = 2
        
    def initialize_dynamic_settings(self):
        self.alien_points = 1
        self.ship_speed = 2
        self.bullet_speed = 1.5
        self.alien_speed = 1.0

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points *= self.score_up
