from box import Box 

class Button(Box):
    def __init__(self, x=0, y=0,
                width=100, height=60,
                margin=20, padding=10,
                border=1, border_radius=3,
                border_color=(0,0,0),
                content='Button',
                content_color=(255,255,255),
                color=(133,133,133),
                interactable=True):
        Box.__init__(self, x, y,
                    width, height, 
                    margin, padding,
                    border, border_radius,
                    border_color,
                    content, 
                    content_color,
                    color,
                    interactable)

    def handle_events(self, events):
        pass
        