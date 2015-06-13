import pygame
from spritesheet_functions import SpriteSheet

class Projectile(pygame.sprite.Sprite):
    """ This class represents the Laser . """
    def __init__(self, sprite_sheet_data):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.player = None
        self.enemy = None
        # Direction used to determine which direction the laser travels
        self.direction = None
        self.starting_x = None

        sprite_sheet = SpriteSheet("resources/attacks/laser.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
        
        self.image = pygame.transform.scale(self.image, (50, 14))
        self.rect = self.image.get_rect()


class Laser(Projectile):
    """ Create the characters long range attack

        Attributes:
            speed: movement speed of the laser
            range: the distance the laser can move before it is destroyed
            dmg: laser does 15 damage. As it travels the damage is does is 
                 increased by 1.1
    """
    
    speed = 35
    range = 850
    dmg = 0
    
    def update(self):
        self.move()
        self.dmg += 1.1
        
    def move(self):
        if self.direction == 'R':
            self.rect.x += self.speed
        else:
            self.rect.x += self.speed * -1
        