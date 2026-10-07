import math
import pygame

from sensors import Sensor


class Car:

    def __init__(self, x, y):

        self.position = pygame.Vector2(x, y)

        self.width = 28
        self.height = 44

        # Start facing upward.
        self.angle = -math.pi / 2

        self.speed = 1.5
        self.steering_strength = 0.08

        # Five sensors around the front.
        self.sensors = [
            Sensor(-60),
            Sensor(-30),
            Sensor(0),
            Sensor(30),
            Sensor(60),
        ]

        self.sensor_values = [1.0] * 5

    def get_sensor_origin(self):

        # Start sensors slightly ahead of the car.
        direction = pygame.Vector2(
            math.cos(self.angle),
            math.sin(self.angle)
        )

        return self.position + direction * 10

    def update_sensors(self, obstacles):

        origin = self.get_sensor_origin()

        self.sensor_values = [
            sensor.cast(
                origin,
                self.angle,
                obstacles
            )
            for sensor in self.sensors
        ]

    def steer(self, direction):

        # Keep steering between -1 and +1.
        direction = max(
            -1.0,
            min(1.0, direction)
        )

        self.angle += (
            direction *
            self.steering_strength
        )

    def update(self):

        front_clearance = self.sensor_values[2]

        # Slow down when an obstacle is close.
        if front_clearance < 0.25:

            current_speed = 0.6

        elif front_clearance < 0.40:

            current_speed = 1.0

        elif front_clearance < 0.60:

            current_speed = 1.5

        else:

            current_speed = self.speed

        direction = pygame.Vector2(
            math.cos(self.angle),
            math.sin(self.angle)
        )

        self.position += direction * current_speed

    def get_rect(self):

        # Use a circular collision area.
        radius = 20

        return pygame.Rect(
            int(self.position.x - radius),
            int(self.position.y - radius),
            radius * 2,
            radius * 2
        )

    def collides(self, obstacles):

        car_rect = self.get_rect()

        return any(
            car_rect.colliderect(
                obstacle.rect
            )
            for obstacle in obstacles
        )

    def draw(self, screen):

        # Create a transparent surface for the car.
        surface_width = self.width + 14
        surface_height = self.height + 14

        car_surface = pygame.Surface(
            (
                surface_width,
                surface_height
            ),
            pygame.SRCALPHA
        )

        center_x = surface_width // 2
        center_y = surface_height // 2

        left = center_x - self.width // 2
        right = center_x + self.width // 2
        top = center_y - self.height // 2
        bottom = center_y + self.height // 2

        # Main body.
        pygame.draw.rect(
            car_surface,
            (45, 150, 225),
            (
                left,
                top,
                self.width,
                self.height
            ),
            border_radius=8
        )

        # Front hood.
        pygame.draw.polygon(
            car_surface,
            (65, 170, 235),
            [
                (left + 5, top + 13),
                (left + 8, top + 4),
                (right - 8, top + 4),
                (right - 5, top + 13)
            ]
        )




        # Wheels.
        wheel_color = (20, 20, 20)

        pygame.draw.rect(
            car_surface,
            wheel_color,
            (left - 3, top + 8, 6, 12),
            border_radius=2
        )

        pygame.draw.rect(
            car_surface,
            wheel_color,
            (right - 3, top + 8, 6, 12),
            border_radius=2
        )

        pygame.draw.rect(
            car_surface,
            wheel_color,
            (left - 3, bottom - 20, 6, 12),
            border_radius=2
        )

        pygame.draw.rect(
            car_surface,
            wheel_color,
            (right - 3, bottom - 20, 6, 12),
            border_radius=2
        )

        # Headlights.
        pygame.draw.rect(
            car_surface,
            (255, 245, 175),
            (left + 5, top + 5, 6, 4),
            border_radius=2
        )

        pygame.draw.rect(
            car_surface,
            (255, 245, 175),
            (right - 11, top + 5, 6, 4),
            border_radius=2
        )

       

        pygame.draw.rect(
            car_surface,
            (220, 50, 50),
            (right - 11, bottom - 9, 6, 4),
            border_radius=2
        )

        # Show the front direction.
        pygame.draw.polygon(
            car_surface,
            (255, 255, 255),
            [
                (center_x, top + 1),
                (center_x - 4, top + 8),
                (center_x + 4, top + 8)
            ]
        )

        # Rotate the car with its direction.
        rotated = pygame.transform.rotate(
            car_surface,
            -math.degrees(self.angle) - 90
        )

        rect = rotated.get_rect(
            center=self.position
        )

        screen.blit(
            rotated,
            rect
        )