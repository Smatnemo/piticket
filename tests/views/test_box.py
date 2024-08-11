import pygame
from piticket.views.box import Box

# Initialize pygame and set display
pygame.init()
win = pygame.display.set_mode((800,400), pygame.RESIZABLE)
win.fill((255,0,0))

content = '/home/pi/Dev/piticket/piticket/pictures/assets/pibooth.png'
# Create instance here after initializing pygame
box = Box(x=10, y=10, 
        width=100, height=60, 
        margin=20, padding=10, 
        border=3, border_radius=10, 
        border_color=(0,0,0), 
        content='Buttton', 
        content_color=(0,0,0), 
        color=(255, 255, 255), 
        interactable=True)
# Create box instance with image
image_box = Box(x=10, y=10, 
        width=100, height=60, 
        margin=20, padding=10, 
        border=3, border_radius=10, 
        border_color=(0,0,0), 
        content=content, 
        content_color=(0,0,0), 
        color=(255, 255, 255), 
        interactable=True)

def test_draw_text(view_loop):
    view_loop(image_box.draw, win)

def test_draw(view_loop):
    view_loop(box.draw, win)

        