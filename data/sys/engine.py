## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
import pygame, sys
from pygame.locals import *
from pie.color import *
from constants import *
from states import *
from gprofile import *
from jukebox import *
from gui import *

class Engine(object):
    def __init__(self):
        self.running = True
        self.init()

    def init(self):
        pygame.init()

        # Display settings
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), 0, 32)
        pygame.display.set_caption('AstroJumper')
        self.clock = pygame.time.Clock()
        
        self.fonts = {'font'  : font('Puke-Force-8.ttf', SCREEN_W/15),
                      'small' : font('Puke-Force-8.ttf', SCREEN_W/20),
                      'large' : font('Puke-Force-8.ttf', SCREEN_W/10)}
        self.juke = JukeBox()
        self.profile = Profile()
        self.state = MainMenu(self)

    def mainloop(self):
        self.juke.play('ambience', loop=True, music=True)
        self.profile.save()
        while self.running:
            self.screen.fill(B_COLORS['BLACK'])
            self.profile.parse()
            self.state.render()
                
            self.clock.tick(50) # FPS limit
            pygame.display.update()

        pygame.quit()
        sys.exit()

    def quitGame(self):
        self.running = False
