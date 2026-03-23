import random
import pygame

class Particle:
    """A single floating dust particle for the menu background."""
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.reset()

    def reset(self):
        """Re-initialize particle at a random position with random speed."""
        self.x = random.randint(0, self.screen_w)
        self.y = random.randint(0, self.screen_h)
        self.size = random.uniform(1, 3)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.speed_y = random.uniform(-0.5, 0.5)
        self.alpha = random.randint(50, 150) # Transparency
        self.fade_speed = random.uniform(0.2, 0.8)

    def update(self):
        """Move the particle and handle fading."""
        self.x += self.speed_x
        self.y += self.speed_y
        self.alpha -= self.fade_speed
        
        # If particle is invisible or off-screen, reset it
        if self.alpha <= 0 or not (0 <= self.x <= self.screen_w and 0 <= self.y <= self.screen_h):
            self.reset()

    def draw(self, surface):
        """Draw a semi-transparent circle."""
        # Create a small surface for per-pixel alpha
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (0, 255, 127, int(self.alpha)), (self.size, self.size), self.size)
        surface.blit(s, (self.x, self.y))