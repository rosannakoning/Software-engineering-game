import pygame
from objects import spawn_object

pygame.init()

## --- SOUNDS ---
# Let op: Zorg dat deze bestanden echt in de map 'sounds' staan!
catch_sound = pygame.mixer.Sound("sounds/fallingsounds.wav")
catch_sound.set_volume(0.5)

missing_sound = pygame.mixer.Sound("sounds/error.wav")
missing_sound.set_volume(0.8)

start_sound = pygame.mixer.Sound("sounds/button.wav")
start_sound.set_volume(0.5)

background_song = pygame.mixer.Sound("sounds/backgroundsong.wav")
background_song.set_volume(0.05)


# Scherm instellingen
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

# Score instellingen
score = 0 
font = pygame.font.SysFont(None, 36)

# --- START DE MUZIEK HIER ---
background_song.play(-1)  # -1 betekent dat het liedje oneindig herhaalt

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
            score += 1 
            catch_sound.play()  # Speel geluid als je iets vangt!
            falling_objects.remove(obj)
        
        # Verwijder als het object de grond raakt
        elif obj.is_off_screen(screen_height):
            missing_sound.play() # Speel geluid als je mist!
            falling_objects.remove(obj)

    # --- TEKENEN ---
    screen.fill((135, 206, 235)) # Blauwe lucht

    # Teken mandje
    pygame.draw.rect(screen, (139, 69, 19), basket)

    # Teken de vallende objecten
    for obj in falling_objects:
        obj.draw(screen)

    # Score op het scherm
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    pygame.display.update()

pygame.quit()