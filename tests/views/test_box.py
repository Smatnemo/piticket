import pygame
import pytest
from piticket.views.box import (Box, Button, PopUpBox, PopUpBoxProcessing, Header,
                                Footer, RightSideBar, LeftSideBar)

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


def test_popupbox_update(view_loop):
    popupbox = PopUpBox(parent=win,timeout=10)
    # Create call back functions for buttons
    popupbox.btn1.clicked(print_func, 'Clicked Button 1')
    popupbox.btn2.clicked(print_func, 'Clicked Button 2')
    view_loop(popupbox.update, win)
    view_loop(popupbox.clear, win)
    

def test_popupboxprocessing_update(view_loop):
    popupprocess = PopUpBoxProcessing(pygame.event.Event(pygame.MOUSEBUTTONUP,{'btn':1}),parent=win,gif_image='Spinner_transparent')
    popupprocess.triggered(print_func, 'Clicked Button pop up')
    view_loop(popupprocess.update, win)
    view_loop(popupprocess.clear, win)
    
def test_header_draw(view_loop):
    header = Header(parent=win)
    view_loop(header.draw,win)
    view_loop(header.clear,win)

def test_footer_draw(view_loop):
    footer = Footer(parent=win)
    view_loop(footer.draw,win)
    view_loop(footer.clear,win)

def test_right_side_bar_draw(view_loop):
    right_side_bar = RightSideBar(parent=win)
    view_loop(right_side_bar.draw,win)
    view_loop(right_side_bar.clear,win)

def test_left_side_bar_draw(view_loop):
    left_side_bar = LeftSideBar(parent=win)
    view_loop(left_side_bar.draw,win)
    view_loop(left_side_bar.clear,win)

        