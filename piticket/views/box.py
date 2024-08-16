import pygame 
import time
import itertools
import os.path as osp
from PIL import Image
from piticket.pictures import get_pygame_image, get_gifs
from piticket.utils import multiline_text_to_surfaces

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

    def __init__(self, parent:object,
                x:int, y:int, 
                width:int, height:int,
                position:str, 
                margin:int, padding:int,                 
                border:int, border_radius:int,
                border_color:tuple,
                content:str, content_color:tuple,
                color:tuple,  interactable:bool):
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
        :attr parent: parent must implement a get_rect method to recturn a pygame.Rect object
                    parent must be set at initialization
        :type parent: object
        """
        self.parent = parent
        self.margin = margin 
        # Pass a tuple and create a pygame Rect: check setter
        self.rect = (x,y,width,height)
        # Set these after creating pygame Rect
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height 
        
        # Call the position property method to validate and set value
        self.position = position
        self.color = color
        self.padding = padding 
        self.border = border 
        self.border_radius = border_radius
        self.border_color = border_color
        
        self.content = content
        self.content_color = content_color
        self.content_surfaces = []

        self.interactable = interactable
        self._clicked = False 
        self._released = False 
        self._hovered = False

        # save screen color
        self.screen_color = None 

        # if box has parent and position set, change the position of the box based on value of position
        self.position_box()
    
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self,parent):
        if not parent and not hasattr(parent, 'get_rect'):
            raise Exception(f'{parent} is not a valid parent. Please provide valid pygame.Surface or Box object as parent')
        # parent must have the attribute of get_rect, this object or a pygame.Surface object
        self._parent = parent

    @property 
    def rect(self):
        return self._rect 
    
    @rect.setter 
    def rect(self, rect):
        """ Validate and set rectangle
        :param rect: rectangle coordinates 
        :type rect: tuple
        """
        if not isinstance(rect,(tuple,list)):
            raise ValueError(f'{rect} must be tuple or list.')
        assert len(rect) == 4, 'Length of tuple must be 4'
        # Child rect without margin
        self._rect = pygame.Rect(rect)

    @property
    def position(self):
        """Return position value: getter"""
        return self._position

    @position.setter
    def position(self, pos):
        """Set position value: setter"""
        if pos not in self.POSITIONS:
            raise ValueError(f'Choose valid value from POSITIONS - {self.POSITIONS}')
        self._position = pos 


    @property 
    def padding(self):
        """Get the value of padding"""
        return self._padding

    @padding.setter
    def padding(self, padding):
        """Set the value of padding"""
        if padding not in [None,*range(0,min(self.rect.width,self.rect.height)//2,1)]:
            raise ValueError(f'{padding} is not a valid value for padding')
        self._padding = padding

    def get_rect(self):
        return self.rect 

    def get_at(self, pixel_coord):
        if isinstance(pixel_coord,(tuple,list)):
            assert len(pixel_coord) == 2, "Pixel coordinates should be 2"
            return self.color

    def change_xy(self, coord):
        """Change the position of the box using x, y coordinates and 
        change the coordinates of the content as well
        """
        assert len(coord) == 2, "Coord must be 2"
        # Check that content is within the box
        assert self.rect.collidepoint(coord), "Coord must be within the "

    def position_box(self):
        """Position current Box within parent Box using the position attribute"""
        parent_rect = self.parent.get_rect()
        if self.position:
            width = self.rect.width
            if self.position.endswith('left'):
                self.rect.x = parent_rect.left
            elif self.position.endswith('center'):
                self.rect.x = parent_rect.centerx - width//2
            elif self.position.endswith('right'):
                self.rect.x = parent_rect.right - width
                
            height = self.rect.height
            if self.position.startswith('top'):
                self.rect.y = parent_rect.top
            elif self.position.startswith('center'):
                self.rect.y = parent_rect.centery - height//2
            elif self.position.startswith('bottom'):
                self.rect.y = parent_rect.bottom - height
            
            if self.__class__.__name__ == 'PopUpBox':
                print(parent_rect.bottom)
                print(self.rect)
                # exit()dfs

        elif not self.position:
            # if only parent exists, tranlate x and y positions to fit the positions of the parent
            self.rect.x = parent_rect.x + self.rect.x
            self.rect.y = parent_rect.y + self.rect.y

        # Check that the margins + box dimensions are within the parent
        try:
            assert parent_rect.collidepoint((self.rect.x,
                                self.rect.y)), f'Coordinates x:{self.rect.x}, y:{self.rect.y} must be within the parent dimensions {parent_rect.x}, {parent_rect.y}, {parent_rect.width}, {parent_rect.height}'
            assert parent_rect.collidepoint((self.rect.x+self.rect.width, 
                                    self.rect.y+self.rect.height)),f'Coordinates {self.rect.x+self.rect.width}, {self.rect.y+self.rect.height} for bottom-right must be within the parent {parent_rect.x}, {parent_rect.y}, {parent_rect.width}, {parent_rect.height}' 
        except AssertionError as ex:
            if self.rect.x+self.rect.width==parent_rect.width or self.rect.y+self.rect.height==parent_rect.height:
                pass
            else:
                raise AssertionError(ex)
        self.position_text()

    def position_text(self, align='center'):
        """Position text within Box. Possible align values are in self.POSITIONS
            and class attributes.
        
        :param align: position box within the rect
        :type align: str
        """
        # Maximum padding value should not be greater that min(width, height)//2 as ensured in the padding setter
        if self.padding:
            rect = self.rect.inflate(-2*self.padding, -2*self.padding)
        elif not self.padding:
            rect = self.rect
        else:
            return
        if self.content is not None:
            if not osp.isfile(self.content):
                self.content_surfaces = multiline_text_to_surfaces(self.content, 
                                                            self.content_color, 
                                                            rect, 
                                                            align=align)
            else:
                surface = get_pygame_image(self.content, size=(rect.width, rect.height), color=None)
                self.content_surfaces = [(surface,surface.get_rect(center=self.rect.center))]
        

    def _draw_text(self, screen):
        # By default, content surface must always be in the center of the box
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
        # # Draw external box with margin
        # rect_with_margin = self.rect.inflate(2*self.margin,2*self.margin)
        # pygame.draw.rect(screen, self.screen_color, rect_with_margin,)
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
        if self.screen_color:
            screen.fill(self.screen_color,rect=self.rect)
        else:
            screen.fill((0,0,0))

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
        Box.__init__(self, parent,
                    x, y,
                    width, height, 
                    position,
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

    
class PopUpBox(Box):
    def __init__(self, parent=None,
                x=0, y=0,
                width=300, height=200,
                position='bottom-center',
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content='Would you like to continue?',
                content_color=(255,255,255),
                color=(133,133,133),
                interactable=False,
                timeout=10):
        """:param timeout: how long the pop up box should remain on the screen
           :type timeout: int"""
        # Marks the beginning
        self._started = True 
        # For timeout
        self._start_time = time.time()
        self._end_time = timeout + self._start_time
        self._timeout = timeout
        self._timeout_text = ''

        self._content = content

        Box.__init__(self, 
                parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, color,
                interactable)

        # Marks the end of the popupbox execution circle when True
        self._triggered = False
        self._triggered_callback_func = None
        self._triggered_callback_args = None 
        self._triggered_callback_kwargs = None

        # Initialize and position buttons
        self.btn1 = Button(content='Yes',parent=self)
        self.btn2 = Button(content='No',parent=self)
        self.position_buttons()
    
    def handle_events(self,event):
        if not event:
            return 
        
    def triggered(self, func, *args, **kwargs):
        self._triggered_callback_func = func 
        self._triggered_callback_args = args 
        self._triggered_callback_kwargs = kwargs

    def position_text(self, align='top-center'):
        # Keep creating text surfaces for timer
        self._timeout_text = f'App will lock in {int(self._end_time-self._start_time)} seconds.\n'
        if self._end_time - self._start_time < 0:
            self._started = False
            self._triggered = True
        self.content = self._timeout_text + self._content
        Box.position_text(self, align)
        # Get time for next loop
        self._start_time = time.time()

    def position_buttons(self):
        # Calculate the center coordinates
        x,y = self.rect.center
        if hasattr(self,'btn1'):
            self.btn1.rect.x = x - self.btn1.rect.width - self.btn1.margin 
            self.btn1.rect.y = y
            # Reposition text
            self.btn1.position_text()
        if hasattr(self,'btn2'):
            self.btn2.rect.x = self.btn2.margin + x
            self.btn2.rect.y = y
            # Reposition text
            self.btn2.position_text()

    def update(self, event, screen):
        # Recreate and reposition text surfaces
        self.position_text()
        if self._started:
            self.draw(screen)
            # Draw and handle events of buttons
            # after drawing pop up box on screen
            self.btn1.update(event,screen)
            self.btn2.update(event,screen)
        if self._triggered:
            if self._triggered_callback_func:
                self._triggered_callback_func(*self._triggered_callback_args,
                                            **self._triggered_callback_kwargs)
            self.clear(screen)


class PopUpBoxProcessing(Box):
    def __init__(self, event,
                parent=None, x=0, y=0,
                width=300, height=200,
                position='center',
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content='Processing',
                content_color=(255,255,255),
                color=(133,133,133),
                interactable=False,
                gif_image=None):
        """:param gif_name: the name of the folder with gif frames.
           :type gif_name: str
           :param event: specific event to respond to
           :type event: pygame.event.Event
        """
        self.event = event 
        self.gif_image = gif_image

        Box.__init__(self, 
                parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, color,
                interactable)
        # Marks the beginning
        self._started = True 
        # Marks the end of the processing circle
        self._triggered = False
        self._triggered_callback_func = None
        self._triggered_callback_args = None 
        self._triggered_callback_kwargs = None

    @property 
    def gif_image(self):
        return self._gif_image 

    @gif_image.setter
    def gif_image(self, gif_folder_name):
        """Use folder name to return a generator of gif frame names
        """
        self._gif_image = itertools.cycle(get_gifs(gif_folder_name)) 

    def triggered(self, func, *args, **kwargs):
        self._triggered_callback_func = func 
        self._triggered_callback_args = args 
        self._triggered_callback_kwargs = kwargs

    def handle_events(self,event):
        if not event:
            return
        # if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(event.pos):
        #     self._released = True 
        if event.type == self.event.type:
            self._triggered = True
            self._started = False

    def position_text(self,align='top-center'):
        Box.position_text(self,align=align)

    def position_gif(self, image_surface, position='bottom-center'):
        """
        """
        x, y = self.rect.x,self.rect.y
        if position:
            width = image_surface.get_rect().width
            if position.endswith('left'):
                x = self.rect.left
            elif position.endswith('center'):
                x = self.rect.centerx - width//2
            elif position.endswith('right'):
                x = self.rect.right - width
            else:
                raise ValueError(f'Invalid argument {position}. Choose from {self.POSITIONS}')
            
            height = image_surface.get_rect().height
            if position.startswith('top'):
                y = self.rect.top 
            elif position.startswith('center'):
                y = self.rect.centery - height//2
            elif position.startswith('bottom'):
                y = self.rect.bottom - height
            else:
                raise ValueError(f'Invalid argument {position}. Choose from {self.POSITIONS}')
        return x, y

    def draw(self, screen):
        Box.draw(self,screen)
        img = next(self.gif_image) 
        im = get_pygame_image(img,color=None,size=(150,19950))
        screen.blit(im,self.position_gif(im))
        
    def update(self, event, screen):
        self.handle_events(event)
        if self._started:
            # Draw pop up box on screen
            self.draw(screen)
        if self._triggered:
            # Use triggered to execute callback function just once
            self.clear(screen)
            # Execute any callback functions if any
            if self._triggered_callback_func:
                self._triggered_callback_func(*self._triggered_callback_args,
                                            **self._triggered_callback_kwargs)
            self._triggered = False
        
        
class Header(Box):
    def __init__(self, parent=None, 
                x=0, y=0, width=None, 
                height=80, 
                margin=20, padding=10,
                border=1, border_radius=0,
                border_color=(0,0,0),
                content=None,
                content_color=(255,255,255),
                color=(133,133,133),
                interactable=False):

        position=self.TOPLEFT

        if not width:
            width = parent.get_rect().width

        Box.__init__(self,
                parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, color,
                interactable)

class Footer(Box):
    def __init__(self,parent=None, 
                x=0, y=0, width=None, 
                height=80, 
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content=None,
                content_color=(255,255,255),
                color=(133,133,133),
                interactable=False):

        position=self.BOTTOMLEFT
        if not width:
            width = parent.get_rect().width

        Box.__init__(self,parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, color,
                interactable)
        

class LeftSideBar(Box):
    def __init__(self,parent=None, 
                x=0, y=0, width=80, 
                height=None, 
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content=None,
                content_color=(255,255,255),
                color=(133,133,133),
                interactable=False):

        position=self.TOPLEFT 
        if not height:
            height = parent.get_rect().height

        Box.__init__(self,
                parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, color,
                interactable)

class RightSideBar(Box):
    def __init__(self,parent=None, 
                x=0, y=0, width=80, 
                height=None, 
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content=None,
                content_color=(255,255,255),
                color=(133,133,133),
                interactable=False):

        position=self.TOPRIGHT
        if not height:
            height = parent.get_rect().height

        Box.__init__(self,
                parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, color,
                interactable)
        

