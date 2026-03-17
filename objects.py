import random
import pygame


class FallingObject:
    def __init__(self, screen_width):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height

        self.type = random.choice(["melon", "banana", "apple", "pear", "strawberry", "bomb"])
        self.speed = random.randint(3, 7)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        if self.type == "melon":
            # Watermelon slice
            pygame.draw.polygon(screen, (0, 200, 0), [
                (self.x, self.y + 40),
                (self.x + 40, self.y + 40),
                (self.x + 20, self.y)
            ])
            pygame.draw.polygon(screen, (255, 0, 0), [
                (self.x + 5, self.y + 35),
                (self.x + 35, self.y + 35),
                (self.x + 20, self.y + 5)
            ])
            # Seeds
            for i in range(3):
                pygame.draw.circle(screen, (0, 0, 0), (self.x + 12 + i * 8, self.y + 25), 2)

        elif self.type == "banana":
            pygame.draw.arc(screen, (255, 255, 0), (self.x, self.y, 40, 40), 0.5, 2.5, 6)
            pygame.draw.arc(screen, (255, 220, 0), (self.x + 5, self.y + 5, 30, 30), 0.5, 2.5, 4)

        elif self.type == "apple":
            pygame.draw.circle(screen, (255, 0, 0), (self.x + 20, self.y + 22), 15)
            pygame.draw.rect(screen, (139, 69, 19), (self.x + 18, self.y + 5, 4, 10))
            pygame.draw.ellipse(screen, (0, 200, 0), (self.x + 22, self.y + 5, 10, 6))

        elif self.type == "pear":
            pygame.draw.ellipse(screen, (0, 255, 0), (self.x + 10, self.y + 15, 20, 25))
            pygame.draw.circle(screen, (0, 255, 0), (self.x + 20, self.y + 15), 10)
            pygame.draw.rect(screen, (139, 69, 19), (self.x + 18, self.y + 2, 4, 8))

        elif self.type == "strawberry":
            pygame.draw.polygon(screen, (255, 0, 0), [
                (self.x + 20, self.y + 40),
                (self.x + 5, self.y + 15),
                (self.x + 35, self.y + 15)
            ])
            pygame.draw.circle(screen, (0, 200, 0), (self.x + 20, self.y + 10), 8)
            # Seeds
            for i in range(5):
                pygame.draw.circle(screen, (255, 255, 0),
                                   (self.x + 10 + i * 5, self.y + 25), 1)

        elif self.type == "bomb":
            pygame.draw.circle(screen, (60, 60, 60), (self.x + 20, self.y + 20), 18)
            pygame.draw.line(screen, (200, 200, 200),
                             (self.x + 20, self.y + 5), (self.x + 30, self.y - 8), 3)
            pygame.draw.circle(screen, (255, 140, 0), (self.x + 30, self.y - 8), 4)

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def spawn_object(screen_width):
    return FallingObject(screen_width)
