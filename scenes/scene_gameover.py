import pygame as pg
import wingbase.colors as colors
import sys
import wingbase.ui as ui
import wingbase.scene as scene

class Scene_Gameover(scene.Scene):
  def __init__(self, WINDOW, CLOCK, FPS = 30, GROUPS = []):
    super().__init__(WINDOW, CLOCK, FPS=30, GROUPS=[])
    self.group_button = pg.sprite.Group()
    self.groups.append(self.group_button)
    self.tomainmenubutton = ui.Button(180,240,'./assets/goscreen.png',self.on_button_click)
    self.group_button.add(self.tomainmenubutton)
    self.to_next_stage = False
  def on_button_click(self,arg):
    self.to_next_stage = True
  def loop(self):
    if self.to_next_stage:
      return 1
    else: return 0
  def event_handle(self, event):
    if event.type == pg.MOUSEBUTTONDOWN:
      for button in self.group_button.sprites():
        button.click()
    super().event_handle(event)

if __name__ == "__main__":
  pg.init()
  SCREEN = (960, 720)
  WINDOW = pg.display.set_mode(SCREEN)
  FPS = 60
  CLOCK = pg.time.Clock()
  SCENE = Scene_Gameover(WINDOW, CLOCK, 60, [])
  while True:
    SCENE.loop_begin()
    SCENE.loop() # change scene according to loop return
    SCENE.loop_tick()
