import cv2 
import pygame 

from .video import Video
from .post_processing import PostProcessing


class VideoPygame(Video):
    def __init__(self, path, chunk_size=10, max_threads=1, max_chunks=1, subs=None, post_process=PostProcessing.none, interp=cv2.INTER_LINEAR, use_pygame_audio=False, 
                reverse=False, no_audio=False, speed=1, youtube=False, quality=0, loop=True):
        Video.__init__(self, path, chunk_size, max_threads, max_chunks, subs, post_process, interp, use_pygame_audio, reverse, no_audio, speed, youtube, quality)
        self._loop = loop

    def __str__(self):
        return f"<VideoPygame(path={self.path})>"

    def _handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.QUIT:
                # place event back in the event queue after use
                pygame.event.post(event)
                self.close()

    def _create_frame(self, data):
        return pygame.image.frombuffer(data.tobytes(), self.current_size, "BGR")
    
    def _render_frame(self, surf, pos):
        surf.blit(self.frame_surf, pos)
    
    def loop(self):
        if self._stop_loading and self._chunks_played == self._chunks_claimed:
            if self._loop:
                self.play()

    def preview(self, screen):
        while self.active:
            events = pygame.event.get()
            self._handle_events(events)
            rect = screen.get_rect()
            self.resize((rect.width, rect.height))
            self.draw(screen, (0, 0), force_draw=False)
            pygame.display.update()
            # play in a loop if _loop is True
            self.loop()
            