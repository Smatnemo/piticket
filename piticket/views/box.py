import pygame 
import os.path as osp 
from piticket.pictures import get_pygame_image
from piticket.views.background import multiline_text_to_surfaces

class Box:
    def __init__(self, x:int, y:int, 
                width:int, height:int, 
                margin:int, padding:int,                 
                border:int, border_radius:int,
                border_color:tuple,
                content:str, content_color:tuple,
                color:tuple, interactable:bool):
        """Generic base box class for all box elements to be implemented
        in the app.
        :attr rect: a rectangle of dimensions x, y, width and height
        :type rect: pygame.Rect
        :attr margin: the gap between the box and outer elements
        :type margin: int
        :attr padding: the gap between a border and the content of the box
        :type padding: int
        :attr border: the thickness of the box outer line
        :type border: int
        :attr border_radius: the curve around the edges of the box
        :type border_radius: int
        :attr border_color: the color of the border
        :type border_color: tuple or list
        :attr content: the content in the box either text or image
        :type content: str
        :attr color: the color of the box
        :type color: tuple or list
        :attr content_color: the color of the text if text is the content. No color if image is content
        :type content_color: tuple or list
        :attr screen: the screen surface before a button is added
        :type screen: pygame.Surface
        """
        self.rect = pygame.Rect((x,y,width,height))
        self.color = color
        self.margin = margin 
        self.padding = padding 
        self.border = border 
        self.border_radius = border_radius
        self.border_color = border_color
        
        self.content = content
        self.content_color = content_color

        self.interactable = interactable
        self._clicked = False 
        self._released = False 
        self._hovered = False

        # Maximum padding value should not be greater that min(width, height)//2
        if self.padding != 0 and self.padding in list(range(1,min(width, height)//2,1)):
            rect = self.rect.inflate(-2*self.padding, -2*self.padding)
        elif self.padding == 0:
            rect = self.rect
        else:
            raise ValueError(f"Padding value {self.padding} is out of range. padding must be greater than or equal to 0 and less than {min(width, height)//2}")

        if not osp.isfile(self.content):
            self.content_surfaces = multiline_text_to_surfaces(self.content, 
                                                        self.content_color, 
                                                        rect, 
                                                        align='center')
        else:
            surface = get_pygame_image(self.content, size=(rect.width, rect.height))
            self.content_surfaces = [(surface,surface.get_rect(center=self.rect.center))]

        self.screen_color = None 

    def _draw_text(self, screen):
        for content_surface, pos in self.content_surfaces:
            screen.blit(content_surface, pos)

    def _draw_box(self, screen, color=None, border_color=None):
        """
        :param screen: the pygame surface to draw on
        :type screen: pygame.Surface
        :param interaction: draw the box based on the interaction such as clicked, released, hovered
        :type interation: str
        """
        if not color:
            color = self.color 
        if not border_color:
            border_color = self.border_color 
        
        # Draw box with box self.color
        pygame.draw.rect(screen, color, self.rect,
                        border_radius=self.border_radius)
        # Draw transparent box with only borders with color of self.border_color
        pygame.draw.rect(screen, border_color, self.rect, width=self.border,
                        border_radius=self.border_radius)
        
    
    def _draw_clicked_box(self):
        if self.interactable:
            raise NotImplementedError
        else:
            pass
    
    def _draw_released_box(self):
        if self.interactable:
            raise NotImplementedError
        else:
            pass 
    
    def _draw_hovered_box(self):
        if self.interactable:
            raise NotImplementedError
        else:
            pass

    def handle_events(self, events):
        if self.interactable:
            raise NotImplementedError
        else:
            pass

    def update(self, event, screen):
        pass

    def copy(self):
        return self

    def draw(self, screen):
        # Create a copy of the screen before drawing on the screen
        self.screen_color = screen.get_at((self.rect.x,self.rect.y))
        # Draw on the screen after preserving a copy
        self._draw_box(screen)
        self._draw_text(screen)

    def clear(self, screen):
        screen.fill(self.screen_color,rect=self.rect)

class PopUpBox(Box):
    def __init__(self):
        Box.__init__(self)        
