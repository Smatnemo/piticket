import pygame 
import os.path as osp
from piticket.pictures import get_pygame_image
from piticket.views.background import multiline_text_to_surfaces

class Box:
    TOPLEFT = 'top-left'
    TOPCENTER = 'top-center'
    TOPRIGHT = 'top-right'
    CENTERLEFT = 'center-left'
    CENTER = 'center'
    CENTERRIGHT = 'center-right'
    BOTTOMLEFT = 'bottom-left'
    BOTTOMCENTER = 'bottom-center'
    BOTTOMRIGHT = 'bottom-right'
    POSITIONS = [TOPLEFT, TOPCENTER, TOPRIGHT, CENTERLEFT, CENTER, 
                CENTERRIGHT, BOTTOMLEFT, BOTTOMCENTER, BOTTOMRIGHT, None]

    def __init__(self, x:int, y:int, 
                width:int, height:int,
                position:str, 
                margin:int, padding:int,                 
                border:int, border_radius:int,
                border_color:tuple,
                content:str, content_color:tuple,
                color:tuple,  interactable:bool,
                parent:object=None):
        """Generic base box class for all box elements to be implemented
        in the app.
        :attr rect: a rectangle of dimensions x, y, width and height
        :type rect: pygame.Rect
        :attr position: the position of the box on the pygame surface. Choose value from POSITIONS
                        It can be None.
        :type position: str
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
        :attr parent: parent must implement a get_rect method to recturn
        :type parent: object
        """
        self.rect = pygame.Rect((x,y,width,height))
        # Call the position property method to validate and set value
        self.position = position
        self.color = color
        self.margin = margin 
        self.padding = padding 
        self.border = border 
        self.border_radius = border_radius
        self.border_color = border_color
        
        self.content = content
        self.content_color = content_color
        
        self.parent = parent

        self.interactable = interactable
        self._clicked = False 
        self._released = False 
        self._hovered = False

        # save screen color
        self.screen_color = None 

        # if box has parent and position set, change the position of the box based on value of position
        self.position_box()
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

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        if pos not in self.POSITIONS:
            raise ValueError(f'Choose valid value from POSITIONS - {self.POSITIONS}')
        self._position = pos 

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self,parent):
        if not parent or hasattr(parent,'get_rect'):
            self._parent = parent

    def get_rect(self):
        return self.rect 

    def get_at(self, pixel_coord):
        if isinstance(pixel_coord,(tuple,list)):
            assert len(pixel_coord) == 2, "Pixel coordinates should be 2"
            return self.color

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

    def clicked(self, func, *args, **kwargs):
        """Save a function to execute when the button is released
        """
        if self.interactable:
            raise NotImplementedError 
        else:
            pass

    def hovered(self, func, *args, **kwargs):
        """"""
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

    def position_box(self):
        """Position current item within parent item using"""
        if self.parent:
            if self.position:
                width = self.rect.width
                if self.position.endswith('left'):
                    self.rect.x = self.parent.get_rect().left
                elif self.position.endswith('center'):
                    self.rect.x = self.parent.get_rect().centerx - width//2
                elif self.position.endswith('right'):
                    self.rect.x = self.parent.get_rect().right - width
                    
                height = self.rect.height
                if self.position.startswith('top'):
                    self.rect.y = self.parent.get_rect().top
                elif self.position.startswith('center'):
                    self.rect.y = self.parent.get_rect().centery - height//2
                elif self.position.startswith('bottom'):
                    self.rect.y = self.parent.get_rect().bottom - height

            elif not self.position:
                # if only parent exists, tranlate x and y positions to fit the positions of the parent
                self.rect.x = self.parent.get_rect().x + self.rect.x
                self.rect.y = self.parent.get_rect().y + self.rect.y

    def draw(self, screen):
        # Get the color of the screen or parent
        if self.parent:
            self.screen_color = self.parent.get_at((self.parent.get_rect().x,self.get_rect().y))
        else:
            self.screen_color = screen.get_at((self.rect.x,self.rect.y))
        # Draw on the screen after preserving a copy
        self._draw_box(screen)
        self._draw_text(screen)

    def clear(self, screen):
        screen.fill(self.screen_color,rect=self.rect)

class Button(Box):
    def __init__(self, x=0, y=0,
                width=100, height=60,
                position='center',
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content='Button',
                content_color=(255,255,255),
                color=(133,133,133),
                clicked_color=(60,60,60),
                clicked_border_color=(255,255,255),
                hovered_color=(140,127,127),
                hovered_border_color=(90,90,90),
                parent=None):
        # Button must be interactable
        interactable=True
        Box.__init__(self, x, y,
                    width, height, 
                    position,
                    margin, padding,
                    border, border_radius,
                    border_color,
                    content, 
                    content_color,
                    color,
                    interactable,
                    parent)
        self.clicked_color = clicked_color 
        self.clicked_border_color = clicked_border_color 
        self.hovered_color = hovered_color
        self.hovered_border_color = hovered_border_color

        self._clicked_callback_func = None
        self._clicked_callback_args = None
        self._clicked_callback_kwargs = None
        self._hovered_callback_func = None
        self._hovered_callback_args = None 
        self._hovered_callback_kwargs = None

    def _draw_clicked_box(self, screen):
        Box._draw_box(self, screen, self.clicked_color, self.clicked_border_color)

    def _draw_released_box(self, screen):
        # Released box is normal box
        Box._draw_box(self, screen)

    def _draw_hovered_box(self, screen):
        Box._draw_box(self, screen, self.hovered_color, self.hovered_border_color)

    def clicked(self, func, *args, **kwargs):
        self._clicked_callback_func = func
        self._clicked_callback_args = args 
        self._clicked_callback_kwargs = kwargs

    def hovered(self, func, *args, **kwargs):
        self._hovered_callback_func = func 
        self._hovered_callback_args = args 
        self._hovered_callback_kwargs = kwargs

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
        if self._released and self._clicked_callback_func:
            self._clicked_callback_func(*self._clicked_callback_args,
                                        **self._clicked_callback_kwargs)
        self._released = False

        if self._hovered:
            if self._hovered_callback_func:
                self._hovered_callback_func(*self._hovered_callback_args,
                                        **self._hovered_callback_kwargs)
                

    def draw(self, screen):
        if self._clicked:
            self._draw_clicked_box(screen)
            self._draw_text(screen)
        elif self._hovered:
            self._draw_hovered_box(screen)
            self._draw_text(screen)
        else:
            Box.draw(self, screen)

        # pygame.display.update()
        # Allow time for effect to be seen
        # pygame.time.wait(100)


    
class PopUpBox(Box):
    def __init__(self, x=0, y=0,
                width=300, height=200,
                position='center',
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content='PopUpBox',
                content_color=(255,255,255),
                color=(133,133,133),
                interactable=False,
                parent=None):
        Box.__init__(self, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, color,
                interactable, parent)

        # self.btn3 = Button(content='One',position=self.BOTTOMLEFT,parent=self)
        self.btn1 = Button(content='No',position=self.BOTTOMRIGHT,parent=self)
        self.btn2 = Button(content='Yes',position=self.TOPRIGHT,parent=self)

    def update(self, event, screen):
        self.draw(screen)
        self.btn2.update(event, screen)
        self.btn1.update(event, screen)
        # self.btn3.update(event, screen)

class PopUpBoxProcessing(Box):
    def __init__(self):
        pass


