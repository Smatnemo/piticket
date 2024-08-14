import pytest
import pygame 

@pytest.fixture
def view_loop():
    def loop(func, *args, **kwargs): 
        print(f'Exectuting {func.__name__}')  
        clk = pygame.time.Clock()
        fps = 24
        start = True
        while start:
            events = pygame.event.get()
            event = None
            for event in events:
                if event.type == pygame.QUIT:
                    start = False
                if event.type == pygame.MOUSEBUTTONDOWN\
                    or event.type == pygame.MOUSEBUTTONUP\
                    or event.type == pygame.MOUSEMOTION:
                    event = event
            if func.__name__=='update':
                func(event, *args, **kwargs)
            else:
                func(*args, **kwargs)
            pygame.display.update()
            clk.tick(fps)

    return loop