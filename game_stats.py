class GameStats:
    """Track statistics for Alien Invasion."""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.game_active = False
        self.reset_stats()
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.best_score = self._get_best_score()

    def _get_best_score(self):
        with open('score.txt', 'r') as file:
            best_score = file.read()
            return best_score
        