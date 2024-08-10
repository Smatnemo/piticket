class Box:
    def __init__(self, x, y, 
                width, height, 
                margin, padding,                 
                border, border_radius,
                border_color,
                content, color,
                content_color, 
                interactable):
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

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class PopUpBox(Box):
    def __init__(self):
        Box.__init__(self)

