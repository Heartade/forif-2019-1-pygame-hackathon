import pygame as pg
import sys
import random
import math

Screen = (1000, 600)
FPS = 60

class Bullet(pg.sprite.Sprite):
    def __init__(self, SCENE, x, y, speed):
        pg.sprite.Sprite.__init__(self)
        self.radius = 6
        self.SCENE = SCENE
        self.image = pg.transform.rotate(pg.image.load('.missile.png'))
        self.destroy_image = pg.image.load('')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.xspeed = speed
        self.yspeed = speed
        self.rect.center = (int(self.x), int(self.y))

    def update(self):
    	if self.x < 0 or self.x > self.SCENE.WINDOW.get_size()[0]:
    		self.kill()
    	if self.y < 0 or self.y > self.SCENE.WINDOW.get_size()[1]:
    		self.kill()
    	self.rect.center = (int(self.x), int(self.y))

class ProfessorBullet(Bullet):
	def __init__(self, SCENE, x, y, speed):
		super().__init__(SCENE, x, y, speed)
		self.image = pg.transform.rotate(pg.image.load('.missile.png'))

class Player(pg.sprite.Sprite):
	def __init__(self, SCENE, x, y):
		pg.sprite.Sprite.__init__(self)
		self.SCENE = SCENE
		self.radius = 20
		self.angle = 90
		self.original_image = pg.image.load('.player.png')
		self.image = pg.transform.rotate(self.original_image, self.angle)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.xspeed = 0
		self.yspeed = 0
		self.last_launch = pg.time.get_ticks()
		self.health = 50

	def hit(self, damage):
		self.health -= damage
		if self.health < 0:
			self.kill()
			
	def launch(self):
		if pg.time.get_ticks() - self.last_launch > 100:
			self.SCENE.group_playerbullets.add(Bullet(self.SCENE, self.x, self.y, ((self.xspeed**2+self.yspeed**2)**0.5+100)))
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
				if self.xspeed < -150:
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

		self.image = pg.transform.rotate(self.original_image, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = (int(self.x), int(self.y))

class Professor(pg.sprite.Sprite):
	def __init__(self, SCENE, x, y):
		pg.sprite.Sprite.__init__(self)
		self.SCENE = SCENE
		self.radius = 16
		self.angle = 0
		self.original_image = pg.image.load('.Professor.png')
		self.rect = self.image.get_rect()
		self.x = 500
		self.y = 300
		self.last_launch = pg.time.get_ticks()
		self.health = 100








        
