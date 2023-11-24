import pygame
from constants import *

pygame.mixer.init()

# Определение классов
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = 20  # Adjust the radius for appropriate collision size
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 200 
        self.shoot_sound = pygame.mixer.Sound('assets/shoot.mp3')
        
    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot > self.shoot_delay

    def shoot(self):
        if self.can_shoot():
            self.last_shot = pygame.time.get_ticks()       
            self.shoot_sound.play()
        self.mask = pygame.mask.from_surface(self.image)        

    def move_left(self):
        self.rect.x -= PLAYER_SPEED

    def move_right(self):
        self.rect.x += PLAYER_SPEED

    def move_up(self):
        self.rect.y -= PLAYER_SPEED

    def move_down(self):
        self.rect.y += PLAYER_SPEED
    