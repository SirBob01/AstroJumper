## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
import pygame
from pygame.locals import *
from space import *

class State(object):
    def __init__(self, engine, name):
        self.name = name
        self.engine = engine
        self.screen = engine.screen
        self.fonts = engine.fonts
        self.starfield = StarField()
        self.buttons = []
        self.events = {'esc' : 0,
                       'up' : 1,
                       'down' : 2,
                       'left' : 3,
                       'right' : 4,
                       'space' : 5,
                       'keyup' : 7,
                       'click' : 8}
        self.active = None
        self.counter = 0

    def render(self):
        pass

    def handleEvents(self):
        for b in self.buttons:
            b.render(self.screen)
            
        for e in pygame.event.get():
            if e.type == QUIT:
                self.engine.quitGame()

            if e.type == MOUSEBUTTONDOWN:
                self.active = self.events['click']
            if e.type == MOUSEBUTTONUP:
                for b in self.buttons:
                    if b.rect.collidepoint(e.pos):
                        b.callEvent()
            if e.type == MOUSEMOTION:
                for b in self.buttons:
                    if b.rect.collidepoint(e.pos):
                        b.sel = True
                    else:
                        b.sel = False
                        
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.engine.quitGame()
                if e.key == K_SPACE:
                    self.active = self.events['space']
                if e.key == K_UP:
                    self.active = self.events['up']
                if e.key == K_DOWN:
                    self.active = self.events['down']
                if e.key == K_LEFT:
                    self.active = self.events['left']
                if e.key == K_RIGHT:
                    self.active = self.events['right']
                if e.key == K_x:
                    ## To prevent continuous shooting...
                    if self.name == 'Game on!':
                        if self.player.shots < self.player.overheat:
                            self.player.state = 'shoot'
                            self.player.shots += 1
                    else:
                        pass
                    
            if e.type == KEYUP:
                self.active = self.events['keyup']
        
                
