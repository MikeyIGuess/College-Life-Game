import pygame
from constants import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def update(self, target):
        # Calculate camera position to center on target
        x = -target.rect.centerx + WINDOW_WIDTH // 2
        y = -target.rect.centery + WINDOW_HEIGHT // 2

        # Create border effect near map edges
        if target.rect.centerx < WINDOW_WIDTH // 2:
            x = 0
        elif target.rect.centerx > MAP_WIDTH - (WINDOW_WIDTH // 2):
            x = -(MAP_WIDTH - WINDOW_WIDTH)
            
        if target.rect.centery < WINDOW_HEIGHT // 2:
            y = 0
        elif target.rect.centery > MAP_HEIGHT - (WINDOW_HEIGHT // 2):
            y = -(MAP_HEIGHT - WINDOW_HEIGHT)
        
        self.camera.x = x
        self.camera.y = y
    
    def apply(self, entity):
        # Adjust entity position relative to camera
        return pygame.Rect(
            entity.rect.x + self.camera.x,
            entity.rect.y + self.camera.y,
            entity.rect.width,
            entity.rect.height
        )