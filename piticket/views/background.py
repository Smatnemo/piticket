import pygame 

class Background():
    def __init__(self, image_name, bg_color=(0,0,0), text_color=(255,255,255)):
        self._bg_color = bg_color 
        self._text_color = text_color

        self._name = image_name

        self._texts = []
        # Return a SysFont object by passing the name of the font
        self.font = pygame.font.SysFont('nimbussansnarrow',22)

    def __str__(self):
        return "{}".format(self.__class__.__name__)

    def _write_texts(self, text, screen):
        """Create text surfaces to draw on window surface.
        :param text: text to be written on screen
        :type param: str
        """
        
        self._texts.append(self.font.render(text,True,self._text_color))
        if self._texts:
            screen.blit(self._texts[0],(0,0))

    def set_color(self, color_or_path):
        """Set background color using RGB tuple or path to an image
        
        :param color_or_path: RGB color tuple or image path
        :type color_or_path: tuple or str
        """
        assert len(color_or_path) == 3, "Length of 3 is required (RGB tuple)"
        self._bg_color = color_or_path

    def set_text_color(self, color):
        """"""
        assert len(color) == 3, "Length of 3 is required (RGB tuple)"
        self._text_color = color

    def paint(self, screen):
        screen.fill(self._bg_color)
        self._write_texts('Ticket text', screen)


class IntroBackground(Background):
    def __init__(self):
        Background.__init__(self, 'intro') 
        
