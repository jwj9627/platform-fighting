import pygame
from projectile import Laser
from weapon import Weapon
from platform import Boundary
from spritesheet_functions import SpriteSheet
from status_bar import StatusBar
from wall import Ground, Wall

"""
Global constants
"""
# Color
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

class Player(pygame.sprite.Sprite):
    """ Creates the character that the players control
        
        Attributes:
            able_drop: A boolean to determine if the player is on a platform 
                       that they could fall through
    """
    
    #player 2
    enemy = None
    
    # -- Attributes --
    total_health = 750
    current_health = total_health

    total_stamina = 1000
    current_stamina = total_stamina
    
    # -- Attacks Damage --
    melee_damage = 45
    laser_damage = 15
        
    # -- Attacks Cost --
    stamina_penalty = current_stamina / total_stamina
    melee_cost = 70 
    laser_cost = 50
    
    stamina_rate = 10
    movement_speed = 10
    jump_height = -15
    
    # Conditions
    alive = True
    on_ground = False
    able_drop = False
    attacking = False # Might not be needed
    
    direction = "R"
    
    left_screen_boundary = 0
    right_screen_boundary = 2000
    
    # -- Methods --
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN, num):
        """ Constructor function Pass in the height and width of the screen 
            along with the screen that the players will be drawn on. Num is the 
            0 for player 1 or 1 for player 2"""
            
        # Call the parent's constructor
        super().__init__()
        
        self.screen = SCREEN
        self.num = num
        
        # List of sprites for walking animation
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.jumping_frames_l = []
        self.jumping_frames_r = []
        
        # Load the sprite base the player number
        if num == 0:
            self.load_sprite("player_blue_sprite.png")
        if num == 1:
            self.load_sprite("player_purple_sprite.png")
            
        #self.load_sprite()
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
        
        # List of the player's weapons
        self.weapon_sprite = pygame.sprite.Group()

        self.weapon = None
        
        # List of sprites we can bump against
        self.level = None
        
    def update(self):
        """ Updates the player each frame """
        # Gravity
        self.calc_grav()
        
        self.stamina_penalty = self.current_stamina /self.total_stamina
        
        # Move left/right
        self.rect.x += self.change_x
        
        self.status_bar()
        
        # Update Sprite
        self.update_sprite()
        self.weapon_sprite.update()
        self.weapon_sprite.draw(self.screen)

        # Move left/right
        self.rect.x += self.change_x
        self.horizontal_collision()
 
        # Move up/down
        self.rect.y += self.change_y
        self.vertical_collision()
        
        #Change movement speed when jumping
        self.jumping_speed()
              
        # gets changed in main
        if self.attacking: self.melee_attack()
        
        self.restore_stamina()
    
    # -- collision detection -- 
    def horizontal_collision(self):
        # Check if we hit a boundary
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
        
        # Check for collision with player 2
        hit_player = pygame.sprite.collide_rect(self, self.enemy)
        if hit_player:
            if self.change_x > 0:
                self.rect.right = self.enemy.rect.left
            elif self.change_x < 0:
                self.rect.left = self.enemy.rect.right
        
    def vertical_collision(self):
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0 and self.inside_platform(block):
                if isinstance(block, Ground): self.able_drop = False
                else: self.able_drop = True
                
                # Reset our position based on the top/bottom of the object.
                self.rect.bottom = block.rect.top
                # Stop our vertical movement
                self.change_y = 0      
                self.on_ground = True
            
            # If we are on a ground where there player can't fall through 
            # set able_drop to False
            if isinstance(block, Ground):
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                    self.on_ground = True
                    self.able_drop = False
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                    
                self.change_y = 0      
                
                    
        # Check for collision with player 2
        hit_player = pygame.sprite.collide_rect(self, self.enemy)
        if hit_player and self.change_y > 0:
            if self.change_x > 0:
                self.rect.left = self.enemy.rect.right
            elif self.change_x < 0:
                self.rect.right = self.enemy.rect.left
            else:
                self.rect.bottom = self.enemy.rect.top
            
            self.on_ground = True
               
    def inside_platform(self, block):
        """ Use to put collison only on the top of a platform """
        return (block.rect.top < self.rect.bottom and 
                self.rect.bottom < block.rect.top + 35)
    
    # -- Passives Method --        
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
    
    def restore_stamina(self):
        if self.current_stamina < self.total_stamina:
            if self.change_x == 0 and self.change_y == 0:
                self.stamina_rate = 15
            else:
                self.stamina_rate = 10
                
            self.current_stamina += self.stamina_rate
            
        if self.current_stamina > self.total_stamina:
            self.current_stamina = self.total_stamina
            
    def status_bar(self):
        """ Show the bars for health and stamina """
        x = 0
        if self.num == 0:
            x = 10 # bar for first player
        else:
            x = 614 # bar for second player
        health_bar = StatusBar(self.screen, x, 10, (228,7,7))
        stamina_bar = StatusBar(self.screen, x, 40, (55,204,55))

        health_bar.update(self.current_health / self.total_health)
        stamina_bar.update(self.current_stamina / self.total_stamina)
    
    # -- Attacks Method -- 
    def sufficient_stamina(self, num):
        """ Determine if the player has enought stamina to use the attack """
        cost = 0
        if num == 0: # Melee attack
            cost = self.melee_cost 
        elif num == 1: # Laser attack
            cost = self.laser_cost
            
        return self.current_stamina >= cost
    
    def create_sword(self):
        """ Create the melee weapon """
        self.weapon = Weapon()
        self.weapon.player = self
        self.weapon.enemy = self.enemy
        self.weapon_sprite.add(self.weapon)
    
    def melee_attack(self):           
        self.weapon.attack_animation()
    
    def range_attack(self):
        self.current_stamina -= self.laser_cost
        # Create the long range attack        
        laser = Laser(BLUE_LASER)
        laser.rect.x = self.rect.x + 20
        laser.starting_x = self.rect.x
        laser.rect.y = self.rect.y + self.rect.height / 2
        laser.player = self
        laser.enemy  = self.enemy
        laser.direction = self.direction
        return laser   
    
    def damage(self, damage):
        """ Handles the damage that the player takes """
        self.current_health -= damage
        
        if self.current_health <= 0:
            self.current_health = 0
            self.status_bar()
            self.alive = False     
    
    # -- Movement Method --
    def jumping_speed(self):
        """ adjust the movement speed 
            if the player jumps it's movement speed is decreased
            when the player lands it's movement speed is increased
        """
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
    
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        
        # If it is ok to jump, set our speed upwards
        if ((self.rect.bottom >= self.screen_height and self.on_ground) or 
            len(platform_hit_list) > 0):
            self.change_y = self.jump_height
            self.on_ground = False        

    def go_left(self):
        if self.rect.x > self.left_screen_boundary:
            self.change_x = self.movement_speed * -1
            self.direction = "L"
        elif self.rect.x  < self.left_screen_boundary:
            self.rect.x = self.left_screen_boundary + 10
            
    def go_right(self):
        if self.rect.x < self.right_screen_boundary:
            self.change_x = self.movement_speed
            self.direction = "R"
        elif self.rect.x > self.right_screen_boundary:
            self.rect.x = self.right_screen_boundary - 10
            
    def stop(self):
        self.change_x = 0  
    
    def drop(self):
        """ Fall through platforms """
        if (self.on_ground and self.rect.y < self.screen_height - 200 and 
            self.able_drop):    
            # If it is ok to jump, set our speed upwards
            self.rect.y = self.rect.y + 35
            self.on_ground = False
        self.change_y += 20
    
    # -- Sprite Method -- 
    def update_sprite(self):
        # Update the walking sprite
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
    
    def load_sprite(self, file):
        # Load Movement sprites right side
        sprite_sheet = SpriteSheet(file)
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
        
        # Load Movement Sprites Left side
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
        
        # Load jumping sprite
        image = sprite_sheet.get_image(375, 0, 120, 165)
        image = pygame.transform.scale(image, (64, 88))
        self.jumping_frames_r.append(image)
        self.jumping_frames_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.jumping_frames_l.append(image)
        self.jumping_frames_l.append(image)
        
#sprite coordinates
BLUE_LASER = (105, 0, 100, 38)
