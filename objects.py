import random
import pygame

# Emoji mapping
FRUIT_EMOJIS = {
    "melon": "🍉",
    "banana": "🍌",
    "apple": "🍎",
    "pear": "🍐",
    "strawberry": "🍓",
    "bomb": "💣"
}

class FallingObject:
    def __init__(self, screen_width):
        self.width = 40
        self.height = 40
        self.x = random.randint(0, screen_width - self.width)
        self.y = -self.height

        self.type = random.choice(list(FRUIT_EMOJIS.keys()))
        self.speed = random.randint(3, 7)

        # Font voor emoji (iets groter voor zichtbaarheid)
        self.font = pygame.font.SysFont(None, 40)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        emoji = FRUIT_EMOJIS[self.type]

        text = self.font.render(emoji, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y))

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def spawn_object(screen_width):
    return FallingObject(screen_width)