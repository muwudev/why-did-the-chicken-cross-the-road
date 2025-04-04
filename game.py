import pygame
import random
from settings import *
from sprites.chicken import Chicken
from sprites.obstacles import create_random_obstacle
from settings import DEATH_MESSAGES, DEATH_CAUSES, BUTCHER_QUOTES

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chicken Run")
        self.clock = pygame.time.Clock()
        self.running = True
        self.playing = False
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        # Chicken
        self.chicken = Chicken()
        self.all_sprites.add(self.chicken)
        
        # Obstacle timer
        self.obstacle_timer = 0
        self.game_start_time = 0
        self.delay_passed = False
        
        # Game state
        self.game_over = False
        self.butcher_quote = ""
        self.quote_timer = 0
        self.death_message = ""
        self.death_cause = ""
    
    def new_game(self):
        self.score = 0
        self.game_over = False
        self.obstacles.empty()
        self.chicken.rect.bottom = GROUND_HEIGHT
        self.chicken.velocity_y = 0
        self.chicken.jumping = False
        self.chicken.ducking = False
        self.playing = True
        self.butcher_quote = ""
        self.death_message = ""
        self.death_cause = ""
        self.game_start_time = pygame.time.get_ticks()
        self.delay_passed = False
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.playing:
                    self.chicken.jump()
                elif event.key == pygame.K_DOWN and self.playing:
                    self.chicken.duck(True)
                elif event.key == pygame.K_r and self.game_over:
                    self.new_game()
                elif event.key == pygame.K_RETURN and not self.playing and not self.game_over:
                    self.new_game()
                elif event.key == pygame.K_s and self.playing:
                    pass
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.chicken.duck(False)
    
    def update(self):
        if not self.playing:
            return
            
        self.all_sprites.update()
        
        current_time = pygame.time.get_ticks()
        
        # Check if 3 seconds have passed
        if not self.delay_passed and current_time - self.game_start_time > 3000:
            self.delay_passed = True
        
        # Only spawn obstacles after delay
        if self.delay_passed:
            now = pygame.time.get_ticks()
            if now - self.obstacle_timer > SPAWN_RATE + random.randint(-500, 500):
                self.obstacle_timer = now
                new_obstacle = create_random_obstacle()
                self.obstacles.add(new_obstacle)
                self.all_sprites.add(new_obstacle)
        
        # Random butcher quotes
        if random.random() < 0.01:
            self.butcher_quote = random.choice(BUTCHER_QUOTES)
            self.quote_timer = current_time
        
        if current_time - self.quote_timer > 3000:
            self.butcher_quote = ""
        
        # Collision detection
        if pygame.sprite.spritecollide(self.chicken, self.obstacles, False):
            if not self.chicken.ducking or any(obs.rect.height > 30 for obs in self.obstacles):
                self.game_over = True
                self.playing = False
                self.death_message = random.choice(DEATH_MESSAGES)
                self.death_cause = random.choice(DEATH_CAUSES)
        
        # Score
        self.score += 0.1
    
    def draw(self):
        self.screen.fill(SKY_BLUE)
        pygame.draw.rect(self.screen, (139, 69, 19), (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        if self.playing:
            self.all_sprites.draw(self.screen)
            score_text = self.font.render(f"Score: {int(self.score)}", True, BLACK)
            self.screen.blit(score_text, (20, 20))
            
            if self.butcher_quote:
                quote_text = self.small_font.render(self.butcher_quote, True, (150, 0, 0))
                pygame.draw.rect(self.screen, (255, 255, 255), 
                               (SCREEN_WIDTH - quote_text.get_width() - 30, 15, 
                                quote_text.get_width() + 20, 30))
                pygame.draw.rect(self.screen, (0, 0, 0), 
                               (SCREEN_WIDTH - quote_text.get_width() - 30, 15, 
                                quote_text.get_width() + 20, 30), 2)
                self.screen.blit(quote_text, (SCREEN_WIDTH - quote_text.get_width() - 20, 20))
        
        elif self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            message_text = self.font.render(self.death_message, True, BLACK)
            cause_text = self.small_font.render(f"Reason: {self.death_cause}", True, BLACK)
            score_text = self.font.render(f"Final Score: {int(self.score)}", True, BLACK)
            restart_text = self.font.render("Press R to restart", True, BLACK)
            
            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 80))
            self.screen.blit(message_text, (SCREEN_WIDTH//2 - message_text.get_width()//2, 130))
            self.screen.blit(cause_text, (SCREEN_WIDTH//2 - cause_text.get_width()//2, 170))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 210))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 260))
        
        else:
            title_text = self.font.render("CHICKEN RUN", True, BLACK)
            subtitle_text = self.small_font.render("The Great Escape", True, (100, 100, 100))
            controls_text = self.small_font.render("Controls: SPACE=Jump, DOWN=Duck, S=Squawk", True, BLACK)
            start_text = self.font.render("Press ENTER to start", True, BLACK)
            
            self.screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 80))
            self.screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, 120))
            self.screen.blit(controls_text, (SCREEN_WIDTH//2 - controls_text.get_width()//2, 160))
            self.screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, 200))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        
        pygame.quit()