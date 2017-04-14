## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
import os, operator
from pie.color import *
from resources import *
from state import *
from gui import *
from world import *

class Opening(State):
    def __init__(self, engine):
        State.__init__(self, engine, 'Loading...')
        self.rv = image('data/help/logo.png', resize=(SCREEN_W/2, SCREEN_H/5))
        self.pie = image('data/sys/pie/logo.png', resize=(SCREEN_W/3, SCREEN_H/4))
        self.pygame = image('data/sys/pygame/docs/pygame_powered.gif', resize=(SCREEN_W/3, SCREEN_H/5))
        self.powered = text(self.fonts['font'], 'Powered by...', False, B_COLORS['WHITE'])
        self.counter = 0
        
    def render(self):
        self.handleEvents()
        self.counter += 1
        
        if self.counter <= 180:
            blit(self.screen, self.powered, (SCREEN_W/4, SCREEN_H/2-(SCREEN_H/5)))
            blit(self.screen, self.pie, (SCREEN_W/4, SCREEN_H/2))
            blit(self.screen, self.pygame, (SCREEN_W-(SCREEN_W/4), SCREEN_H/2))
        elif self.counter >= 250 and self.counter <= 500:
            blit(self.screen, self.rv, (SCREEN_W/2, SCREEN_H/3))
        elif self.counter > 510:
            self.engine.state = MainMenu(self.engine)


class MainMenu(State):
    def __init__(self, engine):
        State.__init__(self, engine, 'Main menu')
        self.logo = image('data/imgs/menu/title.png', resize=(SCREEN_W/2, SCREEN_H/3))
        self.banner = text(self.fonts['font'], 'PRESS SPACEBAR TO LAUNCH', False, B_COLORS['WHITE'])
        self.banner_transparent = 255
        self.skin = self.engine.profile.skin
        self.base = HangarBay()

        self.buttons.append(Button((SCREEN_W/10, SCREEN_H/6), label='GARAGE', font=self.fonts['font'], event=self.garage))
        self.buttons.append(Button((SCREEN_W/10, SCREEN_H/4), label='STATS', font=self.fonts['font'], event=self.stats))
        self.buttons.append(Button((SCREEN_W/10, SCREEN_H/3), label='CREDITS', font=self.fonts['font'], event=self.creds))
        
    def render(self):
        self.base.update(self.screen)
        self.base.scoreboard(self.screen, int(self.engine.profile.high), self.fonts['small'])
        self.handleEvents()
        
        self.banner.set_alpha(self.banner_transparent)
        if self.banner_transparent >= 0:
            self.banner_transparent -= 5
        else:
            self.banner_transparent = 255
            
        blit(self.screen, self.logo, (SCREEN_W/2, SCREEN_H/5))
        blit(self.screen, self.banner, (SCREEN_W/2, SCREEN_H-(SCREEN_H/4)))
        Player(self.skin).idle(self.screen)

        if self.active == self.events['space']:
            self.engine.state = Play(self.engine, Player(self.skin))

    def garage(self): self.engine.state = Garage(self.engine)
    def stats(self): self.engine.state = Stats(self.engine)
    def creds(self): self.engine.state = Credits(self.engine)


