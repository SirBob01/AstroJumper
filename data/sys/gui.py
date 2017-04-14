## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
from pie.physics import *
from pie.color import *
from constants import *
from resources import *


class Button(object): ### TODO: Implement  callEvent() taking parameters.
    def __init__(self, pos, label='', font=None, colors=(B_COLORS['YELLOW'], B_COLORS['WHITE']), event=None):
        self.label = label
        self.font = font
        self.colors = colors
        self.pos = pos
        self.sel = False
        self.event = event

    def render(self, camera):
        if self.sel:
            if self.font != None:
                self.b = text(self.font, self.label, False, self.colors[0])
        else:
            if self.font != None:
                self.b = text(self.font, self.label, False, self.colors[1])
        self.rect = self.b.get_rect(center=self.pos)
        blit(camera, self.b, (self.rect[0]+self.b.get_width()/2, self.rect[1]+self.b.get_height()/2))

    def callEvent(self):
        if self.event != None:
            self.event()


class ImgButton(object):
    def __init__(self, pos, imgs, event=None):
        self.imgs = imgs
        self.pos = pos
        self.sel = False
        self.event = event

    def render(self, camera):
        if self.sel:
            self.b = self.imgs[0]
        else:
            self.b = self.imgs[1]
        self.rect = self.b.get_rect(center=self.pos)
        blit(camera, self.b, (self.rect[0]+self.b.get_width()/2, self.rect[1]+self.b.get_height()/2))

    def callEvent(self):
        if self.event != None:
            self.event()
            

class HUD(object):
    def __init__(self, actor):
        self.hp = float(actor.hp)
        self.full = float(actor.full)
        self.maxwidth = SCREEN_W/3

    def update(self, camera):
        if self.hp <= 0:
            self.hp = 0
        bar = surface((self.hp/self.full)*self.maxwidth, SCREEN_H/9)
        outl = surface(self.maxwidth+10, (SCREEN_H/9)+(SCREEN_H/(SCREEN_H*0.1)))
        bar.set_alpha(100)
        outl.set_alpha(100)

        outl.fill(Color(50, 100, 255))
        if self.hp <= self.full/2:
            bar.fill(B_COLORS['RED'])
        else:
            bar.fill(B_COLORS['CYAN'])

        blit(camera, outl, (SCREEN_W/2, 0))
        blit(camera, bar, (SCREEN_W/2, 0))


class TextScenes(object):
    def __init__(self, quotes, font, color=B_COLORS['YELLOW']):
        self.quotes = quotes
        self.font = font
        self.color = color
        self.index = 0
        self.counter = 0

    def render(self, camera, pos, delay, loop=False, center=False):
        line = self.quotes[self.index]
        self.counter += 1
        for n in range(len(line)):
            t = text(self.font, line[n], False, self.color)
            if not center:
                blit(camera, t, (pos[0], pos[1] + n * (self.font.get_height()+self.font.get_height()/2)), center=False)
            else:
                blit(camera, t, (pos[0], pos[1] + n * (self.font.get_height()+self.font.get_height()/2)))
            
        if self.counter%delay == 0:
            self.index += 1
            if self.index == len(self.quotes):
                if not loop:
                    self.index += 0
                    self.index = len(self.quotes)-1
                else:
                    self.index = 0
