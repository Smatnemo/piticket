import pygame
from piticket.views.box import Box 

class Button(Box):
    def __init__(self, x=0, y=0,
                width=100, height=60,
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content='Button',
                content_color=(255,255,255),
                color=(133,133,133),
                interactable=True,
                clicked_color=(60,60,60),
                clicked_border_color=(255,255,255),
                hovered_color=(140,127,127),
                hovered_border_color=(90,90,90)):
        Box.__init__(self, x, y,
                    width, height, 
                    margin, padding,
                    border, border_radius,
                    border_color,
                    content, 
                    content_color,
                    color,
                    interactable)
        self.clicked_color = clicked_color 
        self.clicked_border_color = clicked_border_color 
        self.hovered_color = hovered_color
        self.hovered_border_color = hovered_border_color

    def _draw_clicked_box(self, screen):
        Box._draw_box(self, screen, self.clicked_color, self.clicked_border_color)

    def _draw_released_box(self, screen):
        # Released box is normal box
        Box._draw_box(self, screen)

    def _draw_hovered_box(self, screen):
        Box._draw_box(self, screen, self.hovered_color, self.hovered_border_color)

    def handle_events(self, event):
        if not event:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self._clicked = True
            self._hovered = False
            self._released = False
        elif event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
            self._released = True 
            self._clicked = False
            self._hovered = False
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self._hovered = True
            elif not self.rect.collidepoint(event.pos):
                self._hovered = False
            self._released = False 
            self._clicked = False
    
    def update(self, event, screen):
        self.handle_events(event)
        self.draw(screen)

    def draw(self, screen):
        if self._clicked:
            self._draw_clicked_box(screen)
            self._draw_text(screen)
        elif self._hovered:
            self._draw_hovered_box(screen)
            self._draw_text(screen)
        else:
            Box.draw(self, screen)

        pygame.display.update()
        # Allow time for effect to be seen
        pygame.time.wait(100)


    