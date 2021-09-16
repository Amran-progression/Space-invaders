import pygame
import random

from pygame.constants import KEYDOWN, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_a, K_d, K_s, K_w

pygame.init()
pygame.font.init()




myfont = pygame.font.SysFont('Comic Sans MS', 30)

clock = pygame.time.Clock()

WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet_img = pygame.image.load('bullet.png')
background = pygame.image.load('assets\space.png')
player_img = pygame.image.load('assets\spaceship_yellow.png')
enemy_img = pygame.image.load('assets\spaceship_red.png')
logo_img = pygame.image.load('logo.png')

bullet_sound = pygame.mixer.Sound('bulletsound.mp3')
music = pygame.mixer.music.load('spaceinvaders1.mp3')
pygame.mixer.music.play(-1)




player = pygame.transform.scale(pygame.transform.rotate(player_img, 180),(30,30))
enemy = pygame.transform.scale(enemy_img,(30,30))
bullet_surface = pygame.transform.scale(bullet_img,(12,18))
logo = pygame.transform.scale(logo_img, (350,250))

screen_size = screen.get_size()
bg_size = background.get_size()



pygame.display.set_caption("Space Invaders: My Iteration")


cube = pygame.Rect(250, 400,30,30)

pygame.time.set_timer(pygame.USEREVENT+1, 1000)
pygame.time.set_timer(pygame.USEREVENT+2, random.randint(500,1000))



cube_hit = pygame.USEREVENT+2
    
def menu():
   running = True

   menu_surface = myfont.render("Press P to play",True, (255,255,255))
   menu_rect = menu_surface.get_rect(center = (250,350))
   while running:
       clock.tick(60)
       
       screen.fill((255,255,255))
       screen.blit(background,(0,0))
       screen.blit(logo,(80,50))
       screen.blit(menu_surface,menu_rect)
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
                running = False
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_p:
                    main()
       pygame.display.update()

def game_over():
   running = True

   menu_surface = myfont.render("Game Over",True, (255,255,255))
   score_surface = myfont.render("Score:"+str(score),True, (255,255,255))
   gameover_surface = myfont.render('Press R to play again',True,(255,255,255))
   menu_rect = menu_surface.get_rect(center = (250,150))
   score_rect_ = score_surface.get_rect(center = (250,200))
   gameover_rect = gameover_surface.get_rect(center = (250,250))
   while running:
       clock.tick(60)
       
       screen.fill((255,255,255))
       screen.blit(background,(0,0))
       
       screen.blit(score_surface,score_rect_)
       screen.blit(gameover_surface,gameover_rect)
       screen.blit(menu_surface,menu_rect)
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
                running = False
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_r:
                    main()
       pygame.display.update()


def score_display():
    score_surface = myfont.render("Score: "+str(score), True,(255,255,255))
    score_rect = score_surface.get_rect(center = (250,50))
    screen.blit(score_surface, score_rect)



def main():  
    global score  
    bg_x = (bg_size[0] - screen_size[0]) // 2
    bg_y = (bg_size[1] - screen_size[1]) // 2
    score = 0
    bullet_list = []
    enemy_bullet_list = []
    blue_rect_list = []

    running = True
    while running:
      
        clock.tick(60)
        screen.fill((255,255,255))
        screen.blit(background, (-bg_x,-bg_y))
        screen.blit(player, (cube.x,cube.y))
        
        bullet = pygame.Rect(cube.x,cube.y,7,14)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:                  
                    bullet_list.append(bullet)
                    bullet_sound.play()
            
                    
            if event.type == pygame.USEREVENT+1:
                blue_rect = pygame.Rect(random.randrange(0,WIDTH-30),random.randrange(0,HEIGHT/4),30,30)
                enemy_bullet = pygame.Rect(blue_rect.x,blue_rect.y,7,14)
                blue_rect_list.append(blue_rect)
                enemy_bullet_list.append(enemy_bullet)

        for enemy_bullet in enemy_bullet_list:
            screen.blit(bullet_surface,(enemy_bullet.x,enemy_bullet.y))
            enemy_bullet.y += 8


        for bullet in bullet_list:
            screen.blit(bullet_surface, (bullet.x,bullet.y))
            bullet.y -= 7        

        for blue_rect in blue_rect_list:
            screen.blit(enemy, (blue_rect.x, blue_rect.y))
            blue_rect.y+=3
            if enemy_bullet.colliderect(cube):
                running = False
                game_over()
                 
            if bullet.colliderect(blue_rect) and bullet_list:
                score = score + 1
                blue_rect_list.remove(blue_rect)
                bullet_list.remove(bullet)
            if cube.colliderect(blue_rect):
                running = False
                game_over()
     
                
        score_display()

        if (pygame.key.get_pressed()[K_DOWN] or pygame.key.get_pressed()[K_s]) and cube.y < HEIGHT - 30:
            cube.y+=5
            bg_y -=2
        if (pygame.key.get_pressed()[K_UP] or pygame.key.get_pressed()[K_w]) and cube.y > 0:
            cube.y-=5
            bg_y +=2
        if (pygame.key.get_pressed()[K_LEFT] or pygame.key.get_pressed()[K_a]) and cube.x > 0:
            cube.x-=5
            bg_x +=2
        if (pygame.key.get_pressed()[K_RIGHT] or pygame.key.get_pressed()[K_d]) and cube.x < WIDTH - 30:
            cube.x+=5
            bg_x -=2
        bg_x = max(0, min(bg_size[0]-screen_size[0], bg_x)) 
        bg_y = max(0, min(bg_size[1]-screen_size[1], bg_y))


    
        pygame.display.update()
    
    pygame.quit()
    quit()


menu()
