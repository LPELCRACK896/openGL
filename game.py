import pygame
from pygame.locals import *
from GL import Renderer
width = 960
height = 540
deltaTime = None

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
rend = Renderer(screen)

isRunning = True

while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: isRunning = False

    deltaTime = clock.tick(60) / 1000
    print(deltaTime)
    rend.render()
    pygame.display.flip()

pygame.quit()