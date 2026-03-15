import random
import pygame


class FallingObject:
    def __init__(self, screen_width):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height

        self.type = random.choice(["gift", "star", "bomb", "shield"])
        self.speed = random.randint(3, 7)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        if self.type == "gift":
            pygame.draw.rect(screen, (0, 200, 255), (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, (255, 255, 0), (self.x + 16, self.y, 8, self.height))
            pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y + 16, self.width, 8))

        elif self.type == "star":
            points = [
                (self.x + 20, self.y + 0),
                (self.x + 25, self.y + 14),
                (self.x + 40, self.y + 14),
                (self.x + 28, self.y + 23),
                (self.x + 32, self.y + 38),
                (self.x + 20, self.y + 28),
                (self.x + 8, self.y + 38),
                (self.x + 12, self.y + 23),
                (self.x + 0, self.y + 14),
                (self.x + 15, self.y + 14),
            ]
            pygame.draw.polygon(screen, (255, 255, 0), points)

        elif self.type == "bomb":
            pygame.draw.circle(screen, (60, 60, 60), (self.x + 20, self.y + 20), 18)
            pygame.draw.line(screen, (200, 200, 200), (self.x + 20, self.y + 5), (self.x + 30, self.y - 8), 3)
            pygame.draw.circle(screen, (255, 140, 0), (self.x + 30, self.y - 8), 4)

        elif self.type == "shield":
            pygame.draw.ellipse(screen, (0, 200, 200), (self.x + 5, self.y + 3, 30, 34))
            pygame.draw.ellipse(screen, (255, 255, 255), (self.x + 12, self.y + 10, 16, 18))

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def spawn_object(screen_width):
    return FallingObject(screen_width)