"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Main module for platform scroller example.

From:
http://programarcadegames.com/python_examples/sprite_sheets/

Explanation video: http://youtu.be/czBDKWJqOao

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/

Game art from Kenney.nl:
http://opengameart.org/content/platformer-art-deluxe

"""

import pygame

import constants
import levels

from player import Player, Combee
from player import Bullet, Fireball, power_up, Bluefireball, Pokeball

def main():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Platformer with sprite sheets")

    # Create the player
    player = Player(100)
    blue_powerup = power_up("blue_fire", (900, 700))
    combee = Combee(1000, 1)
    # Create all the levels
    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))
    # List of each bullet

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    combee_sprite_list = pygame.sprite.Group()
    player_sprite_list = pygame.sprite.Group()
    blue_powerup_sprite_list = pygame.sprite.Group()
    player_projectile_sprite_list = pygame.sprite.Group()
    pokeball_sprite_list = pygame.sprite.Group()

    player.level = current_level
    combee.level = current_level
    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    blue_powerup.rect.x = 900
    blue_powerup.rect.y = 700
    combee.rect.x = 500
    combee.rect.y = 500
    combee_sprite_list.add(combee)
    player_sprite_list.add(player)
    blue_powerup_sprite_list.add(blue_powerup)


    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE:
                    print("good throw")
                    if player.direction == "L":
                        pokeball = Pokeball(-1)
                    else:
                        pokeball = Pokeball(1)
                    # Set the bullet so it is where the player is
                    pokeball.rect.x = player.rect.x
                    pokeball.rect.y = player.rect.y

                    pokeball_sprite_list.add(pokeball)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Fire a bullet if the user clicks the mouse button
                if player.direction == "L":
                    projectile = player.attack(-1)
                else:
                    projectile = player.attack(1)
                # Set the bullet so it is where the player is
                if player.attack == Fireball or player.attack == Bluefireball:
                    projectile.rect.x = player.rect.x
                    projectile.rect.y = player.rect.y

                # Add the bullet to the lists
                player_projectile_sprite_list.add(projectile)
                
        if player.health < 0:
            player.health = 0  
        if combee.health < 0:
            combee.health = 0
            combee.capturable = True             
        # Update the player.
        combee_sprite_list.update()
        player_sprite_list.update()
        blue_powerup_sprite_list.update()
        player_projectile_sprite_list.update()
        pokeball_sprite_list.update()       

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        # if player.rect.x >= 500:
        #     diff = player.rect.x - 500
        #     player.rect.x = 500
        #     current_level.shift_world(-diff)

        # # If the player gets near the left side, shift the world right (+x)
        # if player.rect.x <= 120:
        #     diff = 120 - player.rect.x
        #     player.rect.x = 120
        #     current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        combee_sprite_list.draw(screen)
        player_sprite_list.draw(screen)
        # blue_powerup_sprite_list.draw(screen)
        player_projectile_sprite_list.draw(screen)
        pokeball_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        if player.health >= 66:
            player.update_health(screen,(0, 255, 0))
        elif player.health >= 33:
            player.update_health(screen,(255, 255, 0))
        else:
            player.update_health(screen,(255, 0, 0))

        if combee.health >= 666:
            combee.update_health(screen,(0, 255, 0))
        elif combee.health >= 333:
            combee.update_health(screen,(255, 255, 0))
        else:
            combee.update_health(screen,(255, 0, 0))

        if pygame.sprite.groupcollide(combee_sprite_list, player_projectile_sprite_list, False, True):
            combee.health -= 100
        if combee.capturable:
            if pygame.sprite.groupcollide(combee_sprite_list, pokeball_sprite_list, True, True):
                combee.captured = True
        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
