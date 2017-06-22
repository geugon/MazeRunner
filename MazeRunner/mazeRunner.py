#!/usr/bin/env python
"""
mazeRunner.py

Escape the maze quickly.

Author:     geugon
License:    Apache License 2.0
            See http://www.apache.org/licenses/LICENSE-2.0
"""

import pygame

SCREEN_SIZE = (640, 480)
WHITE = (230, 230, 230)
BLACK = (0, 0, 0)
FPS = 30


class MazeRunner():

    """ The game... """

    def __init__(self):
        pygame.init()
        self.running = False
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.runtime = 0
        
        # background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(WHITE)

        # settings
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('freeansbold.ttf', 24)

    def run(self):
        self.running = True
        while self.running:
            self._controlTick()
            self._viewTick()
    
    def _controlTick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def _viewTick(self):
        self.runtime += self.clock.tick(FPS)
        surface = self.font.render(str(self.runtime), True, BLACK)
        self.screen.blit(self.background, (0,0))
        self.screen.blit(surface, (50,50))
        pygame.display.update()

    def cleanup(self):
        pygame.quit()



if __name__ == "__main__":
   mr = MazeRunner()
   mr.run()
   rm.cleanup()
