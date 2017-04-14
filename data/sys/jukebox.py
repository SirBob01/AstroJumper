## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
from resources import *

SOUNDS = {'ambience' : 'Space.ogg',
          'boom' : 'boom.ogg',
          'click' : 'click.ogg',
          'shoot' : 'laser.ogg',
          'menu' : 'menu.ogg',
          'main' : 'main.ogg'}

# Audio engine
class JukeBox(object):
    def __init__(self):
        self.files = SOUNDS
        self.playing = None
        self.volume = 1.0

    def play(self, name, volume=1.0, loop=False, music=False):
        self.volume = volume
        if music:
            self.playing = sound(self.files[name], music=True)
        else:
            self.playing = sound(self.files[name])
            self.playing.set_volume(self.volume)
            
        if loop:
            if music:
                playmusic(True)
            else:
                self.playing.play(-1)
                
        else:
            if music:
                playmusic()
            else:
                self.playing.play()

    def stop(self):
        self.playing.stop()

    def pause(self):
        self.playing.pause()

    def mute(self):
        self.volume = 0.0
        self.playing.set_volume(self.volume)
    
