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
FPS = 30

if __name__ == "__main__":
    
    # init
    pygame.init()
    screen=pygame.display.set_mode(SCREEN_SIZE)

    # background
    background = pygame.Surface(screen.get_size())
    background.fill(WHITE)
    screen.blit(background, (0,0))

    # settings
    clock = pygame.time.Clock()
    clock.tick(FPS)

    # loop
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.update()

    # clean up
    pygame.quit()
