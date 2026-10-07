import math
import pygame


class Sensor:

    def __init__(self, relative_angle_degrees, max_distance=240):

        self.relative_angle = math.radians(relative_angle_degrees)
        self.max_distance = max_distance

        self.distance = max_distance
        self.end_point = (0, 0)

    def cast(self, origin, car_angle, obstacles):

        angle = car_angle + self.relative_angle

        direction = pygame.Vector2(
            math.cos(angle),
            math.sin(angle)
        )

        closest_distance = self.max_distance

        closest_point = (
            origin.x + direction.x * self.max_distance,
            origin.y + direction.y * self.max_distance
        )

        # Smaller step = more accurate collision sensing.
        step = 1

        for distance in range(
            0,
            self.max_distance + 1,
            step
        ):

            point = origin + direction * distance

            for obstacle in obstacles:

                if obstacle.collidepoint(
                    int(point.x),
                    int(point.y)
                ):

                    closest_distance = distance

                    closest_point = (
                        point.x,
                        point.y
                    )

                    self.distance = closest_distance
                    self.end_point = closest_point

                    # 0 = danger
                    # 1 = clear
                    return closest_distance / self.max_distance

        self.distance = closest_distance
        self.end_point = closest_point

        return self.distance / self.max_distance

    def draw(self, screen, origin):

        pygame.draw.line(
            screen,
            (220, 220, 80),
            origin,
            self.end_point,
            2
        )

        pygame.draw.circle(
            screen,
            (255, 80, 80),
            (
                int(self.end_point[0]),
                int(self.end_point[1])
            ),
            4
        )