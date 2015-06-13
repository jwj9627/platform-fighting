import pygame
from spritesheet_functions import SpriteSheet

GREEN = (0,255,0)

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
    def __init__(self, sprite_sheet_data):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("resources/sprites/tiles_spritesheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()
#     def __init__(self, width, height):
#         pygame.sprite.Sprite.__init__(self)
#         
#         self.image = pygame.Surface([width, height])
#         self.image.fill(GREEN)
#         
#         self.rect = self.image.get_rect()
        
class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0
    
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
    enemy = None
 
    level = None
 
    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """
 
        # Move left/right
        self.rect.x += self.change_x
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0 and (self.rect.top < self.player.rect.bottom and 
                                      self.player.rect.bottom < self.rect.top + 34):
                #self.player.change_y = self.change_y
                self.player.rect.bottom = self.rect.top
        
        hit = pygame.sprite.collide_rect(self, self.enemy)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0 and (self.rect.top < self.enemy.rect.bottom and 
                                      self.enemy.rect.bottom < self.rect.top + 34):
                #self.player.change_y = self.change_y
                self.enemy.rect.bottom = self.rect.top
        
        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
            
class Boundary(Platform):
    """ platform that prevent the player from passing"""
    
    player = None
    enemy = None
    level = None
     
    
    def update(self):
        """ Set the platform to invisible and check for collision with the 
            player"""
        self.image.set_alpha(0)
        
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # If we are moving right, set our right side
            # to the left side of the item we hit
            
            # Allow wall climbing
            if self.player.change_x > 0:
                self.player.rect.right = self.rect.right #left
            elif self.player.change_x < 0:
                self.player.rect.left = self.rect.left # right
        
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.enemy)
        if hit:
            # If we are moving right, set our right side
            # to the left side of the item we hit
            
            # Allow wall climbing
            if self.enemy.change_x > 0:
                self.enemy.rect.right = self.rect.right #left
            elif self.enemy.change_x < 0:
                self.enemy.rect.left = self.rect.left # right
                
        