class Garage(State):
    def __init__(self, engine):
        State.__init__(self, engine, 'Garage')
        self.ships = [ShipProfile(i, self.fonts['font'], SHIPS[i][4]) for i in SHIPS.keys()]
        self.ships.sort(key=operator.attrgetter('unlockLvl'))
        
        self.shipIndex = 0
        self.current = self.ships[self.shipIndex]

        self.buttons.append(Button((SCREEN_W/2, SCREEN_H-(SCREEN_H/10)), label='BACK', font=self.fonts['font'], event=self.menu))
        self.buttons.append(ImgButton((SCREEN_W/8, SCREEN_H/2), imgs=[flip(image('data/imgs/menu/arrowb.png', resize=(SCREEN_W/20+(SCREEN_W/20)/4, SCREEN_H/12+(SCREEN_H/12)/4)), True, False), flip(image('data/imgs/menu/arrowb.png', resize=(SCREEN_W/20, SCREEN_H/12)), True, False)], event=self.prevS))
        self.buttons.append(ImgButton((SCREEN_W-SCREEN_W/8, SCREEN_H/2), imgs=[image('data/imgs/menu/arrowb.png', resize=(SCREEN_W/20+(SCREEN_W/20)/4, SCREEN_H/12+(SCREEN_H/12)/4)), image('data/imgs/menu/arrowb.png', resize=(SCREEN_W/20, SCREEN_H/12))], event=self.nextS))

    def render(self):
        self.screen.fill(Color(20, 20, 40))
        self.handleEvents()

        for s in self.ships:
            if s.unlockLvl > self.engine.profile.level and s == self.current:
                s.unlocked = False
            else:
                self.engine.profile.skin = self.current.skin
                    
        if self.shipIndex < 0:
            self.shipIndex = len(self.ships)-1
        if self.shipIndex > len(self.ships)-1:
            self.shipIndex = 0
            
        self.current = self.ships[self.shipIndex]
        self.current.update(self.screen)
        
        
        TITLE = text(self.fonts['font'], self.name, False, B_COLORS['WHITE'])
        blit(self.screen, TITLE, (SCREEN_W/2, SCREEN_H/10))

    def menu(self): self.engine.state = MainMenu(self.engine)
    def prevS(self): self.shipIndex -= 1
    def nextS(self): self.shipIndex += 1
    

class Stats(State):
    def __init__(self, engine):
        State.__init__(self, engine, 'Statistics')
        self.highscore = int(self.engine.profile.high)
        self.level = int(self.engine.profile.level)
        self.xp = int(self.engine.profile.xp)
        
        self.buttons.append(Button((SCREEN_W/2, SCREEN_H-(SCREEN_H/10)), label='BACK', font=self.fonts['font'], event=self.menu))

    def render(self):
        self.screen.fill(Color(20, 20, 40))
        self.handleEvents()

        TITLE = text(self.fonts['font'], self.name, False, B_COLORS['WHITE'])
        HIGH = text(self.fonts['font'], 'Highscore: '+str(self.highscore), False, B_COLORS['YELLOW'])
        LEVEL = text(self.fonts['font'], 'Level: '+str(self.level), False, B_COLORS['YELLOW'])
        XP = text(self.fonts['small'], 'XP: '+str(self.xp)+'/'+str(LEVELS[self.level]), False, B_COLORS['YELLOW'])
        blit(self.screen, TITLE, (SCREEN_W/2, SCREEN_H/10))
        blit(self.screen, HIGH, (SCREEN_W/2, SCREEN_H/4))
        blit(self.screen, LEVEL, (SCREEN_W/2, SCREEN_H*0.45))
        blit(self.screen, XP, (SCREEN_W/2, SCREEN_H-SCREEN_H*0.43))

        rect(self.screen, B_COLORS['CYAN'], SCREEN_W/2-(SCREEN_W/3)/2, SCREEN_H/2, SCREEN_W/3, 15, outline=10)
        rect(self.screen, Color(50, 50, 50), SCREEN_W/2-(SCREEN_W/3)/2, SCREEN_H/2, SCREEN_W/3, 15)
        rect(self.screen, B_COLORS['GREEN'], SCREEN_W/2-(SCREEN_W/3)/2, SCREEN_H/2, (float(self.xp)/float(LEVELS[self.level]))*SCREEN_W/3, 15)

    def menu(self): self.engine.state = MainMenu(self.engine)

    
