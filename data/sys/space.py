## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
from random import *
from pie.entity import *
from pie.color import *
from constants import *
from resources import *

        
class Star(Entity):
    def __init__(self):
        Entity.__init__(self, "Star", randint(0, SCREEN_W), randint(0, SCREEN_H))
        self.size = randint(SCREEN_W/SCREEN_W, SCREEN_H/200)
        self.image = surface(self.size, self.size)
        
    def update(self, camera):
        self.image.fill(B_COLORS['WHITE'])
        blit(camera, self.image, self.vector)
        

class StarField:
    def __init__(self):
        self.stars = []
        self.speed = 0
        for e in range(100):
            self.stars.append(Star())

    def update(self, camera, scroll=False):
        for s in self.stars:
            s.update(camera)
            if scroll:
                if self.speed <= SCREEN_W * 0.02:
                    self.speed += 0.005
                s.vector.x -= self.speed
                if s.vector.x <= 0:
                    s.vector.x = SCREEN_W
