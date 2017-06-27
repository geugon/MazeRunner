#!/usr/bin/env python
"""
mazeRunner.py

Escape the maze quickly.

Author:     geugon
License:    Apache License 2.0
            See http://www.apache.org/licenses/LICENSE-2.0
"""

import pygame
import json
from ast import literal_eval


class Settings():
    
    """ Parses and stores settings from input json file """

    def __init__(self, color_fname):
        """ Input json must have single depth level """
        with open(color_fname) as f:
            data = json.load(f)
        for k,v in data.items():
            setattr(self, k, literal_eval(v))


class PlayerSprite(pygame.sprite.Sprite):

    """ Player's Sprite """

    def __init__(self):
        super(PlayerSprite, self).__init__()
        r = settings.PLAYER_RADIUS
        self.image = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        self.image.fill(colors.CLEAR)
        pygame.draw.circle(self.image, colors.RED, (r, r), r, 0)
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
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        self.runtime = 0
        
        # background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(colors.WHITE)

        # setup
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
        self.runtime += self.clock.tick(settings.FPS)
        surface = self.font.render(str(self.runtime), True, colors.BLACK)
        self.screen.blit(self.background, (0,0))
        self.screen.blit(surface, (50,50))

        self.playerSpriteGroup.draw(self.screen)
        pygame.display.update()

    def cleanup(self):
        pygame.quit()



if __name__ == "__main__":
   colors = Settings('colors.json')
   settings = Settings('settings.json')
   mr = MazeRunner()
   mr.run()
   mr.cleanup()
