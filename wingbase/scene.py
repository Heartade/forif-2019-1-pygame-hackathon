import pygame as pg
import wingbase.colors as colors
import sys

class Scene():
  def __init__(self, WINDOW, CLOCK, FPS = 30, GROUPS = []):
    self.WINDOW = WINDOW
    self.CLOCK = CLOCK
    self.FPS = FPS
    self.groups = GROUPS
    self.group_effects = pg.sprite.Group()
    self.groups.append(self.group_effects)
    self.group_main = pg.sprite.Group()
    self.groups.append(self.group_main)
  def event_handle(self, event):
    if event.type == pg.QUIT:
      pg.quit()
      sys.exit()
      return
  def loop_begin(self):
    self.WINDOW.fill(colors.BLACK)
    for event in pg.event.get():
      self.event_handle(event)
    for group in self.groups:
      group.update()
    for group in self.groups:
      group.draw(self.WINDOW)
  def loop(self):
    return 0
  def loop_tick(self):
    pg.display.flip()
    self.CLOCK.tick(self.FPS)

if __name__ == "__main__":
  pg.init()
  SCREEN = (360, 480)
  WINDOW = pg.display.set_mode(SCREEN)
  FPS = 60
  CLOCK = pg.time.Clock()
  SCENE = Scene(WINDOW, CLOCK, 60, [])
  while True:
    SCENE.loop_begin()
    SCENE.loop()
    SCENE.loop_tick()
    
