## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
import os

VER = "AstroJumper 1.0"
SCREEN_W = 1000
SCREEN_H = 600

CANVAS_W = 50
CANVAS_H = 17

LVL = [x for x in range(1, 51)]
XP = [y*132 for y in LVL]
LEVELS = dict(zip(LVL, XP))
SHIPS = {'Sword' : (SCREEN_W/100, 50, 0, 3, 0),
         'Falcon' : (SCREEN_W/66, 75, 7, 5, 10),
         'X7' : (SCREEN_W/58, 100, 14, 7, 15),
         'Mr. Dolphin' : (SCREEN_W/100, 150, 0, 15, 30)}
