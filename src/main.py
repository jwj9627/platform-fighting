import pygame
import sys
from player import Player
from camera import camera_movment
from level import Level_01
from level import Level_02
from menus import Menus

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = int((SCREEN_WIDTH * 3) / 4)

def main():
    """ Main Program """ 
    pygame.init() 
    
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("Platformer Fighting Game")
            
    # Manage how fast the screen updates
    fps_clock = pygame.time.Clock()
    fps = 30
    
    # Create and setup player 1 and player 2
    player = Player(SCREEN_HEIGHT, SCREEN_WIDTH, screen, 0)
    player2 = Player(SCREEN_HEIGHT, SCREEN_WIDTH, screen, 1)

    player.enemy = player2
    player2.enemy = player
    
    player.create_sword()
    player2.create_sword()
    
    #Load menu music
    #pygame.mixer.music.load('resources\music\Dark Ambience.ogg')
    pygame.mixer.music.load('resources\music\Last_Man_Standing.ogg')
    pygame.mixer.music.play()
    
    menu = Menus(screen)
    
    # If settings is one camera will be None else a camera is created
    camera = None
    cam_option = menu.camera_choice()
    if cam_option: 
        camera = camera_movment(player, player2)
    
    menu.loading()    
    
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player, player2))
    level_list.append(Level_02(player, player2))
    
    
    # Set the current Level
    current_level_no = menu.level_choice()
    current_level = level_list[current_level_no]
    
    player.level = current_level
    player2.level = current_level
    
    # Create list
    active_sprite_list = pygame.sprite.Group()
    projectile_sprite_list = pygame.sprite.Group()
    
    # set players position
    reset_players(player, player2, camera)
   
    # Add players and if need the camera to list
    active_sprite_list.add(player)
    active_sprite_list.add(player2)
    if camera is not None: active_sprite_list.add(camera)

    #Load sounds
    sword_sound = pygame.mixer.Sound('resources/sounds/sword_sound.wav') 
    laser_sound = pygame.mixer.Sound('resources/sounds/laser_sound.ogg') 
    
    set_music(current_level_no)
    
    # Loop until the user clicks the close button
    done = False
    
    while(True):
        
        # ------ Main Program Loop ------ 
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    sys.exit()
                
                # Player 1 controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player.go_left()
                    if event.key == pygame.K_d:
                        player.go_right()
                    if event.key == pygame.K_w:
                        player.jump()
                    if event.key == pygame.K_s:
                        player.drop()
                    if event.key == pygame.K_f:
                        if player.sufficient_stamina(1):
                            laser_sound.play()
                            laser = player.range_attack()
                            active_sprite_list.add(laser)
                            projectile_sprite_list.add(laser)
                            current_level.projectile_list.append(laser)
                            
                    if event.key == pygame.K_t:
                        player.attacking = True
                        sword_sound.play()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and player.change_x < 0:
                        player.stop()
                    if event.key == pygame.K_d and player.change_x > 0:
                        player.stop()
                    
                # Player 2 controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        player2.go_left()
                    if event.key == pygame.K_k:
                        player2.go_right()
                    if event.key == pygame.K_u:
                        player2.jump()
                    if event.key == pygame.K_j:
                        player2.drop()
                    if event.key == pygame.K_l:
                        if player2.sufficient_stamina(1):
                            laser_sound.play()
                            laser = player2.range_attack()
                            active_sprite_list.add(laser)
                            projectile_sprite_list.add(laser)
                            current_level.projectile_list.append(laser)
                    if event.key == pygame.K_p:
                        player2.attacking = True
                        sword_sound.play()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_h and player2.change_x < 0:
                        player2.stop()
                    if event.key == pygame.K_k and player2.change_x > 0:
                        player2.stop()
                    
            for laser in projectile_sprite_list:      
                if (laser.rect.x > laser.starting_x + laser.range or 
                    laser.rect.x < laser.starting_x - laser.range):
                    projectile_sprite_list.remove(laser)
                    active_sprite_list.remove(laser)
                 
                hit = pygame.sprite.collide_rect(laser, laser.enemy)
                if hit:
                    laser.enemy.damage(laser.player.laser_damage * 
                                       laser.player.stamina_penalty + laser.dmg)
                    projectile_sprite_list.remove(laser)
                    active_sprite_list.remove(laser)
            
            # If the player gets near the right side, shift the world left (-x)
            shift_left(player, current_level, camera)
            
            # If the player gets near the left side, shift the world right (+x)
            shift_right(player, current_level, camera)
            
            player.left_screen_boundary  = player2.rect.x - 850
            player.right_screen_boundary = player2.rect.x + 850
            player2.left_screen_boundary  = player.rect.x - 850
            player2.right_screen_boundary = player.rect.x + 850
            
            # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
            current_level.draw(screen)
            active_sprite_list.draw(screen)
     
            # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
            # Update the player
            active_sprite_list.update()
            
            # Update items in the level
            current_level.update()
            
            # Limit to 60 frames per second
            fps_clock.tick(fps)
     
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            
            if not player.alive:
                done = True
                menu.display_winner('Player 2 wins')
            elif not player2.alive: 
                menu.display_winner('Player 1 wins')
                done = True
        
        projectile_sprite_list.empty()
        
        # Game Over screen
        # prompt user for rematch or quit
        done = menu.game_over()
        
        # If rematch show level select then reset everything
        if not done: 
            current_level_no = menu.level_choice()
            current_level = level_list[current_level_no]
            player.level = current_level
            player2.level = current_level
            set_music(current_level_no)
            reset_players(player, player2, camera)

def set_music(current_level_no):
    pygame.mixer.music.stop()
    
    if current_level_no == 0:
        pygame.mixer.music.load('resources\music\day_60.ogg')
    else:
        pygame.mixer.music.load('resources\music\Data_Corruption.ogg')
    
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play()

def reset_players(player, player2, camera):
    player.rect.x = 200
    player.rect.y = 500
    player.current_health = player.total_health
    player.alive = True
    

    player2.rect.x = 700
    player2.rect.y = 500
    player2.current_health = player2.total_health
    player2.alive = True
    
    if camera is not None: camera = camera_movment(player, player2)

def shift_left(player, current_level, camera):   
    # Shift everything in the level to the left
    if camera is not None:
        if camera.rect.x >= 400:
            diff = camera.rect.x - 400
            camera.rect.x = 400
            current_level.shift_world(-diff, camera)

    elif player.rect.x >= 500:
        diff = player.rect.x - 500
        player.rect.x = 500
        current_level.shift_world(-diff, camera)

def shift_right(player, current_level, camera):
    # Shift everything in the level to the Right
    if camera is not None:
        if player.rect.x <= 450:
            diff = 450 - camera.rect.x
            camera.rect.x = 450
            current_level.shift_world(diff, camera)
        
    elif player.rect.x <= 120:
        diff = 120 - player.rect.x
        player.rect.x = 120
        current_level.shift_world(diff, camera)
            
if __name__ == "__main__":
    main()
        