import pytest
import pygame 

@pytest.fixture
def view_loop():
    def loop(func, *args, **kwargs):   
        clk = pygame.time.Clock()
        fps = 40
        start = True
        while start:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    start = False

            func(*args, **kwargs)
            pygame.display.update()
            clk.tick(fps)

    return loop