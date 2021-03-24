import pygame, random
import scripts.anim_loader as anim_loader
from pygame.locals import *
pygame.init()

class Circle():
    def __init__(self, img, pos):
        self.pos = pos
        self.img = img
        self.timer = 2
    def render(self, surface):
        surface.blit(self.img, (self.pos[0], self.pos[1]))
    def animation(self):
        pass