class Credits(State):
    def __init__(self, engine):
        State.__init__(self, engine, 'Credits')
        self.logo = image('data/imgs/menu/title.png', resize=(SCREEN_W/2, SCREEN_H/3))
        self.lines = [['Programming and sprites by Keith Leonardo',
                       'Copyright Keith Leonardo, RetroVision Corp. (c) 2013-2014'],
                      ['Powered by Pygame and PIE physics engine',
                       'Written in Python 2.7']]
        self.creds = TextScenes(self.lines, self.fonts['font'], color=B_COLORS['WHITE'])

        self.buttons.append(Button((SCREEN_W/2, SCREEN_H-(SCREEN_H/8)), label='BACK', font=self.fonts['font'], event=self.menu))
        
    def render(self):
        self.screen.fill(Color(20, 20, 40))
        self.handleEvents()

        blit(self.screen, self.logo, (SCREEN_W/2, SCREEN_H/5))
        self.creds.render(self.screen, (SCREEN_W/2, SCREEN_H/2), 100, loop=True, center=True)

    def menu(self): self.engine.state = MainMenu(self.engine)


class Play(State):
    def __init__(self, engine, player):
        State.__init__(self, engine, 'Game on!')
        self.world = PlayField(player, self.engine)
        self.base = HangarBay()
        self.player = self.world.player
        self.newhigh = False
        self.prevhigh = self.engine.profile.high

    def render(self):
        self.handleEvents()
        self.starfield.update(self.screen, scroll=self.player.alive)
        self.base.update(self.screen, scroll=True)
        self.base.scoreboard(self.screen, int(self.engine.profile.high), self.fonts['small'])
        self.world.update(self.screen)
        self.world.spawn_entities(self.screen)

        if self.player.alive:
            # Handle all actions of the player
            for e in self.events.keys():
                if self.active == self.events[e]:
                    self.world.player.state = e

            # When the weapon overheats...
            over = text(self.fonts['font'], 'WEAPON RELOADING!', False, B_COLORS['RED'])
            if self.player.shots == self.player.overheat:
                blit(self.screen, over, (SCREEN_W/2, SCREEN_H/3))
                if self.player.reloadTime < 100:
                    self.player.reloadTime += 1
                else:
                    self.player.reloadTime = 0
                    self.player.shots = 0
                    
            self.player.score += 0.25
            blit(self.screen, text(self.fonts['font'], str(int(self.player.score)), False, B_COLORS['YELLOW']), (SCREEN_W/2, SCREEN_H/8))
        else:
            self.counter += 1
            if self.counter >= 200:
                self.engine.state = GameOver(self.engine, self.player.score, self.player.skin, high=self.newhigh)
                self.counter = 0

        ### Update the player's profile ###
        if self.player.score > self.engine.profile.high:
            self.newhigh = True
            self.engine.profile.high = self.player.score
            if self.prevhigh != 0:
                blit(self.screen, text(self.fonts['font'], 'New Highscore!', False, B_COLORS['WHITE']), (SCREEN_W/2, SCREEN_H/5))

        self.engine.profile.xp += self.player.xp
        self.engine.profile.save()


class GameOver(State):
    def __init__(self, engine, score, player_skin, high=False):
        State.__init__(self, engine, 'Game over!')
        self.score = int(score)
        self.newhigh = high
        self.player = player_skin

        self.buttons.append(Button((SCREEN_W/3, SCREEN_H-(SCREEN_H/8)), label='MAINMENU', font=self.fonts['font'], event=self.menu))
        self.buttons.append(Button((SCREEN_W-(SCREEN_W/3), SCREEN_H-(SCREEN_H/8)), label='RETRY', font=self.fonts['font'], event=self.retry))

    def render(self):
        self.handleEvents()
        blit(self.screen, text(self.fonts['large'], 'SCORE: {0}'.format(self.score), False, B_COLORS['WHITE']), (SCREEN_W/2, SCREEN_H/4))
        if self.newhigh:
            blit(self.screen, text(self.fonts['large'], 'NEW HIGHSCORE!', False, B_COLORS['YELLOW']), (SCREEN_W/2, SCREEN_H/2))
        
    def menu(self): self.engine.state = MainMenu(self.engine)
    def retry(self): self.engine.state = Play(self.engine, Player(self.player))
