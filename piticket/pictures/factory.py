import zlib 
import base64
from PIL import Image, ImageDraw
from io import BytesIO
from xml.etree import ElementTree
from urllib.parse import unquote
from piticket import fonts
from piticket.utils import LOGGER 
from piticket.views.box import Box


def get_ticket_factory(filename, ticket):
    """Return an object for building the ticket.

    :param filename: file path of the xml template for the ticket
    :type filename: str
    :param ticket: dictionary with ticket values
    """
    
    return TicketFactory(filename, ticket)

def px(cin, dpi=600):
    """Convert a dimension in centiinch into pixels.

    :param cin: dimension in centiinch
    :type cin: str, float, int
    :param dpi: dot-per-inch
    :type dpi: int
    """
    return int(float(cin) * dpi / 100)

class TemplateParserError(Exception):
    pass 

class TemplateParser(object):
    """A template is based on a XML file generated with flowchart Maker
    at https://app.diagrams.net.
    """
    def __init__(self, filename, modified_ticket):
        self.filename = filename 
        self.modified_ticket = modified_ticket
        self.data = self.parse()
        
    def inflate(self, data, b64=False):
        """Decompress the data using zlib.
        
        In ~2016 Flowchart Maker started compressing 'using standard deflate'
        https://about.draw.io/extracting-the-xml-from-mxfiles
        """
        if b64: # Optional, additionally base64 decode
            data = base64.b64decode(data)
        return unquote(zlib.decompress(data, -15).decode('utf8'))

    def parse(self):
        """Parse the XML template file.

        :return: data dictionary
        :rtype: dict
        """
        data = {}
        LOGGER.info('Parsing ticket template file: %s', self.filename)
        doc = ElementTree.parse(self.filename).getroot()
        
        for diagram in doc.iter('diagram'):

            if not list(diagram) and diagram.text.strip(): # if it is compressed
                template = ElementTree.fromstring(self.inflate(diagram.text, True))
            else:
                template = diagram.find('mxGraphModel')
            
            template.set('name', diagram.get('name'))
            dpi = int(template[0][0].get('dpi',300))
            size = (px(template.attrib['pageWidth'], dpi),px(template.attrib['pageHeight'], dpi))
            
            shapes = []
            distinct_capture_count = set()
            for cell in template.iter('mxCell'):
                shape = TemplateShapeParser(cell, dpi)

                if shape.type == TemplateShapeParser.TYPE_UNKNOWN:
                    continue 

                if shape.type == TemplateShapeParser.TYPE_TEXT:
                    # Take only text with the name in dictionary
                    if shape.text in self.modified_ticket:
                        shapes.append(shape)
                    else:
                        LOGGER.warning("Template text holder with text '%s' ignored", shape.text)
                else:
                    shapes.append(shape)
                
                # If shape is on the left or the right of the page
                if shape.x + shape.width <= 0 or shape.x >= size[0]:
                    LOGGER.warning("Template shape '%s' X-position out of bounds, try to auto-adjust", shape.text)
                    shape.x = shape.x % size[0]
                
                # If shape is above or below the page
                if shape.y + shape.height <= 0 or shape.y >= size[1]:
                    LOGGER.warning("Template shape '%s' Y-position out of bounds, try to auto-adjust", shape.text)

            # Create template parameters dictionary
            data['shapes'] = shapes
            data['size'] = size
            
            # Calculate the orientation majority for this template
            texts = [shape for shape in shapes if shape.type == TemplateShapeParser.TYPE_TEXT]

            LOGGER.info("Found template '%s': %s texts - %s others", template.get('name'), 
                        len(texts), len(shapes)-len(texts))
        
        if not data:
            raise TemplateParserError("No template found in '{}'".format(self.filename))
        return data
    
    def get(self, key):
        """Return the value of the key passed.
        :param key: key info to get
        :type key: str
        """
        return self.data[key]
    
    def get_size(self):
        """Return the final size of the template or ticket in pixels
        """
        return self.get('size')

    def get_rects(self):
        """Return a list of top-left coordinates and max size rectangle.
        """
        return self.get('shapes')

    def get_text_rects(self):
        """Return a list of top-left coordinates and max size rectangles for texts.
        """
        return [shape for shape in self.get_rects() if shape.type == TemplateShapeParser.TYPE_TEXT]


