"""
Global constants
"""
# Color

from platform import Boundary

import pygame
import random
from projectile import Laser
from spritesheet_functions import SpriteSheet
from collections import Counter


BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)


class Enemy(pygame.sprite.Sprite):
    player = None
    
    # -- Attributes
    health = 50
    damage = 8
    movement_speed = 1
    jump_height = -15
    
    on_ground = False;
    distance = 1500

    state = 0
    
    # List of sprites for walking animation
    walking_frames_l = []
    walking_frames_r = []
    jumping_frames_l = []
    jumping_frames_r = []
    
    direction = "R"
    
    counter = 0   
    
    # -- Methods
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH):
        """ Constructor function """
        # Call the parent's constructor
        super().__init__()
                
        self.load_sprite()
        
        self.screen_height = SCREEN_HEIGHT
        self.screen_width = SCREEN_WIDTH

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 64
        height = 80
        self.image = pygame.Surface([width, height])
        self.image = self.walking_frames_r[0]
        #self.image.fill(RED)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
        
    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()
        
            #self.move_toward_player()
        #self.move_toward_player()
        # Move left/right
        self.rect.x += self.change_x
        
        self.patrol()
        #self.player_inrange()
        
        # Update sprite
        self.update_sprite()
            
        # Move left/right
        self.rect.x += self.change_x
        self.horizontal_collision()
 
        # Move up/down
        self.rect.y += self.change_y
        self.vertical_collision()
        
        #Change movement speed when jumping
        self.jumping_speed()
            
        if not self.on_ground: print('Jumping')
    
    def patrol(self):
        if self.distance >= 1000:
            rand = random.randrange(0,2)
        
        if rand == 0:
            self.go_left()
        else:
            self.go_right()
        
        self.distance -= self.movement_speed
        print(self.distance)
        if self.distance < 0:
            self.distance = 1500
        
    def player_inrange(self):
        if (self.rect.x - 350 < self.player.rect.x and 
            self.player.rect.x < self.rect.x + 350):        
            print('player within x range')

        if (self.rect.y - 350 < self.player.rect.y and 
            self.player.rect.y < self.rect.y + 350):        
            print('player within y range')

    def move_toward_player(self):
        if self.player.rect.x + 150 <  self.rect.x:
            self.go_left()
        elif self.player.rect.x + 150 > self.rect.x:
            self.go_right()
            
        if self.player.rect.y < self.rect.y:
            self.jump()
            
    def horizontal_collision(self):
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if isinstance(block, Boundary):           
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
                
    def vertical_collision(self):
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0 and self.inside_platform(block): # and self.inside_platform(block):
                # Reset our position based on the top/bottom of the object.
                self.rect.bottom = block.rect.top
                # Stop our vertical movement
                self.change_y = 0      
                self.on_ground = True;              
            
    def inside_platform(self, block):
        return (block.rect.top < self.rect.bottom and self.rect.bottom < block.rect.top + 35)
        
            
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            if self.change_y > 0:
                self.change_y += 1.75
            else:
                self.change_y += .65
 
        # Resets position if player falls through the ground
        if self.rect.y >= self.screen_height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = self.screen_height - self.rect.height * 2
   
    def jumping_speed(self):
        if self.on_ground: 
            self.movement_speed = 10
            if self.change_x > 0:
                self.go_right()
            elif self.change_x < 0:
                self.go_left()
        else : 
            self.movement_speed = 8
            if self.change_x > 0:
                self.go_right()
            elif self.change_x < 0:
                self.go_left()
        
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        if self.on_ground:
            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.y -= 2
     
            # If it is ok to jump, set our speed upwards
            if len(platform_hit_list) > 0 or self.rect.bottom >= self.screen_height:
                self.change_y = self.jump_height
                self.on_ground = False
           
    def range_attack(self):
        laser = Laser(BLUE_LASER)
        laser.rect.x = self.rect.x 
        laser.starting_x = self.rect.x
        laser.rect.y = self.rect.y
        laser.player = self
        laser.direction = self.direction
        return laser   
             
    def go_left(self):
        self.rect.x += self.movement_speed * -1
        self.direction = "L"
        
    def go_right(self):
        self.rect.x += self.movement_speed
        self.direction = "R"
        
    def stop(self):
        self.change_x = 0  
    
    def update_sprite(self):
        pos = self.rect.x + self.level.world_shift
        if self.on_ground:
            if self.direction == "R":
                frame = (pos // 60) % len(self.walking_frames_r)
                self.image = self.walking_frames_r[frame]
            else:
                frame = (pos // 60) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]
        else:
            if self.direction == "R":
                frame = (pos // 60) % len(self.jumping_frames_r)
                self.image = self.jumping_frames_r[frame]
            else:
                frame = (pos // 60) % len(self.jumping_frames_l)
                self.image = self.jumping_frames_l[frame]

    def load_sprite(self):
        sprite_sheet = SpriteSheet("purple_player_sprite.png")
        image = sprite_sheet.get_image(0, 0, 120, 165)
        image = pygame.transform.scale(image, (64, 88))
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(125, 0, 120, 165)
        image = pygame.transform.scale(image, (64, 88))
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 0, 120, 165)
        image = pygame.transform.scale(image, (64, 88))
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(250, 0, 120, 165)
        image = pygame.transform.scale(image, (64, 88))
        self.walking_frames_r.append(image)
        
        image = sprite_sheet.get_image(0, 0, 120, 165)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (64, 88))
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(125, 0, 120, 165)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (64, 88))
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 0, 120, 165)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (64, 88))
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(250, 0, 120, 165)
        image = pygame.transform.flip(image, True, False)
        image = pygame.transform.scale(image, (64, 88))
        self.walking_frames_l.append(image)
        
        sprite_sheet = SpriteSheet("JumpRight_Smile_Blue.png")
        image = sprite_sheet.get_image(0, 0, 120, 165)
        image = pygame.transform.scale(image, (64, 88))
        self.jumping_frames_r.append(image)
        self.jumping_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.jumping_frames_l.append(image)
        self.jumping_frames_l.append(image)
        
#sprite coordinates
BLUE_LASER = (105, 0, 100, 38)
