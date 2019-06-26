import pygame as pg
import sys
import wingbase.scene as scene
import scenes.scene_lastboss as scene_lastboss

if __name__ == "__main__":
  pg.init()
  pg.font.init()

  SCREEN = (1080, 720)
  WINDOW = pg.display.set_mode(SCREEN)
  FPS = 60
  CLOCK = pg.time.Clock()
  SCENE_LASTBOSS = scene_lastboss.Scene_LastBoss(WINDOW, CLOCK, 60, [])
  SCENE = SCENE_LASTBOSS
  while True:
    SCENE.loop_begin() # begin loop
    next_scene = SCENE.loop()
    if next_scene != 0: # change scene according to loop return
      pg.quit()
      sys.exit()
    SCENE.loop_tick()
