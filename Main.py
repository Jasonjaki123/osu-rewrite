import pygame, sys, time, json, random
import scripts.cursor
import scripts.anim_loader as anim_loader
import scripts.entity as Entity
import scripts.Circle as Circle
from pygame.locals import *
pygame.init()
# json
with open('scripts/setup.json') as f:
    json_data = json.load(f)

info_obj = pygame.display.Info()
screen = pygame.display.set_mode((info_obj.current_w, info_obj.current_h))
animations = anim_loader.AnimationManager()
pygame.display.set_caption('osu! rewrited')
icon = pygame.image.load(json_data["paths"]["logo"])
icon = pygame.display.set_icon(icon)

clock = pygame.time.Clock()
# Mouse handling stuff
pos = pygame.mouse.get_pos()
cursor = scripts.cursor.cursor(pos, json_data["paths"]["cursor"])
# cursor_trial = Entity.Entity(animations, [cursor.pos[0] - 10, cursor.pos[1] + 10], (50, 50), "trial")
pygame.mouse.set_visible(False)

last_time = time.time()
framerate = 6
particles = []
circle_img = pygame.image.load('data/images/Circle/img_0.png')
circle = Circle.Circle(circle_img,[random.randint(0, 1366), random.randint(0, 768)])
particle_img = pygame.image.load('data/images/animations/trial_idle/img_0.png')
pygame.transform.scale(particle_img, (particle_img.get_width() // 2, particle_img.get_height() // 2))
motion = False
while True:

    screen.fill((0, 0, 0))
    pos = pygame.mouse.get_pos()
    if motion:
        for i in range(10):
            particles.append([[pos[0], pos[1]], [random.randint(0,20) / 10 - 1, random.randint(0,20) / 10 - 1], 0.61])
    for particle in particles:
        particle[2] -= 0.6
        screen.blit(particle_img, (particle[0][0]-particle_img.get_width() // 2, particle[0][1]-particle_img.get_height() // 2))
        if particle[2] <= 0:
            particles.remove(particle)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == MOUSEMOTION:
            motion = True
    cursor.render(screen, pos)
    pygame.display.update()
    clock.tick(60)