class TemplateShapeParser(object):
    
    TYPE_TEXT = 'text'
    TYPE_IMAGE = 'image'
    TYPE_UNKNOWN = 'unknown'

    def __init__(self, mxcell_node, dpi):
        self.text = self.parse_text(mxcell_node)
        self.style = self.parse_style(mxcell_node)
        self.image = self.style.get('image')
        self.rotation = -int(self.style.get('rotation', 0))
        self.x, self.y, self.width, self.height = self.parse_geometry(mxcell_node, dpi)

        # Define shape type 
        if mxcell_node.get('vertex') == '1' and mxcell_node.get('style').startswith('shape=image'):
            self.type = self.TYPE_IMAGE
        elif mxcell_node.get('vertex') == '1' and mxcell_node.get('style').startswith('text;'):
            self.type = self.TYPE_TEXT
        else:
            self.type = self.TYPE_UNKNOWN
    
    def __repr__(self):
        return f"Shape(text='{self.text}', type={self.type})"

    def parse_text(self, mxcell_node):
        """Extract text.
        
        :param mxcell_node: 'mxcell_node' node 
        :type mxcell_node: :py:class: `lementTree.Element`
        """
        try:
            value = ElementTree.fromstring(str(mxcell_node.get('value'))).text
        except ElementTree.ParseError:
            value = mxcell_node.get('value') or ''
        return value 

    def parse_style(self, mxcell_node):
        """Extract style data.
        
        :param mxcell_node: '' node
        :type mxcell_node: :py:class: `ElementTree.Element`
        """
        styledict = {'name': ''}
        if 'style' in mxcell_node.attrib:
            style = [p for p in mxcell_node.attrib['style'].split(';') if p.strip()]
            if '=' not in style[0]:
                styledict['name'] = style.pop(0)
            for key_value in style:
                key, value = key_value.split('=', 1)
                styledict[key] = value 
        return styledict
    
    def parse_geometry(self, mxcell_node, dpi=300):
        """Extract geometry data.

        :param mxcell_node: 'mxCell' node
        :type mxcell_node: :py:class: `ElementTree.Element`
        :param dpi: dot-per-inch
        :type dpi: int
        """
        geometry = mxcell_node.find('mxGeometry')
        if geometry is None:
            x, y, width, height = 0, 0, 0, 0
        else:
            x = px(geometry.get('x', 0), dpi)
            y = px(geometry.get('y', 0), dpi)
            width = px(geometry.attrib.get('width', 0), dpi)
            height = px(geometry.attrib.get('height', 0), dpi)
        return x, y, width, height 


class TicketFactory:
    def __init__(self, template, ticket):
        """
        :attr template: template parser """
        self.template = TemplateParser(template, ticket) 
        self.ticket = ticket
        size = self.template.get_size()
        self.image = self._build_ticket(Image.new('RGBA',size,(255,0,0,0)))
        
    def _image_paste(self, image, dest_image, pos_x, pos_y, angle=None):
        """Paste an image onto another one with the given rotation angle.
        
        :param image: PIL image to draw
        :type image: :py:class: `PIL.Image`
        :param dest_image: PIL image to draw on
        :param pos_x: X-axis position from the left
        :type pos_x: int
        :param pos_y: Y-axis position from the top
        :type pos_y: int
        :param angle: angle rotation in degree
        :type angle: int
        """
        width, height = image.size
        if angle:
            image = image.rotate(angle, expand=True)
        dest_image.paste(image,
                         (pos_x + (width - image.width)//2,
                          pos_y + (height - image.height)//2),
                         image if angle is not None else None)

    def _build_ticket(self, image):
        """Build final ticket by drawing all the shapes defined in the template
        :return: drawn image
        :rtype: :py:class: `PIL.Image`
        """
        i = 0
        for shape in self.template.get_rects():
            i += 1
            if shape.type == TemplateShapeParser.TYPE_TEXT:
                rect = Image.new('RGBA', (shape.width, shape.height), (255, 0, 0, 0))
                draw = ImageDraw.Draw(rect)
                
                if isinstance(self.ticket[shape.text], Box):
                    text = self.ticket[shape.text].content 
                else:
                    text = self.ticket[shape.text]
                if not text:
                    text = 'NIL'
                
                font = fonts.get_pil_font(text,fonts.get_filename('Monoid-Bold.ttf'), shape.width, shape.height)
                _, text_height = font.getsize(text)
                (text_width, _baseline), (offset_x, offset_y) = font.font.getsize(text)
                
                x = (shape.width - text_width) // 2
                
                draw.text((x, (shape.height - text_height) // 2 - offset_y // 2), text, (0,0,0), font=font)
                self._image_paste(rect, image, shape.x, shape.y, shape.rotation)
                
            elif shape.type == TemplateShapeParser.TYPE_IMAGE:
                data = base64.b64decode(shape.image.split(',',1)[1])
                src_image = Image.open(BytesIO(data))
                src_image = src_image.resize((shape.width, shape.height))
                rect = Image.new('RGBA', (shape.width, shape.height), (255, 0, 0, 0))
                self._image_paste(src_image, rect, 0, 0)
                self._image_paste(rect, image, shape.x, shape.y, shape.rotation)
        return image
     
    def save(self, ticket_file):
        self.image.save(ticket_file)