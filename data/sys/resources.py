## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
import pygame

# Resource handling functions
def image(filename, resize=None):
    image = pygame.image.load(filename).convert_alpha()
    if resize is not None:
        image = pygame.transform.scale(image, resize)
    return image
        
def sound(filename, music=False):
    if music is True:
        sound = pygame.mixer.music.load('data/sounds/' + filename)
    else:
        sound = pygame.mixer.Sound('data/sounds/' + filename)
    return sound

def playmusic(loop=False):
    if loop:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()

def font(filename, size=60):
    f = pygame.font.Font("data/font/" + filename, size)
    return f

def text(font, text, aa, color):
    t = font.render(text, aa, color)
    return t

def surface(w, h):
    surf = pygame.Surface((w, h))
    return surf

def blit(display, surface, pos, center=True):
    if center:
        display.blit(surface, (pos[0]-surface.get_width()/2, pos[1]-surface.get_height()/2))
    else:
        display.blit(surface, pos)

def rotate(surf, angle):
    return pygame.transform.rotate(surf, angle)

def scale(surf, size):
    return pygame.transform.scale(surf, size)

def save(filename, surf):
    pygame.image.save(surf, filename)

def flip(surf, xr, yr):
    return pygame.transform.flip(surf, xr, yr)

def rect(display, color, x, y, width, height, outline=0):
    pygame.draw.rect(display, color, (x, y, width, height), outline)

def circle(display, color, x, y, size, outline=0):
    pygame.draw.circle(display, color, (x, y), size, outline)

def oblong(display, color, x, y, width, height, outline=0):
    pygame.draw.rect(display, color, (x, y, width, height), outline)

def line(display, color, start, end, blend=0):
    pygame.draw.aaline(display, color, start, end, blend)

def screenshot(surf, filename):
    pygame.image.save(surf, filename)


class Animate:
    def __init__(self):
        self.opaque = 255
        self.transparent = 0
        self.index = 0
        self.time = 0
        
    def animate(self, camera, imgs, pos, speed, loop=True):
        current = imgs[self.index]

        self.time += 1
        if self.time%speed == 0:
            self.index += 1

        if self.index > len(imgs)-1:
            if loop:
                self.index = 0
            else:
                self.index += 0
                self.index = len(imgs)-1

        blit(camera, current, pos)

    def fade_in(self, camera, img, pos, rate, center=True):
        img.set_alpha(self.transparent)
        if self.transparent < 255:
            self.transparent += rate
        blit(camera, img, pos, center)

    def fade_out(self, camera, img, pos, rate, center=True):
        img.set_alpha(self.opaque)
        if self.opaque > 0:
            self.opaque -= rate
        blit(camera, img, pos, center)    
