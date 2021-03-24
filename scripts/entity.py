import math

import pygame

from .core_funcs import *

def collision_list(obj, obj_list):
    hit_list = []
    for r in obj_list:
        if obj.colliderect(r):
            hit_list.append(r)
    return hit_list

class Entity:
    def __init__(self, assets, pos, size, type):
        self.assets = assets
        self.pos = list(pos).copy()
        self.size = list(size).copy()
        self.type = type
        self.flip = [False, False]
        self.rotation = 0
        self.centered = False
        self.opacity = 255
        self.scale = [1, 1]
        self.active_animation = None
        self.height = 0

        if self.type + '_idle' in self.assets.animations:
            self.set_action('idle')

    @property
    def img(self):
        if not self.active_animation:
            img = self.current_image
        else:
            self.set_image(self.active_animation.img)
            img = self.current_image
        if self.scale != [1, 1]:
            img = pygame.transform.scale(img, (int(self.scale[0] * self.image_base_dimensions[0]), int(self.scale[1] * self.image_base_dimensions[1])))
        if any(self.flip):
            img = pygame.transform.flip(self.current_image, self.flip[0], self.flip[1])
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        if self.opacity != 255:
            img.set_alpha(self.opacity)
        return img

    @property
    def rect(self):
        if not self.centered:
            return pygame.Rect(self.pos[0] // 1, self.pos[1] // 1, self.size[0], self.size[1])
        else:
            return pygame.Rect((self.pos[0] - self.size[0] // 2) // 1, (self.pos[1] - self.size[1] // 2) // 1, self.size[0], self.size[1])

    @property
    def center(self):
        if self.centered:
            return self.pos.copy()
        else:
            return [self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2]

    def set_action(self, action_id, force=False):
        if force:
            self.active_animation = self.assets.new(self.type + '_' + action_id)
        elif (not self.active_animation) or (self.active_animation.data.id != self.type + '_' + action_id):
            self.active_animation = self.assets.new(self.type + '_' + action_id)

    def set_image(self, surf):
        self.current_image = surf.copy()
        self.image_base_dimensions = list(surf.get_size())

    def set_scale(self, new_scale, fit_hitbox=True):
        try:
            self.scale = new_scale.copy()
        except AttributeError:
            self.scale = [new_scale, new_scale]
        if fit_hitbox:
            self.size = [int(self.scale[0] * self.image_base_dimensions[0]), int(self.scale[1] * self.image_base_dimensions[1])]

    def render(self, surf, pos):
        surf.blit(self.img, ((pos[0]) // 1, (pos[1] - self.height) // 1))

    def update(self, dt):
        if self.active_animation:
            self.active_animation.play(dt)
