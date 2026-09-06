import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self Driving Car")

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30,30,30)) #BG GREY (RGB Basis) 

    pygame.display.flip()

pygame.quit()        