import pygame
import random
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.radius = 25  # Adjust the radius for appropriate collision size
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            # self.rect.y = random.randint(-100, -50)
            self.rect.y = -20
        self.mask = pygame.mask.from_surface(self.image)