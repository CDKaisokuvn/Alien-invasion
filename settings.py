class Settings:
    """A class to store all settings for the game.
    """

    def __init__(self):
        """Initialize the game's settings
        """
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 2
        self.ship_limit = 3

        # Bullet settings
        self.bullet_color = (60, 60, 60)
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_speed = 2.0
    
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        ## fleet direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1
