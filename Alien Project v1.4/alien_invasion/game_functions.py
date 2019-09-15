import sys # to quit game
from time import sleep # to pause game for moment

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        print('Right')
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
        print('Left')
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
        
def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Mouse click event on button
            check_play_button(ai_settings, screen, stats, sb, play_button,
                ship, aliens, bullets, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
        aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings when game ended or starts for first time
        ai_settings.initialize_dynamic_settings()
        
        # Hide the mouse cursor. set_visible(False) -> pygame hide cursor when curdor is on windows
        pygame.mouse.set_visible(False)
        
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        # Reset the scoreboard images.
        sb.prep_score()         # display current score
        sb.prep_high_score()    # Display high score
        sb.prep_level()         # Diplay current level 
        sb.prep_ships()         # Display no.of ships left
        
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.blit(ai_settings.bg_color, (0,0))
    
    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()   # Draw ship on its current location
    aliens.draw(screen) # <element>.draw(<where to draw>) on Group() -> pygame draw each element in group at the position defined.
    
    # Draw the score information(i.e; current score, high score, level)
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, # collided bullet & alien removed
        aliens, bullets)
        
def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score: # if current score > high score 
        stats.high_score = stats.score # current score = high score
        sb.prep_high_score()           # display high score
            
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets):
    """Respond to bullet-alien collisions."""
    # sprite.groupcollide -> look up collision of 2 gropups
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions: # if collision event occur
        for aliens in collisions.values():                          # those alins collided with bullets(i.e; each alien hit by single bullet)
            stats.score += ai_settings.alien_points * len(aliens)   #  hitted alian * current score = exact score
            sb.prep_score()                                         # To display updated score
        check_high_score(stats, sb)                         # Check current score has achieved high score
    
    if len(aliens) == 0: # if no alien in current level 
        # If the entire fleet is destroyed, start a new level.
        bullets.empty() # destroy all bullets
        ai_settings.increase_speed() # increse speed of (ship, bullet, alien)
        
        # Increase level.
        stats.level += 1 # increase level by 1
        sb.prep_level()  # To display level incremented level
        
        create_fleet(ai_settings, screen, ship, aliens) # create fleet
    
def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites(): # looping through each alien
        if alien.check_edges(): # if true alien is at edge of screen then pass it change_fleet_direction.
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites(): # looping through each alien
        alien.rect.y += ai_settings.fleet_drop_speed # drop down each alien by fleet_drop_speed.
    ai_settings.fleet_direction *= -1 # then change direction by  multiplying it by -1 -> To make if fleet dropping from L then move R or vice versa.
    
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        
        # Update scoreboard.
        sb.prep_ships()       # Diaply how many ships left
        
    else:
        stats.game_active = False  # To make game over if no ship left
        pygame.mouse.set_visible(True) # make cursor reappear when games end
    
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    
    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    
    # Pause after hitting the ship.
    sleep(0.5)
    
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
        bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom: # if alien reached bottom
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break
            
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
      then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens) # Check alien is at edge of screen, if yes then move whole fleet down with change in direction 
    aliens.update() # update position of alien
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens): # Check alien & ship had collided 
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)     # remain ship decremented, if no ship left game over

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
            
def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width # available space for x 
    number_aliens_x = int(available_space_x / (2 * alien_width)) # no of column, int() not to make partial column 
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -            # available space for y
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))   # no. of row, int() not to make partial row
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width # make rectangular obj 
    alien.x = alien_width + 2 * alien_width * alien_number # formula for alien in row.
    alien.rect.x = alien.x  # image to place in row from left to right.
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number # image to place in row from top to bottom. 
    aliens.add(alien) # add alien in right most the prevoius alien

def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)