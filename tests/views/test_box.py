import pygame
from piticket.views.box import Box, Button, PopUpBox, PopUpBoxProcessing

# Auxiliary function
def print_func(*args):
    if args: 
        print(args[0])
# Initialize pygame and set display
pygame.init()
win = pygame.display.set_mode((800,400), pygame.RESIZABLE)
win.fill((255,0,0))

content = '/home/pi/Dev/piticket/piticket/pictures/assets/pibooth.png'
# Create instance here after initializing pygame
box = Box(x=10, y=10, 
        width=100, height=60,
        position='center', 
        margin=20, padding=10, 
        border=3, border_radius=10, 
        border_color=(0,0,0), 
        content='Box', 
        content_color=(0,0,0), 
        color=(255, 255, 255), 
        parent=win,
        interactable=True)
# Create box instance with image
image_box = Box(x=10, y=10, 
        width=100, height=60,
        position='center',
        margin=20, padding=10, 
        border=3, border_radius=10, 
        border_color=(0,0,0), 
        content=content, 
        content_color=(0,0,0), 
        color=(255, 255, 255),
        parent=win, 
        interactable=True)

def test_draw_text(view_loop):
    view_loop(image_box.draw, win)

def test_draw(view_loop):
    view_loop(box.draw, win)

def test_clear(view_loop):
    view_loop(box.clear, win)

# Test button
button = Button(parent=win)
# Test callback function for clicked
button.clicked(print_func, 'Clicked')
# Test callback function for hovered
button.hovered(print_func, 'Hovered')

def test_button_update(view_loop):
    view_loop(button.update, win)

def test_clear_button(view_loop):
    view_loop(button.clear, win)


# Test PopUpBox
popupbox = PopUpBox(parent=win)
# Create call back functions for buttons
popupbox.btn1.clicked(print_func, 'Clicked Button 1')
popupbox.btn2.clicked(print_func, 'Clicked Button 2')

def test_popupbox_update(view_loop):
    view_loop(popupbox.update, win)

def test_popupbox_clear(view_loop):
    view_loop(popupbox.clear, win)

popupprocess = PopUpBoxProcessing(pygame.event.Event(pygame.MOUSEBUTTONUP,{'btn':1}),parent=win,gif_image='Spinner_transparent')
popupprocess.triggered(print_func, 'Clicked Button pop up')
def test_popupboxprocessing_update(view_loop):
    view_loop(popupprocess.update, win)

def test_popupboxprocessing_clear(view_loop):
    view_loop(popupprocess.clear, win)
        