import pygame as pg
import wingbase.colors as colors
import sys
import wingbase.ui as ui
import wingbase.scene as scene

class Scene_GameClear(scene.Scene):
  def __init__(self, WINDOW, CLOCK, FPS = 30, GROUPS = [], score = 0):
    super().__init__(WINDOW, CLOCK, FPS=30, GROUPS=[])
    try:
      f = open('./assets/highscore.txt',mode='r')
      s = int(f.readline())
      if s < score:
        f.close()
        f = open('./assets/highscore.txt',mode='w')
        f.write(str(score))
    except:
      f = open('./assets/highscore.txt',mode='w')
      f.write(str(score))
    self.game_font = pg.font.Font('./assets/NotoSans-BoldItalic.ttf',24) 
    self.score = score
    self.group_button = pg.sprite.Group()
    self.groups.append(self.group_button)
    self.tomainmenubutton = ui.Button(180,240,'./assets/clearscreen.png',self.on_button_click)
    self.score_text_surface = self.game_font.render("SCORE: "+str(score), True, pg.Color(255,255,255))
    self.score_text_rect = self.score_text_surface.get_rect()
    self.score_text_rect.center = (180,260)
    self.group_button.add(self.tomainmenubutton)
    self.to_next_stage = False
  def on_button_click(self,arg):
    self.to_next_stage = True
  def loop(self):
    self.WINDOW.blit(self.score_text_surface,self.score_text_rect)
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
  SCENE = Scene_GameClear(WINDOW, CLOCK, 60, [], 100)
  while True:
    SCENE.loop_begin()
    SCENE.loop() # change scene according to loop return
    SCENE.loop_tick()
