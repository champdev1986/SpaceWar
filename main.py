import pygame
import time
import random
import math
from models.space_ship import Spaceship
from models.space_ship_bullet import SpaceShipBullet
from models.enemy import Enemy
from models.astronaut import Astronaut
from constants import *

pygame.font.init()
pygame.mixer.init()

# creating screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space War")

# initializing the assets
bg = pygame.image.load("assets/bg.jpg").convert()
player_image = pygame.image.load('assets/spaceship1.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
enemy_image = pygame.image.load('assets/enemy.png').convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_WIDTH, ENEMY_HEIGHT))
astronaut_image =  pygame.image.load('assets/astronaut.png').convert_alpha()
astronaut_image = pygame.transform.scale(astronaut_image, (ASTRONAUT_WIDTH, ASTRONAUT_HEIGHT))

# initializing music and sounds
pygame.mixer.music.load('assets/background.mp3')
shoot_sound = pygame.mixer.Sound('assets/shoot.mp3')
game_over_sound = pygame.mixer.Sound('assets/game_over.mp3')

# define game variables
allSprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
spaceShipBullets = pygame.sprite.Group()
astronauts = pygame.sprite.Group()
amount_of_guns = 1

bg_width = bg.get_width()
tiles = math.ceil(SCREEN_HEIGHT / bg_width) + 1

FONT = pygame.font.SysFont("comicsans", 30)

# def draw(player, elapsed_time, stars, scroll):
def draw(all_sprites, elapsed_time, damage, score, scroll):

    # draw scrolling background 
    for i in range(0, tiles):
        screen.blit(bg, (0, 160-i*bg_width + scroll))

    # draw elapsed time
    timeText = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    screen.blit(timeText, (10, 10))

    damageText = FONT.render(f"Damage: {damage}", 1, "white")
    screen.blit(damageText, (600, 10))

    scoreText = FONT.render(f"Score: {score}", 1, "white")
    screen.blit(scoreText, (600, 30))

    # draw sprites
    all_sprites.draw(screen)

    pygame.display.flip()

def main():
    running = True
    enemySpawnTimer = pygame.time.get_ticks()
    astronautSpawnTimer = pygame.time.get_ticks()
    scroll = 0

    clock = pygame.time.Clock()
    startTime = time.time()
    elapsedTime = 0
    damage = 0
    score = 0
    
    # create player
    player = Spaceship(player_image, SCREEN_WIDTH/2-PLAYER_WIDTH/2, SCREEN_HEIGHT - PLAYER_HEIGHT)
    allSprites.add(player)
    allSprites.update()

    # start background music
    pygame.mixer.music.play(-1)

    # create enemies
    for _ in range(5):
        enemy = Enemy(enemy_image, random.randint(1, 3))
        allSprites.add(enemy)
        enemies.add(enemy)

    while running:

        elapsedTime = time.time() - startTime # elapsed time to draw

        current_time = pygame.time.get_ticks() // 1000  # Get current time in seconds

        if current_time - enemySpawnTimer >= ENEMY_SPAWN_INTERVAL:
            enemySpawnTimer = current_time
            for _ in range(3):  # Increase by 3 enemies each time
                enemy = Enemy(enemy_image, random.randint(1, 3))
                allSprites.add(enemy)
                enemies.add(enemy)
        
        if current_time - astronautSpawnTimer >= ASTRONAUT_SPAWN_INTERVAL:
            astronautSpawnTimer = current_time
            astronaut = Astronaut(astronaut_image)
            allSprites.add(astronaut)
            astronauts.add(astronaut)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
         
        # move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.move_left()
        if keys[pygame.K_RIGHT] and player.rect.right < SCREEN_WIDTH:
            player.move_right()
        if keys[pygame.K_UP] and player.rect.top > 0:
            player.move_up()
        if keys[pygame.K_DOWN] and player.rect.bottom < SCREEN_HEIGHT:
            player.move_down()
        if keys[pygame.K_SPACE]:
            if player.can_shoot():
                player.shoot()               
                shoot_sound.play()
                bullet = SpaceShipBullet(player.rect.centerx, player.rect.top)
                spaceShipBullets.add(bullet)
                allSprites.add(bullet)   

        # check for collisions
        hitsPlayerWithEnemy = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle)
        if hitsPlayerWithEnemy:            
            pygame.mixer.music.stop()
            game_over_sound.play()
            lost_text = FONT.render("You lost!", 1, "white")
            screen.blit(lost_text, (SCREEN_WIDTH/2 - lost_text.get_width()/2, SCREEN_HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(GAME_OVER_DELAY)
            running = False
            break

        for playerBullet in spaceShipBullets:
            hitsEnemyWithBullet = pygame.sprite.spritecollide(playerBullet, enemies, True)
            if hitsEnemyWithBullet:
                for enemy in hitsEnemyWithBullet:
                    playerBullet.kill()
                    score += 1

        hitsPlayerWithAstronaut = pygame.sprite.spritecollide(player, astronauts, True)
        if hitsPlayerWithAstronaut:
            print('Astronaut!')

        for enemy in enemies:
            # enemy.update()
            if enemy.rect.y > SCREEN_HEIGHT:
                damage += 1
                print(f"Damage = {damage}")
                enemies.remove(enemy)


        allSprites.update() # update all sprites

        # draw(player, elapsed_time, stars, scroll)
        draw(allSprites, elapsedTime, damage, score, scroll)
        
        # scroll background
        scroll += 5

        #reset scroll
        if scroll > bg_width:
            scroll = 0
        
        clock.tick(FPS) #define FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()