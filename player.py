"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame
import time
import constants
from constants import BLACK

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []

    # What direction is the player facing?
    direction = "R"

    # List of sprites we can bump against
    level = None

    # -- Methods
    def __init__(self, health):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("img/p1_walk.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        self.health = health
        self.attack = Bluefireball

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
    def update_health(self, screen, color):
        pygame.draw.rect(screen, color, (self.rect.x - 15, self.rect.y - 20, self.health, 5), 4)


class Enemy(Player):
    def __init__(self, health):
        super().__init__(health)
        self.capturable = False
        self.captured = False

class Combee(Enemy):

    def __init__(self, health, direction):
        super().__init__(health)
        self.image_list = []
        for i in range(5):
            self.image_list.append(pygame.transform.scale(pygame.image.load("img/combee_badguy" + str(i) + ".png"), (300, 200)).convert_alpha())
            self.image_list.append(pygame.transform.scale(pygame.image.load("img/combee_badguy" + str(i) + ".png"), (300, 200)).convert_alpha())
            self.image_list.append(pygame.transform.scale(pygame.image.load("img/combee_badguy" + str(i) + ".png"), (300, 200)).convert_alpha())
            self.image_list.append(pygame.transform.scale(pygame.image.load("img/combee_badguy" + str(i) + ".png"), (300, 200)).convert_alpha())
            self.image_list.append(pygame.transform.scale(pygame.image.load("img/combee_badguy" + str(i) + ".png"), (300, 200)).convert_alpha())


        self.direction = direction
        self.index = 0
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500
    def update(self):
        self.index += 1
        if self.index >= len(self.image_list):
            self.index = 0
        if self.direction == 1:
            self.image = self.image_list[self.index]
        else:
            self.image = pygame.transform.flip(self.image_list[self.index],True ,False)
    def update_health(self, screen, color):
        if not self.captured:
            pygame.draw.rect(screen, color, (self.rect.x + 20, self.rect.y - 20, self.health/4, 5), 4)



class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, direction):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([10, 4])
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
        self.direction = direction
 
    def update(self):
        """ Move the bullet. """
        self.rect.x += 20 * self.direction



class Fireball(Bullet):
    def __init__(self, direction):
        super().__init__(direction)
        self.image_list = []
        for i in range(5):
            self.image_list.append(pygame.image.load("img/fireball" + str(i) + ".png").convert_alpha())


        self.index = 0

        self.image = self.image_list[0]
        # load all component images of fireball into image_list
    def update(self):
        super().update()
        self.index += 1
        if self.index >= len(self.image_list):
            self.index = 0
        if self.direction == 1:
            self.image = self.image_list[self.index]
        else:
            self.image = pygame.transform.flip(self.image_list[self.index],True ,False)
        # keep a counter variable 
        # change self.image to be the ith image 
        # normal movement stuff  
class Bluefireball(Fireball):
    def __init__(self, direction):
        super().__init__(direction)
        self.image_list = []
        for i in range(5):
            self.image_list.append(pygame.transform.scale(pygame.image.load("img/bluefireball" + str(i) + ".png"), (50, 50)).convert_alpha())

class Pokeball(Fireball):
    def __init__(self, direction):
        super().__init__(direction)
        self.image_list = []
        for i in range(4):
            self.image_list.append(pygame.transform.scale(pygame.image.load("img/pokeball" + str(i) + ".png"), (100, 100)).convert_alpha())
    def update(self):
        self.rect.x += 10 * self.direction
        self.index += 1
        if self.index >= len(self.image_list):
            self.index = 0
        if self.direction == 1:
            self.image = self.image_list[self.index]
        else:
            self.image = pygame.transform.flip(self.image_list[self.index],True ,False)

class power_up(pygame.sprite.Sprite):
    def __init__(self, version, location):
        super().__init__()
        self.image = pygame.image.load("img/blue_fireball_power_up.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.x = location[0]
        self.y = location[1]
        self.rect = self.image.get_rect()
        self.type = version


