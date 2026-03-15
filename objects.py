import random
import pygame


class FallingObject:
    def __init__(self, screen_width: int, object_type: str):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height

        self.object_type = object_type
        self.exploded = False
        self.explosion_timer = 0

        if object_type == "gift":
            self.speed = random.randint(4, 7)
            self.points = 1
        elif object_type == "bomb":
            self.speed = random.randint(5, 8)
            self.points = -1
        else:
            raise ValueError("object_type must be 'gift' or 'bomb'")

    def update(self) -> None:
        if self.exploded:
            self.explosion_timer -= 1
        else:
            self.y += self.speed

    def draw(self, screen: pygame.Surface) -> None:
        if self.exploded:
            self.draw_explosion(screen)
        elif self.object_type == "gift":
            self.draw_gift(screen)
        elif self.object_type == "bomb":
            self.draw_bomb(screen)

    def draw_gift(self, screen: pygame.Surface) -> None:
        # Doos
        pygame.draw.rect(screen, (0, 180, 255), (self.x, self.y, self.width, self.height))
        
        # Linten
        pygame.draw.rect(screen, (255, 255, 0), (self.x + 16, self.y, 8, self.height))
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y + 16, self.width, 8))

        # Strik
        pygame.draw.circle(screen, (255, 0, 255), (self.x + 14, self.y + 8), 6)
        pygame.draw.circle(screen, (255, 0, 255), (self.x + 26, self.y + 8), 6)

    def draw_bomb(self, screen: pygame.Surface) -> None:
        # Bom lichaam
        pygame.draw.circle(
            screen,
            (50, 50, 50),
            (self.x + self.width // 2, self.y + self.height // 2),
            self.width // 2
        )

        # Lont
        pygame.draw.line(
            screen,
            (200, 200, 200),
            (self.x + self.width // 2, self.y),
            (self.x + self.width // 2 + 10, self.y - 10),
            3
        )

        # Vonk
        pygame.draw.circle(screen, (255, 200, 0), (self.x + self.width // 2 + 10, self.y - 10), 4)

    def draw_explosion(self, screen: pygame.Surface) -> None:
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2

        pygame.draw.circle(screen, (255, 120, 0), (center_x, center_y), 25)
        pygame.draw.circle(screen, (255, 200, 0), (center_x, center_y), 15)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 7)

    def explode(self) -> None:
        self.exploded = True
        self.explosion_timer = 15  # aantal frames dat de explosie zichtbaar blijft

    def is_finished(self, screen_height: int) -> bool:
        if self.exploded:
            return self.explosion_timer <= 0
        return self.y > screen_height

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)


def spawn_object(screen_width: int) -> FallingObject:
    object_type = random.choice(["gift", "bomb"])
    return FallingObject(screen_width, object_type)