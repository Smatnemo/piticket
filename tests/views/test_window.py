import pygame
from piticket.views.window import PiWindow

win = PiWindow('Ticket App Test')


def test_init(view_loop):
    view_loop(win.show_intro)

def test_video(view_loop):
    view_loop(win.show_choice)


