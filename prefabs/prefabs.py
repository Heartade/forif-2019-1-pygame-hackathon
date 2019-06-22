import pygame as pg
import sys
import random
import math



class FadeEffect(pg.sprite.Sprite):
  def __init__(self, SCENE, init_alpha, rect, image, life):
    pg.sprite.Sprite.__init__(self)
    self.SCENE = SCENE
    self.original_image = image.copy()
    self.rect = self.original_image.get_rect()
    self.rect.center = rect.center
    self.image = image.copy()
    self.init_alpha = init_alpha
    self.alpha = init_alpha
    self.life = life
  def update(self):
    second_passed = self.SCENE.CLOCK.get_time()/1000
    self.alpha -= self.init_alpha*second_passed/self.life
    self.image = self.original_image.copy()
    if self.alpha < 0:
      self.kill()
      return
    self.image.fill((255,255,255,int(self.alpha)),special_flags=pg.BLEND_RGBA_MULT)
    
class DestroyEffect(FadeEffect):
  def __init__(self, SCENE, init_alpha, rect, image, life, scale=1):
    super().__init__(SCENE, init_alpha, rect, image, life)
    rect = self.rect
    self.original_image = pg.transform.scale(self.original_image, (int(rect.width*scale),int(rect.height*scale)))
    self.image = self.original_image.copy()
    self.rect = self.image.get_rect()
    self.rect.center = rect.center
  def update(self):
    second_passed = self.SCENE.CLOCK.get_time()/1000
    self.alpha -= self.init_alpha*second_passed/self.life
    rect = self.rect
    self.image = pg.transform.scale(self.original_image, (int(rect.width*(1+2*second_passed/self.life)),int(rect.height*(1+2*second_passed/self.life))))
    self.rect = self.image.get_rect()
    self.rect.center = rect.center
    if self.alpha < 0:
      self.kill()
      return
    self.image.fill((255,255,255,int(self.alpha)),special_flags=pg.BLEND_RGBA_MULT)
    
class SuperExplosionEffect(FadeEffect):
  def __init__(self, SCENE, init_alpha, rect, image, life, speed = 100, scale = 1):
    super().__init__(SCENE, init_alpha, rect, image, life)
    self.x = self.rect.center[0]
    self.y = self.rect.center[1]
    self.xspeed = random.randint(-speed,speed)
    self.yspeed = random.randint(-speed,speed)
    rect = self.rect
    self.scale = scale
    self.image = pg.transform.scale(self.original_image, (int(rect.width*scale),int(rect.height*scale)))
    self.rect = self.image.get_rect()
    self.rect.center = rect.center
  def destroy(self):
    self.SCENE.group_overlay.add(DestroyEffect(self.SCENE,128,self.rect,self.original_image,1,1))
  def update(self):
    second_passed = self.SCENE.CLOCK.get_time()/1000
    self.alpha -= self.init_alpha*second_passed/self.life
    self.x += self.xspeed*second_passed
    self.y += self.yspeed*second_passed
    self.rect.center = (int(self.x),int(self.y))
    self.image = self.original_image.copy()
    if self.alpha < 0:
      self.destroy()
      self.kill()
      return
    self.image.fill((255,255,255,int(self.alpha)),special_flags=pg.BLEND_RGBA_MULT)
    
