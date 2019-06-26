import pygame as pg
import wingbase.colors as colors
import sys

class Button(pg.sprite.Sprite):
  def __init__(self, x, y, image_name, function, centered = True, arg = None):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.image.load(image_name)
    self.rect = self.image.get_rect()
    self.function = function
    self.mouseon = False
    self.arg = arg
    if centered: self.rect.center = (x,y)
    else: self.rect.topleft = (x,y)
  def update(self):
    if self.rect.colliderect(pg.Rect(pg.mouse.get_pos(),(1,1))): self.mouseon = True
    else: self.mouseon = False
  def click(self):
    if self.mouseon:
      print("clicked")
      self.function(self.arg)

class Image(pg.sprite.Sprite):
  def __init__(self, x, y, image_name, centered = True):
    pg.sprite.Sprite.__init__(self)
    self.image = pg.image.load(image_name)
    self.rect = self.image.get_rect()
    if centered: self.rect.center = (x,y)
    else: self.rect.topleft = (x,y)
  def update(self):
    pass
