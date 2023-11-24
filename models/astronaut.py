import pygame
import random
from constants import *

class Astronaut(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = ASTRONAUT_SPEED  # Adjust the falling speed as needed
        self.radius = 25

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # Remove if it goes off the screen
        self.mask = pygame.mask.from_surface(self.image)
        
