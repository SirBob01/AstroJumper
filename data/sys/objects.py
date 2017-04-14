## AstroJumper;
## Copyright Keith Leonardo, RetroVision Gaming Corporation (c) 2013-2014;
import random
from pie.vector import *
from pie.physics import *
from pie.color import *
from constants import *
from resources import *
from gui import *

class HangarBay(Entity):
    def __init__(self):
        Entity.__init__(self, 'Hangar bay 7', SCREEN_W/2, SCREEN_H/2)
        self.base = image('data/imgs/menu/base.png', resize=(SCREEN_W, SCREEN_H))
        self.score = image('data/imgs/menu/scoreboard.png', resize=(SCREEN_W/5, SCREEN_H/5))
        self.speed = 0

    def update(self, camera, scroll=False):
        if self.alive:
            if scroll:
                if self.speed <= SCREEN_W * 0.02:
                    self.speed += 0.5
                self.vector.x -= self.speed
            blit(camera, self.base, self.vector)
            blit(camera, self.score, self.vector)
            if self.vector.x <= -(SCREEN_W*3):
                self.kill()

    def scoreboard(self, camera, score, font):
        high = text(font, 'Highscore:', False, B_COLORS['WHITE'])
        score = text(font, str(score), False, B_COLORS['WHITE'])
        blit(camera, high, (self.vector.x, self.vector.y-(self.vector.y/10)))
        blit(camera, score, (self.vector.x, self.vector.y-(self.vector.y/50)))


class ShipProfile(object):
    def __init__(self, skin, font, requiredLevel):
        self.skin = skin
        self.avatar = Player(self.skin)
        self.name = text(font, '{0} Fighter'.format(self.skin), False, B_COLORS['WHITE'])
        self.unlocked = True
        self.unlockLvl = requiredLevel
        self.selected = False
        
        # Ship stats
        self.full = 'Max HP: {0}'.format(SHIPS[self.skin][1])
        self.speed = 'Speed: {0}'.format(SHIPS[self.skin][0])
        self.overheat = 'Rate of Fire: {0}'.format(SHIPS[self.skin][3])
        self.text = TextScenes([[self.full, self.speed, self.overheat]], font)
        self.selectText = text(font, 'Selected', False, B_COLORS['GREEN'])
        self.locked = text(font, 'Reach level {0} to unlock'.format(self.unlockLvl), False, B_COLORS['WHITE'])
    
    def update(self, camera):
        self.text.render(camera, (SCREEN_W/4, SCREEN_H/2), 1)
        blit(camera, self.name, (SCREEN_W/2, SCREEN_H/2-(SCREEN_H/6)))
        self.avatar.display(camera, SCREEN_W/2+(SCREEN_W/8), SCREEN_H/2)
        if not self.unlocked:
            blit(camera, self.locked, (SCREEN_W/2, SCREEN_H/4))
        

class Player(AABB):
    def __init__(self, skin):
        AABB.__init__(self, SCREEN_W/5, SCREEN_H-(SCREEN_H/3), SCREEN_W/5, SCREEN_H/7, name='Player')
        self.images = [image('data/imgs/sprites/player/' + skin + '/player1.png', resize=(self.width, self.height)),
                       image('data/imgs/sprites/player/' + skin + '/player2.png', resize=(self.width, self.height))]
        self.still = image('data/imgs/sprites/player/' + skin + '/idle.png', resize=(self.width, self.height))
        self.shieldSprite = image('data/imgs/environment/shield.png', resize=(self.width+(self.width/3), self.height+(self.height/3)))
        self.skin = skin
        self.score = 0
        self.xp = 0
        self.shots = 0
        self.reloadTime = 0
        self.shield = False
        self.abilityTimer = 500
        self.state = 'idle'
        
        # Ship stats
        if SHIPS.has_key(self.skin):
            self.speed = SHIPS[self.skin][0]
            self.hp = SHIPS[self.skin][1]
            self.full = SHIPS[self.skin][1]
            self.overheat = SHIPS[self.skin][3]
        else:
            self.speed = SHIPS['DEFAULT'][0]
            self.hp = SHIPS['DEFAULT'][1]
            self.full = SHIPS['DEFAULT'][1]
            self.overheat = SHIPS['DEFAULT'][3]

        self.anim = Animate()
        
    def update(self, camera):
        self.hp = min([self.hp, self.full])
        self.anim.animate(camera, self.images, self.vector, speed=10)
        if self.state == 'left':
            self.vector.x -= self.speed
        if self.state == 'right':
            self.vector.x += self.speed
        if self.state == 'up':
            self.vector.y -= self.speed
        if self.state == 'down':
            self.vector.y += self.speed

        ## Screen bounds
        if self.vector.x >= SCREEN_W-(self.width/2):
            self.vector.x = SCREEN_W-(self.width/2)
        if self.vector.x <= (self.width/2):
            self.vector.x = (self.width/2)
        if self.vector.y >= SCREEN_H-(self.height/2):
            self.vector.y = SCREEN_H-(self.height/2)
        if self.vector.y <= (self.height/2):
            self.vector.y = (self.height/2)

        if self.shield:
            blit(camera, self.shieldSprite, self.vector)
            self.abilityTimer -= 1
            if self.abilityTimer <= 0:
                self.abilityTimer = 500
                self.shield = False
            
        HUD(self).update(camera)

    def display(self, camera, x, y):
        self.anim.animate(camera, self.images, Vector(x, y), speed=10)

    def idle(self, camera):
        blit(camera, self.still, self.vector)


