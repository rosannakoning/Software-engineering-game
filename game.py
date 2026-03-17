import pygame
from objects import spawn_object

pygame.init()

## sounds 
catch_sound = pygame.mixer.Sound("/Users/romynguyen/Software-engineering-game/sounds/fallingsounds.wav")
catch_sound.set_volume(0.5)
missing_sound = pygame.mixer.Sound("/Users/romynguyen/Software-engineering-game/sounds/error.wav")
missing_sound.set_volume(0.8)


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit Catch Game")

clock = pygame.time.Clock()

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

    # --- BESTURING AANGEPAST VOOR PIJLTJES ---
    keys = pygame.key.get_pressed()
    # Nu werkt A én het linkerpijltje
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        basket.x -= basket_speed
    # Nu werkt D én het rechterpijltje
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        basket.x += basket_speed

    # Grenzen bewaken
    if basket.x < 0:
        basket.x = 0
    if basket.x > screen_width - basket.width:
        basket.x = screen_width - basket.width

    spawn_timer += 1
    if spawn_timer >= spawn_delay:
        falling_objects.append(spawn_object(screen_width))
        spawn_timer = 0

    for obj in falling_objects[:]:
        obj.update()

        if obj.get_rect().colliderect(basket):
            catch_sound.play()
            falling_objects.remove(obj)
        elif obj.is_off_screen(screen_height):
            missing_sound.play()
            falling_objects.remove(obj)

    screen.fill((0, 0, 0))

    # mandje tekenen
    pygame.draw.rect(screen, (139, 69, 19), basket)
    pygame.draw.line(screen, (160, 82, 45), (basket.x, basket.y + 10), (basket.x + basket.width, basket.y + 10), 2)
    pygame.draw.line(screen, (160, 82, 45), (basket.x, basket.y + 20), (basket.x + basket.width, basket.y + 20), 2)

    for obj in falling_objects:
        obj.draw(screen)

    pygame.display.flip()

pygame.quit()