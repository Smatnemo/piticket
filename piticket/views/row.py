import pygame
from piticket.views.box import Box, Button
from piticket.utils import multiline_text_to_surfaces
from piticket.location import location

class Row(Button):

    def __init__(self, parent,
                width, height,
                color=(255,255,255), 
                additional_color=(208, 240, 192),
                row=(),
                event=None):
            
        Button.__init__(self, parent=parent,x=0, y=0,
                width=width, height=height,
                position='center', margin=10, padding=10,
                border=2, border_radius=15,
                border_color=(253, 255, 0),
                content=list(row), content_color=(255,255,255),
                content_position='top-left',
                color=color, clicked_color=(0,191,0),
                clicked_border_color=(0,127,0),
                hovered_color=(0,127,0),
                hovered_border_color=(253, 255, 0))
        
        self.chosen = False
        self.additional_color = additional_color


    def position_content(self, rect=None, align=None):
        content_surfaces = []
        if self.content is not None:
            # First item top-left
            rect = pygame.Rect((self.rect.x,self.rect.y,self.rect.width,40))
            content_surfaces=Button.position_content(self, rect=rect, content=location+' - '+self.content[0],align=self.TOPLEFT)
            content_surfaces.extend(Button.position_content(self, rect=rect, content=self.content[1],align=self.TOPRIGHT))
            rect = pygame.Rect((self.rect.x,self.rect.y+rect.height-self.padding,self.rect.width,35))
            content_surfaces.extend(Button.position_content(self, rect=rect, content=self.content[2],align=self.BOTTOMLEFT))
        self.content_surfaces = content_surfaces

    def draw(self, screen):
        Button.draw(self,screen)
        # Draw box on half the original box at the bottom part
        if self.additional_color:
            # change y coordinate of the rectangle and use half the height
            # Use copy method otherwise it is a reference to the same object
            rect = self._rect.copy()
            rect.height = rect.height/3 - self.border
            rect.width = rect.width - 2*self.border
            rect.y = rect.y + self.rect.height*2/3  + 2 * self.border
            rect.x = self.rect.x + self.border
            pygame.draw.rect(screen, self.additional_color, rect, border_bottom_left_radius=self.border_radius, border_bottom_right_radius=self.border_radius)
        

class RowView(Box):
    def __init__(self, parent,
                x, y, width, height, 
                position, margin,
                padding, border, border_radius,
                border_color, content,
                content_color, content_position,
                color, interactable=False, rows:dict={}):

        Box.__init__(self, parent, 
                x, y, width, height,
                position, margin, padding,
                border, border_radius,
                border_color, content,
                content_color, content_position,
                color, interactable)
        self.offset = 5
        self.start = 0
        self.end = self.start+self.offset 
        # rows is a dictionary. pass only key which is a tuple
        # Calculate width, height for each row based on the dimensions of the view, which 
        # which is the parent of the rows created below
        width = width
        height = height//self.offset
        self.row_boxes = [Box(parent=self, x=0, y=i*height, 
                            width=width, height=height,
                            position=None, margin=0, 
                            padding=padding, border=border, 
                            border_radius=border_radius,
                            border_color=border_color,
                            content=None, content_color=(0,0,0),
                            content_position='center',
                            color=color,  interactable=False) for i, row in enumerate(rows)]

        self.rows = [Row(parent=row_box,
                        width=width-margin,
                        height=height-margin,
                        color=(0, 106, 78),
                        row=row) for row_box, row in zip(self.row_boxes, rows)]
        # post event when clicked
        for row in self.rows:
            row.clicked(pygame.event.post, pygame.event.Event(pygame.MOUSEBUTTONUP,state='chosen',choice=tuple(row.content)))
        self.chosen_row = None

    def update(self, event, screen):
        Box.draw(self, screen)
        # position and draw parent boxes for each row
        for row in self.row_boxes:
            row.draw(screen)
        # Draw clickable button for each row
        for row in self.rows:
            row.update(event, screen)
