import random
import pygame


class FallingObject:
    def __init__(self, screen_width: int, object_type: str):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height

        self.object_type = object_type

        if object_type == "good":
            self.color = (0, 200, 0)      # groen
            self.speed = random.randint(4, 7)
            self.points = 1
        elif object_type == "bad":
            self.color = (200, 0, 0)      # rood
            self.speed = random.randint(5, 8)
            self.points = -1
        else:
            raise ValueError("object_type must be 'good' or 'bad'")

    def update(self) -> None:
        self.y += self.speed

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def is_off_screen(self, screen_height: int) -> bool:
        return self.y > screen_height

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)


def spawn_object(screen_width: int) -> FallingObject:
    object_type = random.choice(["good", "bad"])
    return FallingObject(screen_width, object_type)