class Bullet(pg.sprite.Sprite): # 우선 총알 오브젝트를 만들고, 그 다음 아군 총알과 적군 총알을 구분할 거예요.
  def __init__(self, SCENE, x, y, speed, angle): # 인자 다섯 개를 받는 생성자예요.
    pg.sprite.Sprite.__init__(self) # 이 줄은 필수!
    self.radius = 6
    self.SCENE = SCENE
    self.image = pg.transform.rotate(pg.image.load('./assets/bullet.png'), angle) # 총알 이미지를 불러오고 회전합니다!
    self.trail_image = pg.transform.rotate(pg.image.load('./assets/bullet_white.png'), angle) # 총알 이미지를 불러오고 회전합니다!
    self.destroy_image = pg.image.load('./assets/explosion1.png')
    self.rect = self.image.get_rect() # rect는 게임 오브젝트의 크기와 위치를 담습니다!
    # 위에서는 이미지에 맞춰 rect를 설정하고 있습니다.
    self.x = x # x 좌표를 정해 줍시다.
    self.y = y # y 좌표를 정해 줍시다.
    # pygame에서 각도는 수평 오른쪽을 기준으로 반시계 방향으로 계산합니다. y축의 방향이 반대라는 점에 유의합시다.
    if len(speed) == 1:
      speed = speed[0]
      self.xspeed = math.cos(math.radians(angle))*speed # x축 속도를 정해 줍시다. (픽셀/초)
      self.yspeed = -math.sin(math.radians(angle))*speed # y축 속도를 정해 줍시다. (픽셀/초)
    else:
      self.xspeed = speed[0]
      self.yspeed = speed[1]
    self.rect.center = (int(self.x),int(self.y))
  def update(self):
    if self.x < 0 or self.x > self.SCENE.WINDOW.get_size()[0]:
      self.kill()
    if self.y < 0 or self.y > self.SCENE.WINDOW.get_size()[1]:
      self.kill()
    second_passed = self.SCENE.CLOCK.get_time()/1000
    # clock.get_time()은 지난 게임 루프부터 (Clock.tick()이 호출된 시점부터) 지난 시간을 밀리초 단위로 알려줍니다.
    # 즉 여기에서 second_passed는 지난 게임 루프부터 지금까지 지난 시간을 초 단위로 알려줍니다.
    self.x += second_passed*self.xspeed
    self.y += second_passed*self.yspeed
    self.rect.center = (int(self.x), int(self.y)) # Rect의 좌표를 변경된 좌표로 업데이트해 줍니다.
    self.SCENE.group_effects.add(FadeEffect(self.SCENE, 128, self.rect, self.trail_image, 0.5))
  def destroy(self):
    self.SCENE.group_overlay.add(DestroyEffect(self.SCENE, 128, self.rect, self.destroy_image, 1))

class EnemyBullet(Bullet):
  def __init__(self, SCENE, x, y, speed, angle): # 인자 다섯 개를 받는 생성자예요.
    super().__init__(SCENE, x, y, speed, angle)
    self.image = pg.transform.rotate(pg.image.load('./assets/enemybullet.png'), angle) # 총알 이미지를 불러오고 회전합니다!
    self.trail_image = pg.transform.rotate(pg.image.load('./assets/bullet_white.png'), angle) # 총알 이미지를 불러오고 회전합니다!
    self.destroy_image = pg.image.load('./assets/explosion2.png')


