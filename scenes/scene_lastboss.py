import pygame as pg 
import wingbase.scene as scene 
import prefabs.prefabs_lastboss as prefabs_lastboss 
import sys 
import random
import math

Screen = (1000, 600) 
FPS = 60

player_damage = 5
professor_damage = 2



class Scene_LastBoss(scene.Scene):
        def __init__(self, WINDOW, CLOCK, FPS = 30, GROUPS = []):
                super().__init__(WINDOW, CLOCK, FPS=30, GROUPS=[])
                pg.mixer.pre_init(buffer=128)
                pg.mixer.set_num_channels(32)
                #SOUND_shoot = pg.mixer.Sound('bullet.wav')
                #pg.mixer.music.load('Gyoga.wav')
                #pg.mixer.music.play(loops=-1)
                self.player = prefabs_lastboss.Player(self,500,500,180)
                self.professor = prefabs_lastboss.Professor(self, 500, 500, 180)
                self.group_player = pg.sprite.Group()
                self.group_player.add(self.player)
                self.group_professor = pg.sprite.Group()
                self.group_professor.add(self.professor)
                self.group_bullets = pg.sprite.Group()
                self.group_professorbullets = pg.sprite.Group()
                self.group_playerbullets = pg.sprite.Group()
                self.groups.append(self.group_player)
                self.groups.append(self.group_professor)
                self.groups.append(self.group_bullets)
                self.groups.append(self.group_playerbullets)
                self.groups.append(self.group_professorbullets)
                
        def loop(self): 
                for bullet in self.group_bullets:
                        if pg.sprite.collide_mask(self.player, bullet):
                                pg.event.post(pg)
                return 0
                
if __name__=="__main__":
        pg.init()
        pg.font.init()
        SCREEN = (960, 720)
        WINDOW = pg.display.set_mode(SCREEN)
        FPS = 60
        CLOCK = pg.time.Clock()
        SCENE = Scene_LastBoss(WINDOW, CLOCK, 60, [])
        while True:
                SCENE.loop_begin()
                SCENE.loop()
                SCENE.loop_tick()
                










        
