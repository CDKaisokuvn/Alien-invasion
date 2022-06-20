import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion():
    """Overall class to manage game assets and behavior.
    """

    def __init__(self):
        """Initialize the game, and create game resource."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.btn = Button(self, 'Play')
        self.score_board = ScoreBoard(self)
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game.
        """

        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            if self.stats.game_active:

                # Update the ship's states

                self.ship.update()
                # Update the bullets
                self._update_bullet()

                self._update_aliens()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        "If click on button play, turn game_active into True"
        btn_cllicked = self.btn.rect.collidepoint(mouse_pos)

        if btn_cllicked and not self.stats.game_active:
            self._reset_game_state()

    def _update_best_score(self, score):
        """Save the best score to score.txt"""
        if int(score) > int(self.stats.best_score):
            with open('score.txt', 'w') as file:
                file.write(str(score))

    def _reset_game_state(self):
        self.stats.reset_stats()
        self.score_board.prep_score()
        self.score_board.prep_best_score()
        self.settings.initialize_dynamic_settings()
        self.stats.game_active = True
        pygame.mouse.set_visible(False)
        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()

    def _check_key_down(self, event):
        """Respond to keypress."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_ESCAPE:
            sys.exit(0)
        if event.key == pygame.K_p and not self.stats.game_active:
            self._reset_game_state()

    def _check_key_up(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        '''Update the positions of all aliens in the fleet.'''
        self._check_fleet_edges()
        self.aliens.update()

    def _update_bullet(self):
        """Update the bullets's position"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
            self.score_board.prep_score()
        self._game_over()
        self._level_up()

    def _level_up(self):
        """Create a new fleet and make the game more difficult.
        """
        if not self.aliens:
            self.bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()

    def _collision(self):
        """Collision between ship and aliens"""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        """Change game statistics."""
        # Decrement ship_left
        self.stats.ship_left -= 1

        # Get rid of any remaining aliens and bullet:
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()
        sleep(0.5)

    def _check_aliens_bottom(self):
        """Check wether or not aliens at bottom."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()

    def _game_over(self):
        """Game over"""
        self._check_aliens_bottom()
        self._collision()

        if self.stats.ship_left < 0:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            self._update_best_score(self.stats.score)

    def _update_screen(self):
        """Update images on the screen. and flip to the new screen."""
        # Set the background color
        self.screen.fill(self.settings.bg_color)
        # Drawn ship image.
        self.ship.blitme()
        # Draw bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Draw aliens
        self.aliens.draw(self.screen)
        # Draw the play button
        if not self.stats.game_active:
            self.btn.draw_button()
        # Draw the score board
        self.score_board.show_score()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)

        self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create a fleet of aliens for the game."""
        # Make an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height

        available_space_y = self.settings.screen_height - \
            (3 * alien_height) - ship_height
        number_rows = available_space_y // (2*alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create a alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x

        y = alien_height + 2 * alien_height * row_number
        alien.rect.y = y

        self.aliens.add(alien)


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