class Player(pg.sprite.Sprite):
  def __init__(self, SCENE, x, y):
    pg.sprite.Sprite.__init__(self)
    self.SCENE = SCENE
    self.radius = 16
    self.angle = 0
    self.original_image = pg.image.load('./assets/avatar_grumpy.png')
    self.original_trail_image = pg.image.load('./assets/player_effect.png') # 총알 이미지를 불러오고 회전합니다!
    self.explosion_image = pg.image.load('./assets/explosion1.png')
    self.rect = self.original_image.get_rect()
    self.x = x
    self.y = y
    self.xspeed = 0
    self.yspeed = 0
    self.last_launch = pg.time.get_ticks()
    self.health = 1000
  def hit(self, damage):
    self.health -= damage
    if self.health < 0:
      self.kill()
      self.destroy()
  def destroy(self):
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random()*2,30,random.random()))
    self.SCENE.death_time = pg.time.get_ticks()
    pass
  def launch(self):
    if pg.time.get_ticks() - self.last_launch > 100:
      self.SCENE.group_playerbullets.add(Bullet(self.SCENE,self.x,self.y,((self.xspeed**2+self.yspeed**2)**0.5+100,),self.angle))
      self.last_launch = pg.time.get_ticks()
  def update(self):
    second_passed = self.SCENE.CLOCK.get_time()/1000
    if self.health < 1000:
      self.health += second_passed*5
    if pg.key.get_focused:
      if pg.key.get_pressed()[pg.K_SPACE]:
        self.launch()
      if pg.key.get_pressed()[pg.K_a]:
        if self.xspeed > -150:
          self.xspeed -= 300*second_passed
      if pg.key.get_pressed()[pg.K_d]:
        if self.xspeed < 150:
          self.xspeed += 300*second_passed
      if pg.key.get_pressed()[pg.K_w]:
        if self.yspeed > -150:
          self.yspeed -= 300*second_passed
      if pg.key.get_pressed()[pg.K_s]:
        if self.yspeed < 150:
          self.yspeed += 300*second_passed
    # 속도를 점점 느리게 바꿔 줍니다.
    if self.xspeed > 0: self.xspeed -= 50*second_passed
    elif self.xspeed < 0: self.xspeed += 50*second_passed
    if self.yspeed > 0: self.yspeed -= 50*second_passed
    elif self.yspeed < 0: self.yspeed += 50*second_passed
    # 좌표를 바꿔 줍니다.
    self.x += second_passed*self.xspeed
    self.y += second_passed*self.yspeed
    if self.x == pg.mouse.get_pos()[0]: self.angle = 90
    else: self.angle = math.degrees(math.atan((pg.mouse.get_pos()[1]-self.y)/(self.x - pg.mouse.get_pos()[0])))
    if self.x > pg.mouse.get_pos()[0]: self.angle += 180
    if self.x < 16:
      self.x = 32-self.x
      self.xspeed = -self.xspeed
    if self.x > self.SCENE.WINDOW.get_size()[0] - 16:
      self.x = 2*self.SCENE.WINDOW.get_size()[0] - 32 - self.x
      self.xspeed = -self.xspeed
    if self.y < 16:
      self.y = 32-self.y
      self.yspeed = -self.yspeed
    if self.y > self.SCENE.WINDOW.get_size()[1] - 16:
      self.y = 2*self.SCENE.WINDOW.get_size()[1] - 32 - self.y
      self.xspeed = -self.xspeed
    self.image = pg.transform.rotate(self.original_image, 0)
    self.rect = self.image.get_rect()
    self.trail_image = pg.transform.rotate(self.original_trail_image, self.angle) # 총알 이미지를 불러오고 회전합니다!
    self.rect.center = (int(self.x), int(self.y)) # Rect의 좌표를 변경된 좌표로 업데이트해 줍니다.
    self.SCENE.group_effects.add(FadeEffect(self.SCENE, 128, self.rect, self.trail_image, 0.5))

