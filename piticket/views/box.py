import pygame 
import time
import itertools
import os.path as osp
from PIL import Image
from datetime import datetime
from piticket.pictures import get_pygame_image, get_gifs
from piticket.utils import multiline_text_to_surfaces
from piticket.location import locator


def create_content_surface(*images,rect=None,align='center'):
    """Return a list of tuples(pygame surface, rect)
    :param images: surface with an image
    :type images: pygame.Surface
    :param rect: rect in which to position content
    :type rect: pygame.Rect
    :param align: where to position it in the rect
    :type align: str
    """
    surfaces = []
    for image in images:
        width = image.get_rect().width
        if align.endswith('left'):
            x = rect.left
        elif align.endswith('center'):
            x = rect.centerx - width//2
        elif align.endswith('right'):
            x = rect.right - width
        else:
            raise ValueError(f'{aign} value is wrong')

        height = image.get_rect().height
        if align.startswith('top'):
            y = rect.top
        elif align.startswith('center'):
            y = rect.centery - height//2
        elif align.startwith('bottom'):
            y = rect.bottom - height
        else:
            raise ValueError(f'{align} value is wrong')
        surfaces.append((image,image.get_rect(x=x,y=y)))
    return surfaces

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
                content_position: str,
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
        self.content_surfaces = []
        self.content_color = content_color
        self.content_position = content_position

        self.interactable = interactable
        self._clicked = False 
        self._released = False 
        self._hovered = False

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
        self.position_content()

    def position_content(self):
        """Position content within Box. Possible align values are in self.POSITIONS
            and class attributes.
        """
        # Maximum padding value should not be greater that min(width, height)//2 as ensured in the padding setter
        if self.padding:
            rect = self.rect.inflate(-2*self.padding, -2*self.padding)
        elif not self.padding:
            rect = self.rect
        else:
            return
        if self.content:
            if not osp.isfile(self.content):
                self.content_surfaces = multiline_text_to_surfaces(self.content, 
                                                            self.content_color, 
                                                            rect, 
                                                            align=self.content_position)
            else:
                surface = get_pygame_image(self.content, size=(rect.width, rect.height), color=None)
                self.content_surfaces = create_content_surface(surface,rect=rect,align=self.content_position)

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
        
        # Draw box with box self.color
        pygame.draw.rect(screen, color, self.rect,
                        border_radius=self.border_radius)
        # Draw transparent box with only borders with color of self.border_color
        if self.border and self.border_color:
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
        # Draw on the screen after preserving a copy
        self._draw_box(screen)
        self._draw_text(screen)

class Button(Box):
    def __init__(self, x=0, y=0,
                width=100, height=60,
                position='center',
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content='Button',
                content_color=(255,255,255),
                content_position='center',
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
                    content_position,
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
        """Set callback function when the button is clicked and released
        """
        self._clicked_callback_func = func
        self._clicked_callback_args = args 
        self._clicked_callback_kwargs = kwargs

    def hovered(self, func, *args, **kwargs):
        """Set callback function when the button is hovered over. Mainly for a function
        that will describe the button's use.
        """
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
                position='center',
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content='Would you like to continue?',
                content_color=(255,255,255),
                content_position='top-center',
                color=(133,133,133),
                interactable=False,
                timeout=10,
                button1_config={'color':(0,191,0),'clicked_color':(0,255,0),'hovered_color':(0,127,0),'content':'Yes'},
                button2_config={'color':(191,0,0),'clicked_color':(255,0,0),'hovered_color':(127,0,0),'content':'No'}):
        """:param timeout: how long the pop up box should remain on the screen
           :type timeout: int"""
        # Marks the beginning
        self.started = True 
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
                content_color, 
                content_position, color,
                interactable)

        # Marks the end of the popupbox execution circle when True
        self._triggered = False
        self._triggered_callback_func = None
        self._triggered_callback_args = None 
        self._triggered_callback_kwargs = None

        # Initialize and position buttons
        self.btn1 = Button(content=button1_config['content'],
                            color=button1_config['color'],
                            clicked_color=button1_config['clicked_color'],
                            hovered_color=button1_config['hovered_color'],
                            parent=self)
        self.btn2 = Button(content=button2_config['content'],
                            color=button2_config['color'],
                            clicked_color=button2_config['clicked_color'],
                            hovered_color=button2_config['hovered_color'],
                            parent=self)
        self.position_buttons()
    
    @property
    def started(self):
        return self._started

    @started.setter
    def started(self, started):
        self._started = started

    def handle_events(self,event):
        if not event:
            return 
        if event.type == pygame.MOUSEBUTTONUP\
            and (self.btn1.rect.collidepoint(event.pos)\
            or self.btn2.rect.collidepoint(event.pos)):
            self.started = False
        
    def triggered(self, func, *args, **kwargs):
        self._triggered_callback_func = func 
        self._triggered_callback_args = args 
        self._triggered_callback_kwargs = kwargs

    def position_content(self):
        # Keep creating text surfaces for timer
        self._timeout_text = f'App will lock in {int(self._end_time-self._start_time)} seconds.\n'
        if self._end_time - self._start_time < 0:
            self.started = False
            self._triggered = True
        self.content = self._timeout_text + self._content
        Box.position_content(self)
        # Get time for next loop
        self._start_time = time.time()

    def position_buttons(self):
        # Calculate the center coordinates
        x,y = self.rect.center
        if hasattr(self,'btn1'):
            self.btn1.rect.x = x - self.btn1.rect.width - self.btn1.margin 
            self.btn1.rect.y = y
            # Reposition text
            self.btn1.position_content()
        if hasattr(self,'btn2'):
            self.btn2.rect.x = self.btn2.margin + x
            self.btn2.rect.y = y
            # Reposition text
            self.btn2.position_content()

    def update(self, event, screen):
        # Recreate and reposition text surfaces
        self.position_content()
        if self.started:
            self.draw(screen)
            # Draw and handle events of buttons
            # after drawing pop up box on screen
            self.btn1.update(event,screen)
            self.btn2.update(event,screen)
            self.handle_events(event)
        if self._triggered:
            if self._triggered_callback_func:
                self._triggered_callback_func(*self._triggered_callback_args,
                                            **self._triggered_callback_kwargs)


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
                content_position='top-center',color=(133,133,133),
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
                content_color, 
                content_position, color,
                interactable)
        # Marks the beginning
        self.started = True 
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

    @property
    def started(self):
        return self._started

    @started.setter
    def started(self, started):
        self._started = started

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
            self.started = False

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
        im = get_pygame_image(img,color=None,size=(150,150))
        screen.blit(im,self.position_gif(im))
        
    def update(self, event, screen):
        self.handle_events(event)
        if self.started:
            # Draw pop up box on screen
            self.draw(screen)
        if self._triggered:
            # Use triggered to execute callback function just once
            # Execute any callback functions if any
            if self._triggered_callback_func:
                self._triggered_callback_func(*self._triggered_callback_args,
                                            **self._triggered_callback_kwargs)
            self._triggered = False
        
        
