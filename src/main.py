import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self Driving Car")

#Car Positioning
car_x = 100
car_y = 300

#Car Speed!
speed = 4
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update Car position upon Speed
    car_x += speed
    screen.fill((30,30,30)) #BG GREY (RGB Basis) 

    pygame.display.flip()

pygame.quit()        