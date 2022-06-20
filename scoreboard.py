import pygame


class ScoreBoard():
    """A class to report scoring information."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_best_score()

    def prep_best_score(self):
        """Turn best score into rendered image"""
        best_score = self.stats.best_score
        best_score_str = str(best_score)
        self.best_score_image = self.font.render(
            best_score_str, True, self.text_color, self.settings.bg_color)
        self.best_score_image_rect = self.best_score_image.get_rect()

        # Display best score at the top left
        self.best_score_image_rect.top = 20
        self.best_score_image_rect.left = self.screen_rect.left + 10

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 20

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.best_score_image, self.best_score_image_rect)
