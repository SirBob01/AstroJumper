## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
import os
from constants import *

class Profile(object):
    def __init__(self):
        if ('game.sav' in os.listdir('data/saves')) == False:
            self.file = open('data/saves/game.sav', 'wb')
            self.high = 0
            self.level = 1
            self.xp = 0
            self.ships = 1
            self.skin = 'Sword'
            self.save()
        else:
            self.load()
                    
    def open(self):
        self.file = open('data/saves/game.sav', 'r+')
        
    def close(self):
        self.file.close()

    def load(self):
        self.open()
        for e in self.file.readlines():
            if e.startswith('h '):
                self.high = int(e[1:].strip('\n'))
            if e.startswith('l '):
                self.level = int(e[1:].strip('\n'))
            if e.startswith('xp '):
                self.xp = int(e[2:].strip('\n'))
            if e.startswith('s '):
                self.ships = int(e[1:].strip('\n'))
            if e.startswith('k '):
                self.skin = (e[2:].strip('\n'))
        self.close()

    def save(self):
        self.open()
        self.file.write('h '+str(int(self.high))+'\n')
        self.file.write('l '+str(int(self.level))+'\n')
        self.file.write('xp '+str(int(self.xp))+'\n')
        self.file.write('s '+str(int(self.ships))+'\n')
        self.file.write('k '+str(self.skin+'\n'))
        self.close()

    def parse(self):
        if self.level >= len(LEVELS)-1:
            self.level = len(LEVELS)-1
            self.xp = LEVELS[self.level]
        if self.xp >= LEVELS[self.level]:
            self.xp = 0
            self.level += 1
        if self.level%10 == 0:
            self.ships += 1
        self.ships = min(self.ships, len(SHIPS.keys()))
        self.ships = max(self.ships, 1)
        self.save()