class Header(Box):
    def __init__(self, parent=None, 
                x=0, y=0, 
                height=80, 
                margin=20, padding=10,
                border=1, border_radius=0,
                border_color=(133,133,133),
                content=None,
                content_color=(255,255,255),
                content_position='center',
                color=(133,133,133),
                interactable=False):

        position=self.TOPLEFT
        width = parent.get_rect().width

        Box.__init__(self,
                parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, 
                content_position, color,
                interactable)

        
        d = datetime.fromtimestamp(time.time())
        self.box = Box(x=0, y=0, 
                        width=200, height=80,
                        position='top-left', 
                        margin=20, padding=10, 
                        border=1, border_radius=10, 
                        border_color=border_color, 
                        content=None, 
                        content_color=(255,255,255), 
                        content_position='center',
                        color=color, 
                        parent=self,
                        interactable=True)
        self.location = Box(x=10, y=10, 
                        width=200, height=40,
                        position='top-center', 
                        margin=20, padding=10, 
                        border=0, border_radius=10, 
                        border_color=None, 
                        content=locator('Newcastle'), 
                        content_color=(255,255,255), 
                        content_position='center',
                        color=color, 
                        parent=self.box,
                        interactable=False)
        self.date = Box(x=10, y=10, 
                        width=200, height=40,
                        position='bottom-center',
                        margin=20, padding=10, 
                        border=0, border_radius=10, 
                        border_color=None, 
                        content=f'{d.day}/{d.month}/{d.year}  {d.hour}:{d.minute}:{d.second}', 
                        content_color=(255,255,255), 
                        content_position='center',
                        color=color,
                        parent=self.box, 
                        interactable=False)

    def position_content(self):
        d = datetime.fromtimestamp(time.time())
        if hasattr(self, 'date'):
            self.date.content = d.strftime('%d/%m/%y  %H:%M:%S')
            self.date.position_content()
        Box.position_content(self)

    def draw(self, screen):
        self.position_content()
        width = screen.get_rect().width 
        if self.width != width:
            self.width = width 
            self.rect = (self.x, self.y, self.width, self.height)
            self.position_box()
        Box.draw(self, screen)
        self.box.draw(screen)
        self.date.draw(screen)
        self.location.draw(screen)


class Footer(Box):
    def __init__(self,parent=None, 
                x=0, y=0,  
                height=80, 
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content=None,
                content_color=(255,255,255),
                content_position='center',
                color=(133,133,133),
                interactable=False):

        position=self.BOTTOMLEFT
        width = parent.get_rect().width

        Box.__init__(self,parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, 
                content_position, color,
                interactable)

    def draw(self, screen):
        width = screen.get_rect().width 
        if self.width != width:
            self.width = width 
            self.rect = (self.x, self.y, self.width, self.height)
            self.position_box()
        Box.draw(self, screen)

class LeftSideBar(Box):
    def __init__(self,parent=None, 
                x=0, y=0, width=80, 
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content=None,
                content_color=(255,255,255),
                content_position='center', 
                color=(133,133,133),
                interactable=False):

        position=self.TOPLEFT 
        height = parent.get_rect().height

        Box.__init__(self,
                parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, 
                content_position, color,
                interactable)

    def draw(self, screen):
        height = screen.get_rect().height 
        if self.height != height:
            self.height = height 
            self.rect = (self.x, self.y, self.width, self.height)
        Box.draw(self, screen)
    
class RightSideBar(Box):
    def __init__(self,parent=None, 
                x=0, y=0, width=80, 
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content=None,
                content_color=(255,255,255),
                content_position='center',
                color=(133,133,133),
                interactable=False):

        position=self.TOPRIGHT
        height = parent.get_rect().height

        Box.__init__(self,
                parent, x, y,
                width, height,
                position,
                margin, padding,
                border, border_radius,
                border_color, content,
                content_color, 
                content_position, color,
                interactable)

    def draw(self, screen):
        height = screen.get_rect().height 
        if self.height != height:
            self.height = height 
            self.rect = (self.x, self.y, self.width, self.height)
        Box.draw(self, screen)
