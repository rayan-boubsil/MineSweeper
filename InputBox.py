import pygame

class InputBox:
    """A graphical input field to let players type their name."""
    def __init__(self, x, y, w, h, text='', label="ENTER NAME:"):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (100, 100, 100)
        self.color_active = (0, 255, 127) # Spring Green
        self.color = self.color_inactive
        self.text = text
        self.label = label
        self.font = pygame.font.SysFont("Consolas", 30)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text # Return the name when ENTER is pressed
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Limit name length to 10 characters
                    if len(self.text) < 10:
                        self.text += event.unicode
        return None

    def draw(self, screen):
        # Draw the Label above the box
        label_surf = self.font.render(self.label, True, (200, 200, 200))
        screen.blit(label_surf, (self.rect.x, self.rect.y - 35))
        
        # Render the current text.
        txt_surface = self.font.render(self.text, True, (255, 255, 255))
        # Resize the box if the text is too long (optional)
        width = max(200, txt_surface.get_width()+10)
        self.rect.w = width
        # Blit the text.
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)