class Enemy(pg.sprite.Sprite):
  def __init__(self, SCENE, x, y, target, patrol_point, angry):
    pg.sprite.Sprite.__init__(self)
    self.SCENE = SCENE
    self.radius = 16
    self.angle = 0
    self.target = target
    char_selector = random.randint(0,2)
    if char_selector == 0:
      self.original_image = pg.image.load('./assets/avatar_professor.png')
    elif char_selector ==1:
      self.original_image = pg.image.load('./assets/avatar_religious_girl.png')
    elif char_selector ==2:
      self.original_image = pg.image.load('./assets/avatar_religious_girl_2.png')
    self.original_trail_image = pg.image.load('./assets/enemy_effect.png')
    self.explosion_image = pg.image.load('./assets/explosion2.png')
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y
    self.xspeed = 0
    self.yspeed = 0
    self.last_launch = pg.time.get_ticks()
    self.health = 50
    self.patrol_point = patrol_point
    self.angry = angry
  def hit(self, damage):
    self.health -= damage
    if self.health < 0:
      self.destroy()
      self.kill()
  def destroy(self):
    self.SCENE.finish_timer += 100
    self.SCENE.score += 1
    text_score_surface = self.SCENE.game_font.render(str(self.SCENE.score),True,pg.Color(255,128,128))
    self.SCENE.spawn_enemy()
    self.SCENE.group_overlay.add(DestroyEffect(self.SCENE,200,self.rect,text_score_surface,1))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random(),20,random.random()))
    self.SCENE.group_overlay.add(DestroyEffect(self.SCENE,128,self.rect,self.explosion_image,1))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random(),20,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random(),20,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random(),20,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random(),20,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random(),20,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random(),20,random.random()))
    self.SCENE.group_overlay.add(SuperExplosionEffect(self.SCENE,128,self.rect,self.explosion_image,random.random(),20,random.random()))
    pass
  def launch(self):
    if pg.time.get_ticks() - self.last_launch > 200:
      #self.SCENE.group_enemybullets.add(EnemyBullet(self.SCENE,self.x,self.y,((self.xspeed**2+self.yspeed**2)**0.5+100,),self.angle))
      self.last_launch = pg.time.get_ticks()
  def update(self):
    second_passed = self.SCENE.CLOCK.get_time()/1000
    if (math.sqrt((self.target.x - self.x) ** 2 + (self.target.y - self.y) ** 2) < 200):
      self.angry = 1
    else:
      self.angry = 0

    if self.angry == 0:
      if self.x > self.patrol_point[0]:
        if self.xspeed > -100:
          self.xspeed -= 200*second_passed
      if self.x < self.patrol_point[0]:
        if self.xspeed < 100:
          self.xspeed += 200*second_passed
      if self.y > self.patrol_point[1]:
        if self.yspeed > -100:
          self.yspeed -= 200*second_passed
      if self.y < self.patrol_point[1]:
        if self.yspeed < 100:
          self.yspeed += 200*second_passed
    elif self.angry == 1:
      if self.x > self.target.x:
        if self.xspeed > -100:
          self.xspeed -= 200*second_passed
      if self.x < self.target.x:
        if self.xspeed < 100:
          self.xspeed += 200*second_passed
      if self.y > self.target.y:
        if self.yspeed > -100:
          self.yspeed -= 200*second_passed
      if self.y < self.target.y:
        if self.yspeed < 100:
          self.yspeed += 200*second_passed

    # 속도를 점점 느리게 바꿔 줍니다.
    if self.xspeed > 0: self.xspeed -= 50*second_passed
    elif self.xspeed < 0: self.xspeed += 50*second_passed
    if self.yspeed > 0: self.yspeed -= 50*second_passed
    elif self.yspeed < 0: self.yspeed += 50*second_passed
    # 좌표를 바꿔 줍니다.
    self.x += second_passed*self.xspeed
    self.y += second_passed*self.yspeed
    if self.xspeed == 0: self.angle = 90
    else: self.angle = math.degrees(math.atan(-self.yspeed/self.xspeed))
    if self.xspeed < 0: self.angle += 180

    if self.x == self.target.x: self.target_angle = 90
    else: self.target_angle = math.degrees(math.atan((self.target.y - self.y)/(self.x - self.target.x)))
    if self.x > self.target.x: self.target_angle += 180
    if abs(self.target_angle-self.angle) < 10 or abs(self.target_angle-self.angle) > 350: self.launch()
    if self.x < 16:
      self.x = 32-self.x
      self.xspeed = -self.xspeed
    if self.x > self.SCENE.WINDOW.get_size()[0] - 16:
      self.x = 2*self.SCENE.WINDOW.get_size()[0] - 32 - self.x
      self.xspeed = -self.xspeed
    if self.y < 16:
      self.y = 32-self.y
      self.yspeed = -self.yspeed
    if self.y > self.SCENE.WINDOW.get_size()[1] - 16:
      self.y = 2*self.SCENE.WINDOW.get_size()[1] - 32 - self.y
      self.xspeed = -self.xspeed
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.trail_image = pg.transform.rotate(self.original_trail_image, self.angle) # 총알 이미지를 불러오고 회전합니다!
    self.rect.center = (int(self.x), int(self.y)) # Rect의 좌표를 변경된 좌표로 업데이트해 줍니다.
    self.SCENE.group_effects.add(FadeEffect(self.SCENE, 128, self.rect, self.trail_image, 0.5))
