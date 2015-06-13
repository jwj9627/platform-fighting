import sys
import pygame


class Menus():
    """Contains all of the menus used in the game"""
    def __init__(self, screen):
        self.screen = screen
        
    def display_maps(self):
        """Show  levels in the game"""
        self.screen.fill((0,0,0))
        
        # Display levels
        lv1 = pygame.image.load('resources/icons/lv1.png')
        lv2 = pygame.image.load('resources/icons/lv2.png')
        self.screen.blit(lv1,(25,200))
        self.screen.blit(lv2,(600,200))
        
        # Display level number
        font = pygame.font.SysFont('Calibri', 45, True, False)
        
        menu_text = font.render('Select Level' , True ,(255,255,255))
        lv1_text = font.render("1: Castle", True, (255,255,255))
        lv2_text = font.render('2: Parasol ' ,True ,(255,255,255))
        
        self.screen.blit(menu_text, [1024 / 2 - 100, 50])
        self.screen.blit(lv1_text, [150, 150])
        self.screen.blit(lv2_text, [700, 150])
        pygame.display.flip()
          
    def level_choice(self):
        """ Get the users choice"""
        self.display_maps()
        
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 0
                    if event.key == pygame.K_2:
                        return 1
    
    def display_winner(self, winner):
        """ Shows the game over screen. Show rematch or quit """
        font = pygame.font.SysFont('Calibri', 45, True, False)
        text = font.render(winner,True ,(0,0,0))
        self.screen.blit(text, [400,225])
        
        font = pygame.font.SysFont('Calibri', 45, True, False)
        
        rematch_text = font.render("Y: Rematch",True ,(0,0,0))
        quit_text = font.render("N: Quit",True ,(0,0,0))
    
        self.screen.blit(rematch_text, [400,275])
        self.screen.blit(quit_text, [385,325])
        
        pygame.display.flip()
                    
    def game_over(self):
        """ Take users choice to either quit or rematch """
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return False                    
    
                    if event.key == pygame.K_n:
                        sys.exit()        

    def display_camera(self):
        """ Show the camera options """
        self.screen.fill((0,0,0))
        
        cam1 = pygame.image.load('resources/icons/cam1.png')
        cam2 = pygame.image.load('resources/icons/cam2.png')
        self.screen.blit(cam1,(100,200))
        self.screen.blit(cam2,(675,200))
        
        # Display level number
        font = pygame.font.SysFont('Calibri', 45, True, False)
        
        menu_text = font.render('Select Camera' , True ,(255,255,255))
        cam1_text = font.render("Camera 1", True, (255,255,255))
        cam2_text = font.render('Camera 2' ,True ,(255,255,255))
        
        self.screen.blit(menu_text, [1024 / 2 - 120, 50])
        self.screen.blit(cam1_text, [150, 150])
        self.screen.blit(cam2_text, [725, 150])
        pygame.display.flip()
    
    def camera_choice(self):
        """ Get users choice for camera """
        self.display_camera()
        
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return False
                    if event.key == pygame.K_2:
                        return True
    
    def loading(self):
        font = pygame.font.SysFont('Calibri', 45, True, False)
        menu_text = font.render('Loading...' , True ,(255,0, 0))
        self.screen.blit(menu_text, [1024 / 2 - 75, 450])
        pygame.display.flip()
        
        