import pygame
from constants import *

class LeftWingBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((3, 5))  # Bullet size
        self.image.fill(VIOLET)  # Bullet color
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10  # Adjust bullet speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
        # hits = pygame.sprite.spritecollide(self, enemies, True)  # Check collision with enemies
        # for enemy in hits:
        #     self.kill()