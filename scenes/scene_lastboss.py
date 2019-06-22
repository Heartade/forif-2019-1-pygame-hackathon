import pygame as pg 
import wingbase.scene as scene
import wingbase.colors as colors
import prefabs.prefabs_lastboss as prefabs_lastboss 
import sys 
import random
import math
import wingbase.ui as ui

Screen = (1080, 720) 
FPS = 60



class Scene_LastBoss(scene.Scene):
        def __init__(self, WINDOW, CLOCK, FPS = 30, GROUPS = []):
                super().__init__(WINDOW, CLOCK, FPS=30, GROUPS=[])
                pg.mixer.pre_init(buffer=128)
                pg.mixer.set_num_channels(32)
                #SOUND_shoot = pg.mixer.Sound('bullet.wav')
                #pg.mixer.music.load('Gyoga.wav')
                #pg.mixer.music.play(loops=-1)
                self.player = prefabs_lastboss.Player(self,540,500,180)
                self.professor = prefabs_lastboss.Professor(self,540,200,180)
                self.bullets = prefabs_lastboss.ProfessorBullet(self,540,500,180,60)
                self.playerbullets = prefabs_lastboss.Bullet(self,540,500,180,90)
                self.group_player = pg.sprite.Group()
                self.group_player.add(self.player)
                self.group_professor = pg.sprite.Group()
                self.group_professor.add(self.professor)
                self.group_bullets = pg.sprite.Group()
                self.group_bullets.add(self.bullets)
                self.group_playerbullets = pg.sprite.Group()
                self.group_playerbullets.add(self.playerbullets)
                self.groups.append(self.group_player)
                self.groups.append(self.group_professor)
                self.groups.append(self.group_bullets)
                self.groups.append(self.group_playerbullets)
                
        def health_bars(self):
                pg.draw.rect(self.WINDOW, (255,0,0), (20, 75, self.professor.health, 25))
                pg.draw.rect(self.WINDOW, (0,0,255), (20, 25, self.player.health, 25))                           

        def loop(self):
                for bullet in self.group_bullets:
                        if pg.sprite.collide_mask(self.player, bullet):
                                bullet.kill()
                                self.player.health -= 2
                                if self.player.health < 0: self.player.kill()
                                
                for playerbullets in self.group_playerbullets:
                        if pg.sprite.collide_mask(self.professor, playerbullets):
                                playerbullets.kill()
                                self.professor.health -= 1
                                if self.professor.health < 0: self.professor.kill()
                self.health_bars()
                return 0
                
if __name__=="__main__":
        pg.init()
        pg.font.init()
        SCREEN = (1080, 720)
        WINDOW = pg.display.set_mode(SCREEN)
        FPS = 60
        CLOCK = pg.time.Clock()
        SCENE = Scene_LastBoss(WINDOW, CLOCK, 60, [])
        while True:
                SCENE.loop_begin()
                SCENE.loop()
                SCENE.loop_tick()
                










        
