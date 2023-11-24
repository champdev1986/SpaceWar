import pygame
import time
import random
import math
from models.space_ship import Spaceship
from models.space_ship_bullet import SpaceShipBullet
from models.enemy import Enemy
from models.astronaut import Astronaut
from models.left_wing_bullet import LeftWingBullet
from models.right_wing_bullet import RightWingBullet
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
game_over_sound = pygame.mixer.Sound('assets/game_over.mp3')
extra_gun_sound = pygame.mixer.Sound('assets/extra_gun.mp3')
collision_sound = pygame.mixer.Sound('assets/collision.mp3')

# define game variables
allSprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
spaceShipBullets = pygame.sprite.Group()
leftWingBullets = pygame.sprite.Group()
rightWingBullets = pygame.sprite.Group()
astronauts = pygame.sprite.Group()

bg_height = bg.get_height()
tiles = math.ceil(SCREEN_HEIGHT / bg_height) + 1

FONT = pygame.font.SysFont("comicsans", 30)

# def draw(player, elapsed_time, stars, scroll):
def draw(all_sprites, elapsed_time, score, scroll, lives):

    # draw scrolling background 
    for i in range(0, tiles):
        screen.blit(bg, (0, 160-i*bg_height + scroll))

    # draw elapsed time
    timeText = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    screen.blit(timeText, (10, 10))

    scoreText = FONT.render(f"Score: {score}", 1, "white")
    screen.blit(scoreText, (660, 10))

    livesText = FONT.render(f"Lives: {lives}", 1, "white")
    screen.blit(livesText, (670, 60))

    # draw sprites
    all_sprites.draw(screen)

    pygame.display.flip()

def game_over():
    pygame.mixer.music.stop()
    game_over_sound.play()
    lost_text = FONT.render("You lost!", 1, "white")
    screen.blit(lost_text, (SCREEN_WIDTH/2 - lost_text.get_width()/2, SCREEN_HEIGHT/2 - lost_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(GAME_OVER_DELAY)


def main():
    running = True
    enemySpawnTimer = pygame.time.get_ticks()
    astronautSpawnTimer = pygame.time.get_ticks()
    scroll = 0

    clock = pygame.time.Clock()
    startTime = time.time()
    elapsedTime = 0
    score = 0
    lives = 3
    amount_of_guns = 1
    levelIncreaseTimer = 0
    level = 1
    
    # create player
    player = Spaceship(player_image, SCREEN_WIDTH/2-PLAYER_WIDTH/2, SCREEN_HEIGHT - PLAYER_HEIGHT/2)
    allSprites.add(player)
    allSprites.update()

    # start background music
    pygame.mixer.music.play(-1)

    while running:

        elapsedTime = time.time() - startTime # elapsed time to draw
        current_time = pygame.time.get_ticks() // 1000  # Get current time in seconds

        if current_time - levelIncreaseTimer >= GAME_LEVEL_INTERVAL:
            levelIncreaseTimer = current_time
            level += 1

        if current_time - enemySpawnTimer >= ENEMY_SPAWN_INTERVAL or len(enemies) < 5:
            enemySpawnTimer = current_time
            for _ in range(2 * level):
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
                match amount_of_guns:
                    case 1:                               
                        spaceShipBullet = SpaceShipBullet(player.rect.centerx, player.rect.top)
                        spaceShipBullets.add(spaceShipBullet)
                        allSprites.add(spaceShipBullet) 
                    case 2:
                        leftWingBullet = LeftWingBullet(player.rect.centerx - 20, player.rect.top - 20)  
                        leftWingBullets.add(leftWingBullet)
                        allSprites.add(leftWingBullet) 
                        rightWingBullet = RightWingBullet(player.rect.centerx + 20, player.rect.top - 20)  
                        rightWingBullets.add(rightWingBullet)
                        allSprites.add(rightWingBullet) 
                    case 3:
                        spaceShipBullet = SpaceShipBullet(player.rect.centerx, player.rect.top)
                        spaceShipBullets.add(spaceShipBullet)
                        allSprites.add(spaceShipBullet) 
                        leftWingBullet = LeftWingBullet(player.rect.centerx - 20, player.rect.top - 20)  
                        leftWingBullets.add(leftWingBullet)
                        allSprites.add(leftWingBullet) 
                        rightWingBullet = RightWingBullet(player.rect.centerx + 20, player.rect.top - 20)  
                        rightWingBullets.add(rightWingBullet)
                        allSprites.add(rightWingBullet) 

        # check for collisions
        hitsPlayerWithEnemy = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle)
        if hitsPlayerWithEnemy:     
            collision_sound.play()
            if amount_of_guns > 1:
                amount_of_guns -= 1
                for enemy in hitsPlayerWithEnemy:
                    enemy.kill()
            else:   
                game_over() 
                running = False
                break
                

        for playerBullet in spaceShipBullets:
            hitsEnemyWithBullet = pygame.sprite.spritecollide(playerBullet, enemies, True)
            if hitsEnemyWithBullet:
                for enemy in hitsEnemyWithBullet:
                    playerBullet.kill()

        for leftWingBullet in leftWingBullets:
            hitsEnemyWithBullet = pygame.sprite.spritecollide(leftWingBullet, enemies, True)
            if hitsEnemyWithBullet:
                for enemy in hitsEnemyWithBullet:
                    leftWingBullet.kill()

        for rightWingBullet in rightWingBullets:
            hitsEnemyWithBullet = pygame.sprite.spritecollide(rightWingBullet, enemies, True)
            if hitsEnemyWithBullet:
                for enemy in hitsEnemyWithBullet:
                    rightWingBullet.kill()     

        hitsPlayerWithAstronaut = pygame.sprite.spritecollide(player, astronauts, True)
        if hitsPlayerWithAstronaut:
            extra_gun_sound.play()
            score += 1
            if amount_of_guns < 3:
                amount_of_guns += 1

        for enemy in enemies:
            if enemy.rect.top > SCREEN_HEIGHT:
                enemies.remove(enemy)

        # check for astronauts falling down
        for astronaut in astronauts:
            astronaut.update()
            if astronaut.rect.top > SCREEN_HEIGHT:
                lives -= 1
            if lives < 0:
                game_over()
                running = False
                break

        allSprites.update() # update all sprites

        draw(allSprites, elapsedTime, score, scroll, lives)
        
        # scroll background
        scroll += 5

        #reset scroll
        if scroll > bg_height:
            scroll = 0
        
        clock.tick(FPS) #define FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()