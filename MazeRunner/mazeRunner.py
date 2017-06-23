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
PLAYER_RADIUS = 10
WHITE = (230, 230, 230)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CLEAR = (0, 0, 0, 0)
FPS = 30


class PlayerSprite(pygame.sprite.Sprite):

    """ Player's Sprite """

    def __init__(self):
        super(PlayerSprite, self).__init__()
        self.image = pygame.Surface((PLAYER_RADIUS*2, PLAYER_RADIUS*2), pygame.SRCALPHA)
        self.image.fill(CLEAR)
        pygame.draw.circle(self.image, RED, (10, 10), PLAYER_RADIUS, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (20, 100)

    def move(self, direction):
        vel = 2
        dx, dy = [tmp*vel for tmp in direction]
        x, y = self.rect.center
        self.rect.center = x+dx, y+dy


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

        # player
        self.playerSprite = PlayerSprite()
        self.playerSpriteGroup = pygame.sprite.Group()
        self.playerSprite.add(self.playerSpriteGroup)


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

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP]:
            self.playerSprite.move((0, -1))
        if keys_pressed[pygame.K_DOWN]:
            self.playerSprite.move((0, 1))
        if keys_pressed[pygame.K_LEFT]:
            self.playerSprite.move((-1, 0))
        if keys_pressed[pygame.K_RIGHT]:
            self.playerSprite.move((1, 0))

    def _viewTick(self):
        self.runtime += self.clock.tick(FPS)
        surface = self.font.render(str(self.runtime), True, BLACK)
        self.screen.blit(self.background, (0,0))
        self.screen.blit(surface, (50,50))

        self.playerSpriteGroup.draw(self.screen)
        pygame.display.update()

    def cleanup(self):
        pygame.quit()



if __name__ == "__main__":
   mr = MazeRunner()
   mr.run()
   mr.cleanup()
