import pygame as pg
import sys
import random
import math

Screen = (1000, 600)
FPS = 60

player_damage = 5
professor_damage = 2

class Bullet_mun(pg.sprite.Sprite):
    def __init__(self, SCENE, x, y, speed, angle):
        pg.sprite.Sprite.__init__(self)
        self.radius = 6
        self.SCENE = SCENE
        self.image = pg.image.load('.assets.dessertation_1.png')
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

class Bullet_e(pg.sprite.Sprite):
    def __init__(self, SCENE, x, y, speed, angle):
        pg.sprite.Sprite.__init__(self)
        self.radius = 6
        self.SCENE = SCENE
        self.image = pg.image.load('.assets.dessertation_2.png')
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

class ProfessorBullet(Bullet_e):
	def __init__(self, SCENE, x, y, speed, angle):
		super().__init__(SCENE, x, y, speed, angle)
		self.image = pg.image.load('.assets.grade_c.png')

class Player(pg.sprite.Sprite):
	def __init__(self, SCENE, x, y):
		pg.sprite.Sprite.__init__(self)
		self.SCENE = SCENE
		self.radius = 20
		self.angle = 90
		self.original_image = pg.image.load('.player.png')
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.xspeed = 0
		self.last_launch = pg.time.get_ticks()
		self.health = 50

	def hit(self, player_damage):
		self.health -= player_damage
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

		self.image = self.original_image
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

	def hit(self, professor_damage):
		self.health -= professor_damage
		if self.health < 0:
			self.kill()

	def launch(self):
		if pg.time.get_ticks() - self.last_launch > 200: 
			self. SCENE.group_enemybullets.add(ProfessorBullet(self.SCENE, self.x, self.y((self.xspeed**2+self.yspeed**2)**0.5+100,), self.angle))
			self.last_launch = pg.time.get_ticks()

	def update(self):
		second_passed = self.SCENE.CLOCK.get_time()/1000
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.rect.center = (500, 300)


if __name__=="__main__":
	pg.mixer.pre_init(buffer=128)
	pg.init()
	window = pg.display.set_mode(Screen)
	clock = pg.time.Clock()
	player = Player()
	player_Group = pg.sprite.Group()
	player_Group.add(Player)
	professor_Group = pg.sprite.Group()
	bulletGroup = pg.sprite.Group()

	pg.mixer.set_num_channels(32)
	SOUND_shoot = pg.mixer.Sound('bullet.wav')
	pg.mixer.music.load('Gyoga.wav')
	pg.mixer.music.play(loops=-1)
	while True:
		window.fill((255,255,255))
		for event in pg.event.get():
			if event.type == pg.QUIT:
				pg.quit()
				sys.exit()
				break
		

		professor_Group.update()
		player.update()
		bulletGroup.update()
		professor_Group.draw(window)
		bulletGroup.draw(window)
		player_Group.draw(window)
		pg.display.flip()
		clock.tick(FPS)

		for bullet in ProfessorBullet:
			if pg.sprite.collide_mask(player, bullet):
				pg.event.post(pg)








        
