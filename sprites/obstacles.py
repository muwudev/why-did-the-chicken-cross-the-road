import pygame
from settings import *

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Single fixed size for all obstacles
        self.image = pygame.Surface((40, 50))  # Width: 40px, Height: 50px
        self.image.fill(RED)  # Solid red color
        
        # Position at ground level, starting off-screen right
        self.rect = self.image.get_rect()
        self.rect.bottom = GROUND_HEIGHT
        self.rect.left = SCREEN_WIDTH
    
    def update(self):
        # Move left at constant speed
        self.rect.x -= OBSTACLE_SPEED
        
        # Remove when off-screen
        if self.rect.right < 0:
            self.kill()

        

def create_random_obstacle():
    # Always returns the same simple obstacle
    return Obstacle()