import pygame
from spritesheet_functions import SpriteSheet

class Weapon(pygame.sprite.Sprite):    
    """ Melee weapon 
    
        Attributes:
            travel: The amount the weapon can travel
            range: The amount the weapon has traveled
    """
    
    travel = 10
    range = 0
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.player = None
        self.enemy = None
        
        self.attack = False
        
        self.sword_frame_r = []
        self.sword_frame_l = []
        self.load_sprite()
        
        self.image = pygame.Surface([103, 32])
        self.image = self.sword_frame_r[0]
        self.rect = self.image.get_rect()
        
    def update(self):
        self.set_pos()
        #self.attack_animation()
    
    def set_pos(self):
        if not self.player.attacking:
            if self.player.direction == "R":
                self.rect.x = self.player.rect.x + 15
                self.rect.y = self.player.rect.y + 50
                self.image = self.sword_frame_r[0]
            elif self.player.direction == "L":
                self.rect.x = self.player.rect.x - 50
                self.rect.y = self.player.rect.y + 50
                self.image = self.sword_frame_l[0]
                
    def attack_animation(self):
        if self.travel > 0 and self.player.attacking and self.player.sufficient_stamina(0):
            self.player.current_stamina -= self.player.melee_cost

            if self.player.direction == "R":
                self.rect.x += self.range + 15
            elif self.player.direction == "L":
                self.rect.x -= self.range + 15
            
            self.travel -= 5
            self.range += 8
            self.move()
            self.attack_hit()
            
            self.rect.y = self.player.rect.y + 50

        else:
            self.travel = 10
            self.range = 5
            self.player.attacking = False
            
    def move(self):
        if self.player.change_x > 0:
            self.rect.x = self.player.rect.x
        
    def attack_hit(self):
        hit_player = pygame.sprite.collide_rect(self, self.enemy)
        if hit_player:
            self.enemy.damage(self.player.melee_damage * self.player.stamina_penalty)
    
    def load_sprite(self):    
        # Load sword sprite
        sprite_sheet = SpriteSheet("resources/attacks/Sword_Update1.png")
        image = sprite_sheet.get_image(0, 0, 103, 32)
        self.sword_frame_r.append(image)
        image = pygame.transform.flip(image, True, False)
        self.sword_frame_l.append(image)

