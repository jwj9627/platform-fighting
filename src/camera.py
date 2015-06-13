import pygame

class camera_movment(pygame.sprite.Sprite):
    """Creates a sprites that is always halfway between player 1 and player 2.
        This is use to keep both players on the screen at the same time """
    def __init__(self, player1, player2):
        # Call the parent's constructor
        super().__init__()
        
        self.player1 = player1
        self.player2 = player2
        
        width = 20
        height = 20
        self.image = pygame.Surface([width, height])
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.x = (self.player1.rect.x + self.player2.rect.x) / 2
        self.rect.y = 500
        