class Enemy(AABB):
    def __init__(self):
        AABB.__init__(self, SCREEN_W+(SCREEN_W/4), random.randint(SCREEN_H/8, SCREEN_H-(SCREEN_H/8)), SCREEN_W/5, SCREEN_H/7, name='Xygrath')
        self.images = [image('data/imgs/sprites/enemy/e1.png', resize=(self.width, self.height)),
                       image('data/imgs/sprites/enemy/e2.png', resize=(self.width, self.height))]
        self.speed = random.randint(SCREEN_W/200, SCREEN_W/76)
        self.state = 'idle'
        self.anim = Animate()

    def update(self, camera):
        self.anim.animate(camera, self.images, self.vector, speed=10)
        self.vector.x -= self.speed
        if random.randint(0, 50) == 1:
            self.state = 'shoot'
        else:
            self.state = 'moving'
        if self.vector.x <= -300:
            self.kill()


class Red(AABB):
    def __init__(self, actor):
        AABB.__init__(self, actor.vector.x, actor.vector.y, (SCREEN_W/2)/10, SCREEN_H/60, name='Red Lazer')
        self.image = image('data/imgs/sprites/lasers/red.png', resize=(self.width, self.height))
        self.speed = SCREEN_W/50

    def update(self, camera):
        blit(camera, self.image, self.vector)
        self.vector.x -= self.speed
        if self.vector.x < -100:
            self.kill()


class Blue(AABB):
    def __init__(self, actor):
        AABB.__init__(self, actor.vector.x, actor.vector.y, (SCREEN_W/2)/10, SCREEN_H/60, name='Blue Lazer')
        self.image = image('data/imgs/sprites/lasers/blue.png', resize=(self.width, self.height))
        self.speed = SCREEN_W/50

    def update(self, camera):
        blit(camera, self.image, self.vector)
        self.vector.x += self.speed
        if self.vector.x > SCREEN_W+(SCREEN_W/4):
            self.kill()


class HealthPack(AABB):
    def __init__(self):
        AABB.__init__(self, SCREEN_W+(SCREEN_W/4), random.randint(SCREEN_H/8, SCREEN_H-(SCREEN_H/8)), SCREEN_W/25, SCREEN_W/25, name='HP')
        self.image = image('data/imgs/environment/hp1.png', resize=(self.width, self.height))
        self.speed = SCREEN_W/200

    def update(self, camera):
        blit(camera, self.image, self.vector)
        self.vector.x -= self.speed
        if self.vector.x <= -300:
            self.kill()


class ShieldPack(AABB):
    def __init__(self):
        AABB.__init__(self, SCREEN_W+(SCREEN_W/4), random.randint(SCREEN_H/8, SCREEN_H-(SCREEN_H/8)), SCREEN_W/25, SCREEN_W/25, name='SP')
        self.images = [image('data/imgs/environment/sp1.png', resize=(self.width, self.height)),
                       image('data/imgs/environment/sp2.png', resize=(self.width, self.height)),
                       image('data/imgs/environment/sp3.png', resize=(self.width, self.height))]
        self.speed = SCREEN_W/200
        self.anim = Animate()

    def update(self, camera):
        self.anim.animate(camera, self.images, self.vector, speed=10, loop=True)
        self.vector.x -= self.speed
        if self.vector.x <= -300:
            self.kill()
        

class Explosion(Entity):
    def __init__(self, actor):
        Entity.__init__(self, 'Boom!', actor.vector.x, actor.vector.y)
        self.images = [image('data/imgs/environment/explosion1.png', resize=(SCREEN_W/5, SCREEN_W/5)),
                       image('data/imgs/environment/explosion2.png', resize=(SCREEN_W/5, SCREEN_W/5)),
                       image('data/imgs/environment/explosion3.png', resize=(SCREEN_W/5, SCREEN_W/5))]
        self.anim = Animate()

    def update(self, camera):
        self.anim.animate(camera, self.images, self.vector, speed=10, loop=False)
        if self.anim.index >= len(self.images)-1:
            self.kill()


class Collect(Entity):
    def __init__(self, actor):
        Entity.__init__(self, 'Kling!', actor.vector.x, actor.vector.y)
        self.images = [image('data/imgs/environment/collect1.png', resize=(SCREEN_W/25, SCREEN_W/25)),
                       image('data/imgs/environment/collect2.png', resize=(SCREEN_W/25, SCREEN_W/25))]
        self.anim = Animate()

    def update(self, camera):
        self.anim.animate(camera, self.images, self.vector, speed=10, loop=False)
        if self.anim.index >= len(self.images)-1:
            self.kill()
