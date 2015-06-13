import pygame
import platform
from platform import Platform
from platform import MovingPlatform
from platform import Boundary
from wall import Wall
from wall import Ground

BLUE = (0, 0, 255)

class Level():
    """ Level class add new levels to the game here"""
    
    # List of sprites used in all levels. Add or remove lists as 
    platform_list = None
    enemy_list = None
    projectile_list = []
    # Background Image
    background = None
    
    # How far this world has been scrolled left/right
    world_shift = 0
    
    def __init__(self, player, player2):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.enemy = player2 # Player 2
        #self.enemy_list.add(player2)
        
    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
        
    def draw(self, screen):
        screen.fill((255,0,0))
        screen.blit(self.background,((self.world_shift // 3) - 200,0))
        
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
    
    def shift_world(self, shift_x, camera):
        # Keep track of the shift amount
        self.world_shift += shift_x
        
        # Go through all the sprites list and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
        
        self.enemy.rect.x += shift_x
        if camera is not None: self.player.rect.x += shift_x

        
        #for enemy in self.enemy_list:
            #enemy.rect.x += shift_x
        
        for laser in self.projectile_list:
            laser.rect.x += shift_x
            laser.starting_x += shift_x


# Create platforms for the level
class Level_01(Level):
    # s_h = screen_height
    # s_w = screen_width    
    def __init__(self, player, enemy):
        Level.__init__(self, player, enemy)
        
        self.background = pygame.image.load("resources/backgrounds/bg_castle.png").convert()
        self.background.set_colorkey((255,255,255))
                
        # Ground
        level = []       
        
        # Top left platform
        for i in range(0, 10):
            level.append([STONE_PLATFORM_MIDDLE, 0 + 70 * i, 168])
            level.append([STONE_PLATFORM_MIDDLE, 2100 - 70 * i, 168])
            
            
        # Left and right wall
        for i in range(1, 11):
            level.append([STONE_WALL, -70, 698 - 70 * i])
            level.append([STONE_WALL, 2100, 698 - 70 * i])
            
        # create middle platforms
        for i in range(1, 6):
            level.append([STONE_PLATFORM_MIDDLE, 840 + 70 * i, 330])
        
        # Created the Ground
        for i in range(0, 30):
            level.append([STONE_PLATFORM_MIDDLE, 70 * i, 768 - 70])
        
        # Climbable on the left and right side
        left_wall = Wall(0, 168, 1, 463, player, enemy)
        self.platform_list.add(left_wall)
        right_wall = Wall(2099, 168, 1, 463, player, enemy)
        self.platform_list.add(right_wall)
        
        # Middle Stone Platform
        for i in range(0, 5):
            for j in range(0, 4):
                level.append([STONE_WALL, 910 + 70 * i, 370 + 40 * j])
        
        # walls and grounds for the Middle Stone    
        middle_left_wall = Wall(909, 328, 1, 234, player, enemy)
        self.platform_list.add(middle_left_wall)
        
        middle_right_wall = Wall(1261, 328, 1, 234, player, enemy)
        self.platform_list.add(middle_right_wall)
        
        middle_top_ground = Ground(910, 328, 351, 1, player, enemy)
        self.platform_list.add(middle_top_ground)
        
        middle_bottom_ground = Ground(910, 561, 351, 1, player, enemy)
        self.platform_list.add(middle_bottom_ground)
        
        # go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            block.enemy = self.enemy
            self.platform_list.add(block)
                  
        #Add left boundary
        for i in range(0, 10):
            left_boundary = Boundary(STONE_PLATFORM_MIDDLE)
            left_boundary.rect.x = -70
            left_boundary.rect.y = 80 - 40 * i
            left_boundary.player = self.player
            left_boundary.enemy = self.enemy
            left_boundary.level = self
            self.platform_list.add(left_boundary)
        
        # Add right Boundary
        for i in range(0, 10):
            right_boundary = Boundary(STONE_PLATFORM_MIDDLE)
            right_boundary.rect.x = 2100
            right_boundary.rect.y = 80 - 40 * i
            right_boundary.player = self.player
            right_boundary.enemy = self.enemy
            right_boundary.level = self
            self.platform_list.add(right_boundary)
            
 
# Create platforms for the level
class Level_02(Level):
 
    def __init__(self, player, enemy):
        Level.__init__(self, player, enemy)
        
        self.background = pygame.image.load("resources/backgrounds/bg_shroom.png").convert()
        self.background.set_colorkey((255,255,255))
                
        # Ground
        level = [
                 
                 [GRASS_LEFT, 0, 768 - 70],
                 [GRASS_RIGHT, 2100 - 70, 768 - 70],
                 
                 [STONE_PLATFORM_LEFT, 400, 165], # Left Top Platform
                 [STONE_PLATFORM_MIDDLE, 470, 165],
                 [STONE_PLATFORM_MIDDLE, 540, 165],
                 [STONE_PLATFORM_RIGHT, 610, 165],
                 
                 [STONE_PLATFORM_LEFT, 0, 350], # Left middle Platform
                 [STONE_PLATFORM_MIDDLE, 70, 350],
                 [STONE_PLATFORM_MIDDLE, 140, 350],
                 [STONE_PLATFORM_MIDDLE, 210, 350],
                 [STONE_PLATFORM_RIGHT , 280, 350],
                 
                 [STONE_PLATFORM_LEFT, 500, 520], # Left bottom Platform
                 [STONE_PLATFORM_RIGHT, 570, 520],
                 
                 [STONE_PLATFORM_LEFT, 1420, 165], # Right Top Platform
                 [STONE_PLATFORM_MIDDLE,1490, 165],
                 [STONE_PLATFORM_MIDDLE, 1560, 165],
                 [STONE_PLATFORM_RIGHT, 1630, 165],

                 [STONE_PLATFORM_LEFT, 1750, 350], # Left middle Platform
                 [STONE_PLATFORM_MIDDLE, 1820, 350],
                 [STONE_PLATFORM_MIDDLE, 1890, 350],
                 [STONE_PLATFORM_MIDDLE, 1960, 350],
                 [STONE_PLATFORM_RIGHT , 2030, 350],    
                 
                 [STONE_PLATFORM_LEFT, 1600, 520], # Left bottom Platform
                 [STONE_PLATFORM_RIGHT, 1670, 520],
                ]
        
        # Level ground
        for i in range(1, 29):
            level.append([GRASS_MIDDLE, 70 * i, 768 - 70])
            
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            block.enemy = self.enemy
            self.platform_list.add(block)
        
        # Add a custom moving left platform
        block = MovingPlatform(STONE_PLATFORM_LEFT)
        block.rect.x = 900
        block.rect.y = 530
        block.boundary_top = 100
        block.boundary_bottom = 600
        block.change_y = 5
        block.player = self.player
        block.enemy = self.enemy
        block.level = self
        self.platform_list.add(block)  

            
        block = MovingPlatform(STONE_PLATFORM_RIGHT)
        block.rect.x = 970
        block.rect.y = 530
        block.boundary_top = 100
        block.boundary_bottom = 600
        block.change_y = 5
        block.player = self.player
        block.enemy = self.enemy
        block.level = self
        self.platform_list.add(block) 
        
        # Add a custom moving  platform       
        block = MovingPlatform(STONE_PLATFORM_LEFT)
        block.rect.x = 1111
        block.rect.y = 100
        block.boundary_top = 100
        block.boundary_bottom = 600
        block.change_y = 5
        block.player = self.player
        block.enemy = self.enemy
        block.level = self
        self.platform_list.add(block)  
        
        block = MovingPlatform(STONE_PLATFORM_RIGHT)
        block.rect.x = 1180
        block.rect.y = 100
        block.boundary_top = 100
        block.boundary_bottom = 600
        block.change_y = 5
        block.player = self.player
        block.enemy = self.enemy
        block.level = self
        self.platform_list.add(block) 
         
        #Add left boundary
        for i in range(0, 20):
            left_boundary = Boundary(STONE_PLATFORM_MIDDLE)
            left_boundary.rect.x = -70
            left_boundary.rect.y = 0 + 40 * i
            left_boundary.player = self.player
            left_boundary.enemy = self.enemy
            left_boundary.level = self
            self.platform_list.add(left_boundary)
        
        # Add right Boundary
        for i in range(0, 20):
            right_boundary = Boundary(STONE_PLATFORM_MIDDLE)
            right_boundary.rect.x = 2100
            right_boundary.rect.y = 0 + 40 * i
            right_boundary.player = self.player
            right_boundary.enemy = self.enemy
            right_boundary.level = self
            self.platform_list.add(right_boundary)
        
# These constants define our platform types:
#   Name of file
#   X location of sprite    
#   Y location of sprite
#   Width of sprite
#   Height of sprite

GRASS_LEFT            = (576, 720, 70, 70)
GRASS_RIGHT           = (576, 576, 70, 70)
GRASS_MIDDLE          = (504, 576, 70, 70)
STONE_PLATFORM_LEFT   = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT  = (792, 648, 70, 40)
STONE_WALL            = (504, 288, 70, 70)
WATER                 = (504, 216, 70, 70)
        