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
import random
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


class Player(pygame.sprite.Sprite):

    """ Player's Sprite """

    def __init__(self):
        super(Player, self).__init__()

        # setup image
        self.radius = settings.PLAYER_RADIUS
        r = self.radius
        self.image = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, colors.RED, (r, r), r, 0)
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()

        # setup movement
        self._acc = settings.PLAYER_MAXSPEED*settings.PLAYER_DRAG
        self._drag = settings.PLAYER_DRAG
        self._pos = (20.0, 100.0) # unsnapped position
        self._vel = (0.0, 0.0)
        self._set_rect_pos()


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

    def move(self, timestep, mediator):
        # velocities are pixels/sec
        dx = ((1.0-timestep*self._drag)*self._vel[0] + 
              timestep*self._acc*self._dir[0])
        dy = ((1.0-timestep*self._drag)*self._vel[1] + 
              timestep*self._acc*self._dir[1])
        self._vel = (dx, dy)

        old_pos = self._pos
        self._pos = (old_pos[0]+self._vel[0]*timestep,
                     old_pos[1]+self._vel[1]*timestep)
        self._set_rect_pos()
        if mediator.approve_move():
            pass
        else:
            self._vel = (-dx*0.5, -dy*0.5)
            self._pos = (old_pos[0], old_pos[1])
            self._set_rect_pos()

    def _set_rect_pos(self):
        self.rect.center = (int(self._pos[0]-self.radius),
                            int(self._pos[1]+self.radius))


class Block(pygame.sprite.Sprite):

    """ Obstacle to prevent player movement """

    def __init__(self, pos):
        super(Block, self).__init__()
        self.size= settings.BLOCK_SIZE
        s = self.size
        self.image = pygame.Surface((s,s))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, colors.BLACK, self.rect)
        self.image = self.image.convert()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        

class Objective(pygame.sprite.Sprite):

    """ The objective of the game is to reach this """

    def __init__(self):
        super(Objective, self).__init__()

        # setup image
        self.radius = settings.OBJECTIVE_RADIUS
        r = self.radius
        self.image = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, colors.GREEN, (r, r), r, 0)
        self.rect = self.image.get_rect()
        self.image = self.image.convert_alpha()
        self.rect.x = random.randrange(settings.SCREEN_SIZE[0])
        self.rect.y = random.randrange(settings.SCREEN_SIZE[1])


class SpriteMediator():

    """ Manages state and interaction of sprites """

    def __init__(self):
        
        self.groups = {}
        
        # create all sprites
        self.player = Player()
        self.store_sprite(self.player, 'player')
        self.objective = Objective()
        self.store_sprite(self.objective, 'objective')
        
        self.walls = []
        for pos in [(15,200),(25,200)]:
            self.walls.append(Block(pos))
            self.store_sprite(self.walls[-1], 'wall')

    def store_sprite(self, sprite, groupName):
        if groupName not in self.groups:
            self.groups[groupName] = pygame.sprite.Group()
        sprite.add(self.groups[groupName])

    def register_inputs(self, cmds):
        self._cmds = cmds

    def update(self, timestep):
        """ Updates position and other attributes,
            but does not draw """
        self.player.set_direction(*self._cmds)
        self.player.move(timestep, self)

    def approve_move(self):
        if pygame.sprite.groupcollide(self.groups['player'],
                                      self.groups['wall'],
                                      False, False):
            return False
        else:
            return True

    def update_state(self):
        if pygame.sprite.collide_circle(self.player, self.objective):
            return "victory"
        return "running"


class View():

    """ Controls all displays to screen """

    def __init__(self):

        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        pygame.display.set_caption("Maze Runner by Geugon")

        # background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(colors.WHITE)
        self.background = self.background.convert()

    def draw_background(self):
        self.screen.blit(self.background, (0,0))
        
    def blit(self, surface, pos):
        """ Manually draw to screen """
        self.screen.blit(surface, pos)

    def update(self, spriteGroups):
        for k, v in spriteGroups.items():
            v.update()
            v.draw(self.screen)
        pygame.display.update()


class MazeRunner():

    """ The game... """

    def __init__(self):
        pygame.init()
        self.view = View()
        self.sprites = SpriteMediator()
        self.state = 'done'
        
        # setup
        self.runtime = 0
        self.playtime = 0
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('freeansbold.ttf', 24)

    def run(self):
        self.state = 'running'
        while self.state != 'done':
            self.runtime += self.clock.tick(settings.FPS)
            self._controlTick()
            self._viewTick()
    
    def _controlTick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = 'done'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = 'done'

        keys_pressed = pygame.key.get_pressed()
        cmds = (keys_pressed[pygame.K_UP],
                keys_pressed[pygame.K_DOWN],
                keys_pressed[pygame.K_LEFT],
                keys_pressed[pygame.K_RIGHT])
        self.sprites.register_inputs(cmds)

        if self.state == 'running':
            self.sprites.update(self.clock.get_time()/1000.0) 
            self.playtime = self.runtime
            self.state = self.sprites.update_state()
 

    def _viewTick(self):
        msg = "Run time: {}".format(str(self.playtime/1000.0))
        HUDclock = self.font.render(msg, True, colors.BLACK)
        self.view.draw_background()
        self.view.blit(HUDclock, (50,50))
        self.view.update(self.sprites.groups)

    def cleanup(self):
        pygame.quit()



if __name__ == "__main__":
   colors = Settings('colors.json')
   settings = Settings('settings.json')
   mr = MazeRunner()
   mr.run()
   mr.cleanup()
