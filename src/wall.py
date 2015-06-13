import pygame

class Wall(pygame.sprite.Sprite):
    """ Create a wall which a player can wall climb """
    def __init__(self, x, y, width, height, player1, player2):
        pygame.sprite.Sprite.__init__(self)
        
        self.player1 = player1
        self.player2 = player2
        
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill((0,0,0))
        
    def update(self):
        self.collision()
    
    def collision(self):
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player1)
        if hit:
            # If we are moving right, set our right side
            # to the left side of the item we hit
            
            # Allow wall climbing
            if self.player1.change_x > 0:
                self.player1.on_ground = True
                self.player1.rect.right = self.rect.right
                
            elif self.player1.change_x < 0:
                self.player1.on_ground = True
                self.player1.rect.left = self.rect.left
        
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player2)
        if hit:
            # Allows wall climbing
            if self.player2.change_x > 0:
                self.player2.rect.right = self.rect.right
            elif self.player2.change_x < 0:
                self.player2.rect.left = self.rect.left
        
class Ground(pygame.sprite.Sprite):
    """ Creates a ground that the player can not fall through"""
    def __init__(self, x, y, width, height, player1, player2):
        pygame.sprite.Sprite.__init__(self)
        
        self.player1 = player1
        self.player2 = player2
        
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill((0,0,0))
        
    def update(self):
        self.collision()
        
    def collision(self):
        hit = pygame.sprite.collide_rect(self, self.player1)        
        if hit:
            if self.player1.rect.x > self.rect.x:
                # Reset our position based on the top/bottom of the object.
                self.player1.rect.bottom = self.rect.top
                # Stop our vertical movement
                self.player1.change_y = 0      
                self.player1.on_ground = True
                self.player1.able_drop = False
            
            if self.player1.change_y < 0:
                self.player1.rect.top = self.rect.bottom
                self.player1.change_y = 0
                
        hit = pygame.sprite.collide_rect(self, self.player2)
        if hit:
            if self.player2.rect.x > self.rect.x:
                # Reset our position based on the top/bottom of the object.
                self.player2.rect.bottom = self.rect.top
                # Stop our vertical movement
                self.player2.change_y = 0      
                self.player2.on_ground = True
                self.player2.able_drop = False
            
            if self.player2.change_y < 0:
                self.player2.rect.top = self.rect.bottom
                self.player2.change_y = 0