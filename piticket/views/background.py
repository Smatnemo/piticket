import pygame 

class Background():
    def __init__(self, bg_color, text_color):
        self._bg_color = bg_color 
        self._text_color = text_color

        self._texts = []
        self.font = None

    def _write_texts(self, text, screen):
        """Create text surfaces to draw on window surface.
        :param text: text to be written on screen
        :type param: str
        """
        available_fonts = pygame.font.get_fonts()
        # Get a list of available fonts
        print(available_fonts)
        # initialize font object in pygame
        # return a font of size 12
        # If you intend to use a truetype Face font file, use size parameter as well
        # 
        font = pygame.font.Font()
        # Return a SysFont object by passing the name of the font
        self.font = pygame.font.SysFont('nimbussansnarrow',22)
        self._texts.append(self.font.render(text,True,self._text_color))
        if self._texts:
            screen.blit(self._texts[0],(0,0))


    def paint(self, screen):
        screen.fill(self._bg_color)
        self._write_texts('Ticket text', screen)
        
        
