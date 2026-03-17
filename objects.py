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
            # watermeloen
            pygame.draw.circle(screen, (0, 180, 0), (self.x + 20, self.y + 20), 18)
            pygame.draw.circle(screen, (255, 60, 60), (self.x + 20, self.y + 20), 14)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 15, self.y + 18), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 20, self.y + 24), 2)
            pygame.draw.circle(screen, (0, 0, 0), (self.x + 25, self.y + 18), 2)

        elif self.type == "banana":
            # banaan
            pygame.draw.arc(screen, (255, 230, 0), (self.x + 5, self.y + 5, 30, 25), 0.5, 2.8, 6)
            pygame.draw.arc(screen, (255, 210, 0), (self.x + 8, self.y + 8, 24, 18), 0.5, 2.8, 4)

        elif self.type == "apple":
            # appel
            pygame.draw.circle(screen, (220, 0, 0), (self.x + 20, self.y + 22), 14)
            pygame.draw.rect(screen, (120, 70, 20), (self.x + 18, self.y + 6, 4, 8))
            pygame.draw.ellipse(screen, (0, 180, 0), (self.x + 22, self.y + 7, 10, 6))

        elif self.type == "pear":
            # peer
            pygame.draw.circle(screen, (100, 220, 80), (self.x + 20, self.y + 14), 10)
            pygame.draw.ellipse(screen, (100, 220, 80), (self.x + 10, self.y + 16, 20, 20))
            pygame.draw.rect(screen, (120, 70, 20), (self.x + 18, self.y + 3, 4, 7))

        elif self.type == "strawberry":
            # aardbei
            pygame.draw.polygon(screen, (220, 0, 50), [
                (self.x + 20, self.y + 38),
                (self.x + 7, self.y + 16),
                (self.x + 33, self.y + 16)
            ])
            pygame.draw.polygon(screen, (0, 180, 0), [
                (self.x + 20, self.y + 10),
                (self.x + 14, self.y + 16),
                (self.x + 20, self.y + 14),
                (self.x + 26, self.y + 16)
            ])
            for seed_x, seed_y in [(16, 24), (20, 28), (24, 24), (18, 32), (22, 32)]:
                pygame.draw.circle(screen, (255, 230, 120), (self.x + seed_x, self.y + seed_y), 1)

        elif self.type == "bomb":
            # bom
            pygame.draw.circle(screen, (50, 50, 50), (self.x + 20, self.y + 22), 16)
            pygame.draw.rect(screen, (100, 100, 100), (self.x + 18, self.y + 6, 4, 8))
            pygame.draw.line(screen, (220, 220, 220), (self.x + 20, self.y + 6), (self.x + 28, self.y - 2), 2)
            pygame.draw.circle(screen, (255, 140, 0), (self.x + 30, self.y - 3), 3)

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def spawn_object(screen_width):
    return FallingObject(screen_width)