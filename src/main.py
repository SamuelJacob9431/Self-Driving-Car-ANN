import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self Driving Car")

#Car Positioning, tis Start Position
car_x = 100
car_y = 300

#Car Speed! Movin by 4 px every update
speed = 4
running = True

#timer
clock = pygame.time.Clock()
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Update Car position upon Speed
    car_x += speed
    screen.fill((30,30,30)) #BG GREY (RGB Basis) 
    
    #Render Car temp as rect
    pygame.draw.rect(
        screen,
        (200, 200, 200),
        (car_x, car_y, 40, 20)
    )

    pygame.display.flip()
    #60 FPS
    clock.tick(60)

pygame.quit()        