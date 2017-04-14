## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;

### Testing Phase ###
import os
from pie.color import *
from constants import *
from resources import *
from state import *

class Editor(State):
    def __init__(self, engine):
        State.__init__(self, engine, 'Ship Editor')
        self.pixelSize = ((SCREEN_W/CANVAS_W)+(SCREEN_H/CANVAS_H))/4
        self.canvas = surface(CANVAS_W*self.pixelSize, CANVAS_H*self.pixelSize)
        self.saveShip()
        
    def render(self):
        self.handleEvents()
        self.screen.fill(Color(20, 20, 40))

        # Draw the canvas
        self.canvas.fill(B_COLORS['WHITE'])
        for x in range(self.canvas.get_width()/self.pixelSize):
            for y in range(self.canvas.get_height()/self.pixelSize):
                rect(self.canvas, B_COLORS['BLACK'], x*self.pixelSize, y*self.pixelSize, self.pixelSize, self.pixelSize, outline=1)

        TITLE = text(self.fonts['font'], self.name, False, B_COLORS['WHITE'])
        blit(self.screen, TITLE, (SCREEN_W/2, SCREEN_H/10))
        
        blit(self.screen, self.canvas, (SCREEN_W/2, SCREEN_H/2))

    def saveShip(self):
        filename = raw_input('Name of ship: ')
        filepath = os.mkdir('data/imgs/sprites/player/'+filename)
        final =  scale(self.canvas, (self.canvas.get_width()/self.pixelSize, self.canvas.get_height()/self.pixelSize))

        save('data/imgs/sprites/player/'+filename+'/idle.png', final)
        save('data/imgs/sprites/player/'+filename+'/player1.png', final)
        save('data/imgs/sprites/player/'+filename+'/player2.png', final)
        
