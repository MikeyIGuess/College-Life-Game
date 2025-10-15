import pygame
from constants import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    def apply(self, entity):
        # Returns a rectangle with the entity's position adjusted for camera
        return pygame.Rect(entity.rect.x - self.camera.x, entity.rect.y - self.camera.y, entity.rect.width, entity.rect.height)
    
    def apply_rect(self, rect):
        # Returns a rectangle with position adjusted for camera
        return pygame.Rect(rect.x - self.camera.x, rect.y - self.camera.y, rect.width, rect.height)
    
    def apply_pos(self, pos):
        # Returns a position tuple adjusted for camera
        return (pos[0] - self.camera.x, pos[1] - self.camera.y)
        
    def update(self, target):
        # Updates camera position to center on target
        x = -target.rect.x + WINDOW_WIDTH // 2
        y = -target.rect.y + WINDOW_HEIGHT // 2
        
        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WINDOW_WIDTH), x)  # right
        y = max(-(self.height - WINDOW_HEIGHT), y)  # bottom
        
        self.camera = pygame.Rect(-x, -y, self.width, self.height)