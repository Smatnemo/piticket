
class Background():
    def __init__(self, bg_color, text_color):
        self._bg_color = bg_color 
        self._text_color = text_color

    
    
    def paint(self, screen):
        screen.fill(self._bg_color)
        
