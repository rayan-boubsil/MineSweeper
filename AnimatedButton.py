import pygame

class AnimatedButton:
    """A button that grows and changes color smoothly when hovered."""
    def __init__(self, x, y, w, h, text, callback):
        self.base_rect = pygame.Rect(x, y, w, h)
        self.current_rect = pygame.Rect(x, y, w, h) # The one that scales
        self.text = text
        self.callback = callback
        
        # Colors (R, G, B)
        self.base_color = pygame.Color(45, 45, 55)
        self.target_color = pygame.Color(0, 255, 127) # Spring Green
        self.current_color = pygame.Color(45, 45, 55)
        
        self.font = pygame.font.SysFont("Verdana", 24, bold=True)
        self.scale_factor = 1.0 # 1.0 = 100% size
        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.base_rect.collidepoint(mouse_pos)
        
        # 1. SCALE ANIMATION (Target is 1.1x if hovered, else 1.0x)
        target_scale = 1.1 if self.is_hovered else 1.0
        # Lerp formula: current + (target - current) * speed
        self.scale_factor += (target_scale - self.scale_factor) * 0.2
        
        # Update the visual rect based on scale
        new_w = self.base_rect.w * self.scale_factor
        new_h = self.base_rect.h * self.scale_factor
        # Keep it centered on the original position
        self.current_rect = pygame.Rect(0, 0, new_w, new_h)
        self.current_rect.center = self.base_rect.center

        # 2. COLOR ANIMATION (Lerping R, G, B values)
        goal_color = self.target_color if self.is_hovered else self.base_color
        # Smoothly transition each RGB channel
        r = self.current_color.r + (goal_color.r - self.current_color.r) * 0.1
        g = self.current_color.g + (goal_color.g - self.current_color.g) * 0.1
        b = self.current_color.b + (goal_color.b - self.current_color.b) * 0.1
        self.current_color = pygame.Color(int(r), int(g), int(b))

    def draw(self, screen):
        # Draw shadow for depth
        shadow_rect = self.current_rect.copy()
        shadow_rect.move_ip(3, 3)
        pygame.draw.rect(screen, (10, 10, 10), shadow_rect, border_radius=12)
        
        # Draw main button
        pygame.draw.rect(screen, self.current_color, self.current_rect, border_radius=12)
        
        # Border
        border_col = (255, 255, 255) if self.is_hovered else (80, 80, 80)
        pygame.draw.rect(screen, border_col, self.current_rect, 2, border_radius=12)
        
        # Text scaling
        temp_font = pygame.font.SysFont("Verdana", int(24 * self.scale_factor), bold=True)
        text_surf = temp_font.render(self.text, True, (255, 255, 255) if not self.is_hovered else (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.current_rect.center)
        screen.blit(text_surf, text_rect)

    def handle_click(self):
        if self.is_hovered:
            self.callback()