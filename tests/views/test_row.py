import pygame
from piticket.views.row import Row, RowView

# Initialize pygame and set display
pygame.init()
win = pygame.display.set_mode((800,400), pygame.RESIZABLE)
win.fill((255,0,0))

def test_row_view(view_loop):
    row_view = RowView(parent=win)
    view_loop(row_view.update, win)

def test_row(view_loop):
    row = Row(content='Row',padding=20,parent=win)
    view_loop(row.update, win)
    