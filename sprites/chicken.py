import pygame
from settings import *

class Chicken(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Display dimensions
        self.display_width = 60
        self.display_height = 60
        
        # Load individual animation sprites
        self.animations = {
            'run': self._load_animation_frames('assets/chicken_run.png', 4),
            'jump': self._load_animation_frames('assets/chicken_jump.png', 4),
            'duck': self._load_animation_frames('assets/chicken_duck.png', 4)
        }
        
        # Animation state
        self.current_state = 'run'
        self.current_frame = 0
        self.animation_speed = 0.1
        self.image = self.animations[self.current_state][self.current_frame]
        self.rect = self.image.get_rect()
        
        # Physics
        self.rect.x = 100
        self.rect.bottom = GROUND_HEIGHT
        self.velocity_y = 0
        self.jumping = False
        self.ducking = False
        self.on_ground = True
        
        # Hitbox adjustments
        self.hitbox_offset_x = 10
        self.hitbox_offset_y = 5
    
    def _load_animation_frames(self, path, frame_count,):
        """Load and prepare animation frames from a sprite sheet"""
        sheet = pygame.image.load(path).convert_alpha()
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()
        
        frames = []
        for i in range(frame_count):
            # Extract frame
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            
            # Scale while maintaining aspect ratio
            scale_factor = min(
                self.display_width/frame_width, 
                self.display_height/frame_height
            )
            new_width = int(frame_width * scale_factor)
            new_height = int(frame_height * scale_factor)
            frame = pygame.transform.scale(frame, (new_width, new_height))
            
            # Center in display size
            centered_frame = pygame.Surface((self.display_width, self.display_height), pygame.SRCALPHA)
            x_offset = (self.display_width - new_width) // 2
            y_offset = (self.display_height - new_height) // 2
            centered_frame.blit(frame, (x_offset, y_offset))
            
            frames.append(centered_frame)
        
        return frames
    
    def update(self):
        # Animation updates
        self.current_frame += self.animation_speed
        
        # State management
        if self.jumping:
            self.current_state = 'jump'
            self.rect.height = self.display_height
        elif self.ducking:
            self.current_state = 'duck'
            self.rect.height = self.display_height * 0.7  # Ducking is shorter
        else:
            self.current_state = 'run'
            self.rect.height = self.display_height
        
        # Loop animation
        if self.current_frame >= len(self.animations[self.current_state]):
            self.current_frame = 0
        
        # Update image and hitbox
        self.image = self.animations[self.current_state][int(self.current_frame)]
        self.rect.width = self.display_width
        
        # Physics
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Ground collision
        if self.rect.bottom > GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.velocity_y = 0
            self.on_ground = True
            self.jumping = False
    
    def jump(self):
        if self.on_ground and not self.ducking:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False
            self.jumping = True
            self.current_frame = 0
    
    def duck(self, is_ducking):
        if self.on_ground and not self.jumping:
            self.ducking = is_ducking
            if is_ducking:
                self.current_frame = 0