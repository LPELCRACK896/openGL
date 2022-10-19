import pygame
from pygame.locals import *
from GL import Renderer, Model
from shaders import *
width = 960
height = 540
deltaTime = None

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
rend = Renderer(screen)

triangle = [-0.5, -0.5, 0,          1.0, 0.0, 0.0,
            0, 0.5, 0,              0.0, 1.0, 0.0,
            0.5, -0.5, 0,           0.0, 0.0, 1.0,
            ]

triangle = Model(triangle)
triangle.position.z -= 10
rend.setShadders(VERTEX_SHADER, FRAGMENT_SHADER)
rend.scene.append(triangle)

isRunning = True

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: isRunning = False

    deltaTime = clock.tick(60) / 1000
    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()