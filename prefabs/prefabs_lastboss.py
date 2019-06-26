import pygame as pg
import random
import math

hakgua = 'mun'

class Bullet(pg.sprite.Sprite):
    def __init__(self, SCENE, x, y, speed, angle):
        pg.sprite.Sprite.__init__(self)
        self.SCENE = SCENE
        self.image = pg.transform.scale(pg.image.load('./assets/dissertation_1.png'),(64,64))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.angle = 90
        self.xspeed = speed
        self.yspeed = speed
        self.rect.center = (int(self.x), int(self.y))

    def update(self):
        self.yspeed -= 1
        self.rect.centery += self.yspeed
        if self.rect.centery <= 0:
            self.kill()

class ProfessorBullet(Bullet):
    def __init__(self, SCENE, x, y, speed, angle):
        super().__init__(SCENE, x, y, speed, angle)
        if random.randint(1,3) == 1:
            self.image = pg.transform.scale(pg.image.load('./assets/grade_c.png'),(64,64))
        elif random.randint(1, 3) == 2:
            self.image = pg.transform.scale(pg.image.load('./assets/grade_d.png'),(64,64))
        else:
            self.image = pg.transform.scale(pg.image.load('./assets/grade_f.png'),(64,64))
        self.speed = speed
        self.angle = angle
    def update(self):
        second_passed = self.SCENE.CLOCK.get_time()/1000
        self.rect.centerx += self.speed*second_passed*math.cos(math.radians(self.angle))
        self.rect.centery += self.speed*second_passed*math.sin(math.radians(self.angle))
        if self.rect.centery <= 0:
            self.kill()

class Player(pg.sprite.Sprite):
    def __init__(self, SCENE, x, y, angle):
        pg.sprite.Sprite.__init__(self)
        self.SCENE = SCENE
        self.angle = 90
        self.original_image = pg.image.load('./assets/avatar.png')
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.xspeed = 50
        self.last_launch = pg.time.get_ticks()
        self.health = 50
            
    def launch(self):
        if pg.time.get_ticks() - self.last_launch > 100:
            self.SCENE.group_playerbullets.add(Bullet(self.SCENE, self.x, self.y, self.xspeed/1000, self.angle))
            self.last_launch = pg.time.get_ticks()

    def update(self): 
        second_passed = self.SCENE.CLOCK.get_time()/1000
        if pg.key.get_focused:
            if pg.key.get_pressed()[pg.K_SPACE]:
                self.launch()
            if pg.key.get_pressed()[pg.K_a]:
                if self.xspeed > -150:
                    self.xspeed -= 300*second_passed
            if pg.key.get_pressed()[pg.K_d]:
                if self.xspeed < 150:
                    self.xspeed += 300*second_passed

        if self.xspeed > 0:
            self.xspeed -= 50*second_passed
        elif self.xspeed < 0:
            self.xspeed += 50*second_passed

        self.x += second_passed*self.xspeed

        if self.x < 16:
            self.x = 16
        if self.x > self.SCENE.WINDOW.get_size()[0] - 16:
            self.x = self.SCENE.WINDOW.get_size()[0] - 16

        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.x), int(self.y))
        
class Professor(pg.sprite.Sprite):
    def __init__(self, SCENE, x, y, angle):
        pg.sprite.Sprite.__init__(self)
        self.SCENE = SCENE
        self.angle = 90
        self.original_image = pg.image.load('./assets/avatar_professor.png')
        self.image = pg.transform.rotate(self.original_image, 90)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.last_launch = pg.time.get_ticks()
        self.health = 100

    def launch(self):
        self.SCENE.group_bullets.add(ProfessorBullet(self.SCENE, self.x, self.y, 100, random.randint(30, 150)))
        self.last_launch = pg.time.get_ticks()

    def update(self):
        second_passed = self.SCENE.CLOCK.get_time()/1000
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.x), int(self.y))
        if self.last_launch+1000 <= pg.time.get_ticks():
            self.launch()
