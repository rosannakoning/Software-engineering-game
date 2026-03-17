import pygame
from objects import spawn_object

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit Catch Game")

clock = pygame.time.Clock()

# --- VARIABELEN ---
basket = pygame.Rect(350, 530, 100, 40)
basket_speed = 7

falling_objects = []
spawn_timer = 0
spawn_delay = 40

score = 0
lives = 3

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

def is_bomb(obj):
    # Pas dit aan als jouw bomb-kenmerk anders heet in objects.py
    return hasattr(obj, "type") and obj.type == "bomb"

running = True
game_over = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # reset game
                basket.x = 350
                falling_objects.clear()
                spawn_timer = 0
                score = 0
                lives = 3
                game_over = False

    if not game_over:
        # BESTURING (A/D én Pijltjes)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            basket.x -= basket_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            basket.x += basket_speed

        # Grenzen bewaken
        if basket.x < 0:
            basket.x = 0
        if basket.x > screen_width - basket.width:
            basket.x = screen_width - basket.width

        # Logica van de vallende objecten
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            falling_objects.append(spawn_object(screen_width))
            spawn_timer = 0

        for obj in falling_objects[:]:
            obj.update()

            # Check voor botsing met mandje
            if obj.get_rect().colliderect(basket):
                if is_bomb(obj):
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                else:
                    score += 1  # alleen fruit geeft punten

                falling_objects.remove(obj)

            # Verwijder als het object van het scherm valt
            elif obj.is_off_screen(screen_height):
                falling_objects.remove(obj)

    # TEKENEN
    screen.fill((0, 0, 0))  # Zwarte achtergrond

    # Teken mandje
    pygame.draw.rect(screen, (139, 69, 19), basket)

    # Teken de vallende objecten
    for obj in falling_objects:
        obj.draw(screen)

    # Score linksboven
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Hartjes rechtsboven
    heart_text = font.render("❤️" * lives, True, (255, 255, 255))
    heart_x = screen_width - heart_text.get_width() - 20
    screen.blit(heart_text, (heart_x, 20))

    # Game over scherm
    if game_over:
        game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Druk op R om opnieuw te beginnen", True, (255, 255, 255))

        screen.blit(
            game_over_text,
            (
                screen_width // 2 - game_over_text.get_width() // 2,
                screen_height // 2 - 50
            )
        )
        screen.blit(
            restart_text,
            (
                screen_width // 2 - restart_text.get_width() // 2,
                screen_height // 2 + 20
            )
        )

    pygame.display.update()

pygame.quit()