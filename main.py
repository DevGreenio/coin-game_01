import asyncio
import random
import pygame  # noqa: F401 — ΜΗΝ το σβήσεις: το pygbag διαβάζει ΜΟΝΟ αυτό το αρχείο για imports
import time

random.seed(time.time_ns())

# ---------------- Ρυθμίσεις ----------------
WIDTH, HEIGHT = 800, 600
FPS = 180
GAME_TIME = 60
TARGET=70
STARTING_LIVES = 3
HIT_COOLDOWN=1200 #milliseconds 1200==1,2 sec



async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #Loading Graphics
    player_img=pygame.image.load("images/player.png").convert_alpha()
    player_img=pygame.transform.scale(player_img, (40,40))

    enemy_img=pygame.image.load("images/enemy.png").convert_alpha()
    enemy_img=pygame.transform.scale(enemy_img, (50,50))

    yellow_coin_img=pygame.image.load("images/coin_yellow.png").convert_alpha()
    yellow_coin_img=pygame.transform.scale(yellow_coin_img, (30,30))
    blue_coin_img=pygame.image.load("images/coin_blue.png").convert_alpha()
    blue_coin_img=pygame.transform.scale(blue_coin_img, (30,30))
    purple_coin_img=pygame.image.load("images/coin_purple.png").convert_alpha()
    purple_coin_img=pygame.transform.scale(purple_coin_img, (30,30))
    
    
    pygame.display.set_caption("Coiner")
    clock = pygame.time.Clock()

    # ΒΗΜΑ 1 — ο παίκτης: ένα ορθογώνιο (x, y, πλάτος, ύψος)
    player = pygame.Rect(380, 280, 40, 40)
    speed = 5
    lives=STARTING_LIVES
    last_hit_time= -HIT_COOLDOWN

    enemy_x= 100
    enemy_y=150
    enemy = pygame.Rect(enemy_x,enemy_y,50,50)
    enemy_speed = 4
    enemy_dir=1

    # ΒΗΜΑ 3 — το νόμισμα: σε τυχαία θέση
    coin_x = random.randint(20, WIDTH - 20)
    coin_y = random.randint(20, HEIGHT - 20)

    coin_type=random.randint(1,10)

    if coin_type <=6:
        coin_color=(255, 209, 102) #yellow
        coin_value=1 #score + 1
    elif coin_type <= 9:
        coin_color=(70,150,255) # blue
        coin_value = 3 #score +3
    elif coin_type  == 10:
        coin_color = (192,100,255) #purp
        coin_value = 5 #score + 5



    score=0
    font = pygame.font.Font(None, 48)
    small_font=pygame.font.Font(None ,36)
    coin_font = pygame.font.Font(None, 24)

    start_time=pygame.time.get_ticks()
    
    won=False

    running = True
    game_over=False
    while running:
        # 1) ΓΕΓΟΝΟΤΑ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                player.x, player.y=380, 280
                coin_x=random.randint(20, WIDTH - 20)
                coin_y=random.randint(20, HEIGHT - 20)
                enemy_x= random.randint(25, WIDTH - 25)
                enemy_y=random.randint(25, HEIGHT -25)
                enemy_speed = 4
                score=0
                start_time = pygame.time.get_ticks()
                lives=STARTING_LIVES
                
                
                game_over=False
                won=False
                



        # 2) ΛΟΓΙΚΗ
        # ΒΗΜΑ 2 — κίνηση με τα βελάκια
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.x -= speed
            if keys[pygame.K_RIGHT]:
                player.x += speed
            if keys[pygame.K_UP]:
                player.y -= speed
            if keys[pygame.K_DOWN]:
                player.y += speed
            player.clamp_ip(screen.get_rect())


            coin_rect = pygame.Rect(coin_x - 15, coin_y - 15, 30, 30)
            if player.colliderect(coin_rect):
                coin_x=random.randint(20, WIDTH - 20)
                coin_y=random.randint(20, HEIGHT - 20)
                score+=coin_value
                coin_type = random.randint(1,10)
                if coin_type <=6:
                    coin_color=(255, 209, 102) #yellow
                    coin_value=1 #score + 1
                elif coin_type <= 9:
                    coin_color=(70,150,255) # blue
                    coin_value = 3 #score +3
                elif coin_type  == 10:
                    coin_color = (192,100,255) #purp
                    coin_value = 5 #score + 5
                if score%3==0:
                    enemy_speed+=1

            
            if enemy.left <= 0 or enemy.right >= WIDTH:
                enemy_dir*=-1
            enemy.x=enemy.x+enemy_speed*enemy_dir

            current_time=pygame.time.get_ticks()
            
            if enemy.colliderect(player):

            
            
                if current_time - last_hit_time >= HIT_COOLDOWN:
                    lives -=1
                    last_hit_time=current_time
                
                    player.x=380
                    player.y=280
                
                    if lives<=0:
                        game_over=True
                        won=False


            
            
            
            elapsed_time=(pygame.time.get_ticks()-start_time) // 1_000
            time_left=GAME_TIME - elapsed_time


            



            if time_left <=0 and score<TARGET:
                game_over = True
                won=False

            if time_left <=0 and score >= TARGET:
                game_over=True
                won=True


        
        

        # 3) ΖΩΓΡΑΦΙΚΗ
        screen.fill((15, 40, 60))
        
        screen.blit(player_img, player) #player
        
        
        if coin_value == 1:
            coin_img = yellow_coin_img
        elif: coin_value==3:
            coin_img=blue_coin_img
        else:
            coin_img=purple_coin_img
        
        screen.blit(coin_img, (coin_x - 15, coin_y - 15))
        value_text=coin_font.render(str(coin_value), True, (0,0,0))
        screen.blit(value_text, (coin_x - value_text.get_width()//2,coin_y - value_text.get_height()//2))

        screen.blit(enemy_img,enemy) #enemy


        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (20, 20))
        text1 = font.render(f"Time: {time_left}", True, (255, 255, 255))
        screen.blit(text1, (550, 20))
        txtfps = font.render(f"FPS: {FPS}", True, (255, 255, 255))
        screen.blit(txtfps, (20, 50))
        life_text=font.render(f"Lives: {lives}", True, (255,255,255))
        screen.blit(life_text, (550,50))

        if game_over:
            if won:
                msg = "You Win"
            else:
                msg= "You Lose"

            end_text = font.render(msg, True, (255, 255, 255))
            restart_text = small_font.render("Press R to retry", True, (255,255,255))

            screen.blit(end_text, (WIDTH // 2 - end_text.width // 2, HEIGHT // 2-40))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.width // 2, HEIGHT // 2 + 40))
        pygame.display.flip()

        clock.tick(FPS)
        await asyncio.sleep(0)  # ΜΗΝ το σβήσεις: χωρίς αυτό δεν τρέχει στο web

    pygame.quit()


asyncio.run(main())

