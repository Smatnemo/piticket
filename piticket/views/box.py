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
        self.clicked = False 
        self.released = False 
        self.hovered = False

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

    def handle_events(self, events):
        if self.interactable:
            raise NotImplementedError
        else:
            pass

    def update(self):
        pass

    def copy(self):
        return self

    def draw_text(self, screen):
        for content_surface, pos in self.content_surfaces:
            screen.blit(content_surface, pos)

    def draw_box(self, screen):
        # pass border_color attrite to rect color so the the border line looks like the desired
        # color
        pygame.draw.rect(screen, self.color, self.rect,
                        border_radius=self.border_radius)
        pygame.draw.rect(screen, self.border_color, self.rect, width=self.border,
                        border_radius=self.border_radius)

    def draw(self, screen):
        self.draw_box(screen)
        self.draw_text(screen)
        
# Border_color is not applied
# The color passed to the pygame.draw.rect() method is used to draw a border
# if the border which is the thickness is removed or turned to 0, the box is filled 
# Desired behaviour 
# self.border attribute should be colorable - done
# the color should fill the box - done
# Content should be text or image text

class PopUpBox(Box):
    def __init__(self):
        Box.__init__(self)        
