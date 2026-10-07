import pygame

from car import Car
from neural_network import NeuralNetwork
from obstacles import Obstacle




pygame.init()

WIDTH = 1000
HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))


clock = pygame.time.Clock()
font = pygame.font.Font(None, 26)


def create_obstacles():

    return [


        Obstacle(100, 80, 800, 25),
        Obstacle(100, 595, 800, 25),

        Obstacle(100, 80, 25, 540),
        Obstacle(875, 80, 25, 540),

       

        Obstacle(300, 300, 400, 35),
    ]




car = Car(WIDTH / 2, 540)

obstacles = create_obstacles()

network = NeuralNetwork()

running = True
crashed = False
paused = False



while running:

   

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_r:

                car = Car(WIDTH / 2, 540)

                crashed = False



    if not crashed and not paused:

        # 1. SENSOR
        car.update_sensors(
            [obstacle.rect for obstacle in obstacles]
        )


        # 2. ANN
        outputs, hidden = network.forward(
            car.sensor_values
        )


        steering = outputs[1] - outputs[0]


        # -------------------------------------
        # SAFETY CORRECTION
        # -------------------------------------

        left_space = (
            car.sensor_values[0]
            + car.sensor_values[1]
        ) / 2

        right_space = (
            car.sensor_values[3]
            + car.sensor_values[4]
        ) / 2

        front_space = car.sensor_values[2]


        # If an obstacle is approaching,
        # steer toward the side with more space.

        if front_space < 0.65:

            if right_space > left_space:

                steering += 0.8

            else:

                steering -= 0.8


        # Keep steering within -1 to +1.

        steering = max(
            -1.0,
            min(1.0, steering)
        )


        # 4. MOVE CAR

        car.steer(steering)

        car.update()


        # -------------------------------------
        # COLLISION
        # -------------------------------------

        if car.collides(obstacles):

            crashed = True


        # -------------------------------------
        # KEEP CAR INSIDE TRACK
        # -------------------------------------

        if not (
            80 < car.position.x < 920
            and
            80 < car.position.y < 595
        ):

            crashed = True


    # =========================================
    # DRAW
    # =========================================

    screen.fill(
        (25, 25, 25)
    )


    # Track boundary

    pygame.draw.rect(
        screen,
        (90, 90, 90),
        pygame.Rect(
            100,
            80,
            800,
            515
        ),
        3
    )


    # Obstacles

    for obstacle in obstacles:

        obstacle.draw(screen)


    # Car

    car.draw(screen)


    # Sensors

    for sensor in car.sensors:

        sensor.draw(
            screen,
            car.get_sensor_origin()
        )


    # =========================================
    # INFORMATION
    # =========================================

    title = font.render(
        "5 Sensors -> 6 Hidden Neurons -> 2 Outputs",
        True,
        (240, 240, 240)
    )

    screen.blit(
        title,
        (20, 15)
    )


    sensor_text = font.render(
        "Sensors: "
        + " ".join(
            f"{value:.2f}"
            for value in car.sensor_values
        ),
        True,
        (220, 220, 220)
    )

    screen.blit(
        sensor_text,
        (20, 40)
    )


    output_text = font.render(
        f"ANN Output: "
        f"LEFT={outputs[0]:.2f} "
        f"RIGHT={outputs[1]:.2f}",
        True,
        (220, 220, 220)
    )

    screen.blit(
        output_text,
        (20, 65)
    )


    # Crash message

    if crashed:

        message = font.render(
            "CRASHED - Press R to restart",
            True,
            (255, 100, 100)
        )

        screen.blit(
            message,
            (
                WIDTH // 2 - 130,
                20
            )
        )


    pygame.display.flip()

    clock.tick(FPS)


pygame.quit()