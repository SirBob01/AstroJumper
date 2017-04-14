## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
import random
from pie.physics import *
from pie.color import *
from constants import *
from resources import *
from objects import *
from space import *

class PlayField(object):
    def __init__(self, player, engine):
        self.engine = engine
        self.entities = []
        self.player = player
        self.entities.append(self.player)

        self.flash = surface(SCREEN_W, SCREEN_H)
        self.flashA = 0

    def spawn_entities(self, camera):
        if randint(0, 75) == 1:
            self.entities.append(Enemy())
        if randint(0, 1000) == 1:
            self.entities.append(HealthPack())
        if randint(0, 1000) == 1:
            self.entities.append(ShieldPack())

    
    def update(self, camera):
        self.flash.fill(B_COLORS['WHITE'])
        self.flash.set_alpha(self.flashA)
        if self.flashA > 0:
            self.flashA -= 5
        else:
            self.flashA = 0
        blit(camera, self.flash, (SCREEN_W/2, SCREEN_H/2))
        ### Entity relationships... 
        for e in self.entities:
            if e.alive:
                e.update(camera)
                
                if e.name == 'Player':
                    if e.hp <= 0:
                        e.hp = 0
                        e.kill()
                        Explosion(e).update(camera)
                        self.engine.juke.play('boom')
                    if e.state == 'shoot':
                        self.entities.append(Blue(e))
                        self.engine.juke.play('shoot')
                if e.name == 'Xygrath':
                    if randint(0, 30) == 1:
                        self.entities.append(Red(e))
                        self.engine.juke.play('shoot')
                        
                for e2 in self.entities:
                    if e  == e2: continue
                    if e2.alive:
                        if e.name == 'Red Lazer' and e2.name == 'Player' and collideAABB(e, e2):
                            e.kill()
                            if e2.shield != True:
                                e2.hp -= 15
                            self.entities.append(Explosion(e))
                            self.engine.juke.play('boom')
                        if e.name == 'Blue Lazer' and e2.name == 'Xygrath' and collideAABB(e, e2):
                            e.kill()
                            e2.kill()
                            self.entities.append(Explosion(e2))                            
                            self.player.xp += 7
                            self.engine.juke.play('boom')
                        if e.name == 'Player' and e2.name == 'Xygrath' and collideAABB(e, e2):
                            if e.shield == True:
                                e.shield = False
                            else:
                                e.kill()
                                self.entities.append(Explosion(e))
                                self.engine.juke.play('boom')
                            e2.kill()
                            self.entities.append(Explosion(e2))
                            self.player.xp += 7
                            self.engine.juke.play('boom')
                        if e.name == 'Player' and e2.name == 'HP' and collideAABB(e, e2):
                            e2.kill()
                            self.flashA = 255
                            e.hp += 15
                        if e.name == 'Player' and e2.name == 'SP' and collideAABB(e, e2):
                            e2.kill()
                            self.entities.append(Collect(e2))
                            e.shield = True
