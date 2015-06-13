import pygame

class StatusBar:
    """ Status Bar to display health, stamina, etc"""
    
    # Background
    BACKGROUND1 = (229,229,229)
    BACKGROUND2 = (203,203,203)

    def __init__(self, screen, x, y, color):
        """ Constructor Pass in the x and y values and the color of the bar"""
        self.screen = screen
        self.x = x
        self.y = y
        self.color = color
    
    def update(self, width):
        """ Draws the background and updates the bar to show how much health,
            stamina, ect is left"""
        self.draw_background()
        self.draw_bar(width)
    
    def draw_background(self):
        """ Create the background that the bars are placed on"""
        pygame.draw.rect(self.screen, self.BACKGROUND1, (self.x, self.y, 400, 30))
        pygame.draw.rect(self.screen, self.BACKGROUND2, (self.x + 5, self.y + 5, 
                                                         390, 20), 3)
        
    def draw_bar(self, width):
        """ Draw the background with the amount of health, stamina, ect that is 
            left"""
        pygame.draw.rect(self.screen, self.color, (self.x + 8, self.y + 8, 
                                                   384 * width, 14))