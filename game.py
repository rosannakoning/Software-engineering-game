import pygame
from objects import spawn_object

pygame.init()

# Scherm instellingen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit Catch Game")

clock = pygame.time.Clock()

# --- JOUW TAAK: DE SPELER ---
basket = pygame.Rect(350, 530, 100, 40)
basket_speed = 7

falling_objects = []
spawn_timer = 0
spawn_delay = 40

font = pygame.font.SysFont(None, 36)

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        basket.x -= basket_speed
    if keys[pygame.K_d]:
        basket.x += basket_speed

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
            falling_objects.remove(obj)
        # Verwijder als het object de grond raakt
        elif obj.is_off_screen(screen_height):
            falling_objects.remove(obj)

    # TEKENEN
    screen.fill((0, 0, 0)) # Zwarte achtergrond

    pygame.draw.rect(screen, (255, 255, 255), basket)

    # Teken de vallende objecten
    for obj in falling_objects:
        obj.draw(screen)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    pygame.display.update()

pygame.quit()