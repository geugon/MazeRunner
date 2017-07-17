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


ROOT2 = 0.5**0.5


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

        # setup image
        r = settings.PLAYER_RADIUS
        self.image = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        self.image.fill(colors.CLEAR)
        pygame.draw.circle(self.image, colors.RED, (r, r), r, 0)
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()

        # setup movement
        self._acc = settings.PLAYER_MAXSPEED*settings.PLAYER_DRAG
        self._drag = settings.PLAYER_DRAG
        self._pos = (20.0, 100.0) # unsnapped position
        self._vel = (0.0, 0.0)

        pos = tuple((int(x) for x in self._pos))
        self.rect.center = pos

    def set_direction(self, up, down, left, right):
        if up and not down:
            y = -1
        elif down and not up:
            y = 1
        else:
            y = 0

        if left and not right:
            x = -1
        elif right and not left:
            x = 1
        else:
            x = 0

        if y==1 and x!=0:
            y = ROOT2
        if y==-1 and x!=0:
            y = -ROOT2

        if x==1 and y!=0:
            x = ROOT2
        if x==-1 and y!=0:
            x = -ROOT2

        self._dir = (x,y)

    def update(self, timestep):
        # velocities are pixels/sec
        dx = (1.0-timestep*self._drag)*self._vel[0] + timestep*self._acc*self._dir[0]
        dy = (1.0-timestep*self._drag)*self._vel[1] + timestep*self._acc*self._dir[1]
        print("x={}\tdx={}\ttimestep={}\tdrag={}\tacc=={}".format(self._pos[0],dx,timestep,self._drag,self._acc)) 

        self._vel = (dx, dy)
        self._pos = (self._pos[0]+self._vel[0]*timestep,
                     self._pos[1]+self._vel[1]*timestep)
        pos = tuple((int(x) for x in self._pos))
        self.rect.center = pos


class View():

    """ Controls all displays to screen """

    def __init__(self):
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        pygame.display.set_caption("Maze Runner by Geugon")
        self._spriteGroups = {}

        # background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(colors.WHITE)
        self.background = self.background.convert()

    def store_sprite(self, sprite, groupName):
        if groupName not in self._spriteGroups:
            self._spriteGroups[groupName] = pygame.sprite.Group()
        sprite.add(self._spriteGroups[groupName])

    def draw_background(self):
        self.screen.blit(self.background, (0,0))
        
    def blit(self, surface, pos):
        """ Manually draw to screen """
        self.screen.blit(surface, pos)

    def update(self, timestep):
        for k, v in self._spriteGroups.items():
            v.update(timestep)
            v.draw(self.screen)
        pygame.display.update()


class MazeRunner():

    """ The game... """

    def __init__(self):
        pygame.init()
        self.view = View()
        self.running = False
        self.runtime = 0
        
        # setup
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('freeansbold.ttf', 24)

        # player
        self.playerSprite = PlayerSprite()
        self.view.store_sprite(self.playerSprite, 'player')

    def run(self):
        self.running = True
        while self.running:
            self.runtime += self.clock.tick(settings.FPS)
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
        self.playerSprite.set_direction(keys_pressed[pygame.K_UP],
                                        keys_pressed[pygame.K_DOWN],
                                        keys_pressed[pygame.K_LEFT],
                                        keys_pressed[pygame.K_RIGHT])

    def _viewTick(self):
        msg = "Run time: {}".format(str(self.runtime/1000.0))
        HUDclock = self.font.render(msg, True, colors.BLACK)
        self.view.draw_background()
        self.view.blit(HUDclock, (50,50))
        self.view.update(self.clock.get_time()/1000.0)

    def cleanup(self):
        pygame.quit()



if __name__ == "__main__":
   colors = Settings('colors.json')
   settings = Settings('settings.json')
   mr = MazeRunner()
   mr.run()
   mr.cleanup()
