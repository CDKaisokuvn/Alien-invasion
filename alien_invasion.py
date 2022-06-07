import sys

import pygame
from settings import Settings
from ship import Ship


class AlienInvasion():
    """Overall class to manage game assets and behavior.
    """

    def __init__(self):
        """Initialize the game, and create game resource."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)

    def run_game(self):
        """Start the main loop for the game.
        """

        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            # Update the ship's states
            self.ship.update()
            # Show on the screen
            self._update_screen()

    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                self._check_key_down(event)

            elif event.type == pygame.KEYUP:
                self._check_key_up(event)

    def _check_key_down(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_ESCAPE:
            sys.exit(0)

    def _check_key_up(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self):
        """Update images on the screen. and flip to the new screen."""
        # Set the background color
        self.screen.fill(self.settings.bg_color)
        # Drawn ship image.
        self.ship.blitme()
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
