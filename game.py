import pygame
from objects import spawn_object
import random
import math

pygame.init()
pygame.mixer.init()

# --- SOUNDS ---
catch_sound = pygame.mixer.Sound("sounds/fallingsounds.wav")
catch_sound.set_volume(0.5)

missing_sound = pygame.mixer.Sound("sounds/error.wav")
missing_sound.set_volume(0.8)

start_sound = pygame.mixer.Sound("sounds/button.wav")
start_sound.set_volume(0.5)

background_song = pygame.mixer.Sound("sounds/backgroundsong.wav")
background_song.set_volume(0.05)

# explosion_sound = pygame.mixer.Sound("sounds/falling_bomb.wav")
# explosion_sound.set_volume(0.7)

# --- Display Settings ---
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruit Catch Game")

clock = pygame.time.Clock()

# --- VARIABLES ---
basket = pygame.Rect(350, 530, 100, 40)
basket_speed = 7

falling_objects = []
spawn_timer = 0
spawn_delay = 40

score = 0
lives = 3

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# --- LIFES --- 
def draw_heart(screen, x, y, size=10):
    pygame.draw.circle(screen, (255, 0, 0), (x, y), size)
    pygame.draw.circle(screen, (255, 0, 0), (x + size, y), size)

    points = [
        (x - size, y),
        (x + 2 * size, y),
        (x + size // 2, y + 2 * size)
    ]
    pygame.draw.polygon(screen, (255, 0, 0), points)

# --- Pause Menu ---
def pause_menu(screen, font, big_font, score, background_song):
    paused = True
    sound_on = background_song.get_volume() > 0

    # Buttons
    restart_button = pygame.Rect(300, 200, 200, 50)
    continue_button = pygame.Rect(300, 270, 200, 50)
    sound_button = pygame.Rect(300, 340, 200, 50)
    score_button = pygame.Rect(300, 410, 200, 50)

    button_color = (255, 165, 0)   # Orange
    hover_color = (255, 200, 50)   # Lighter with hover
    text_color = (255, 255, 255)   # White

    while paused:
        screen.fill((135, 206, 235))  # Achtergrond

        # PAUSED Text
        paused_text = big_font.render("PAUSED", True, (255, 0, 0))
        screen.blit(
            paused_text,
            (
                screen.get_width() // 2 - paused_text.get_width() // 2,
                100
            )
        )

        # Hover buttons
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for rect in [restart_button, continue_button, sound_button, score_button]:
            if rect.collidepoint(mouse_x, mouse_y):
                pygame.draw.rect(screen, hover_color, rect, border_radius=10)
            else:
                pygame.draw.rect(screen, button_color, rect, border_radius=10)

        # Text buttons
        screen.blit(font.render("Restart", True, text_color), (restart_button.x + 50, restart_button.y + 10))
        screen.blit(font.render("Continue", True, text_color), (continue_button.x + 50, continue_button.y + 10))
        screen.blit(font.render(f"Sound {'On' if sound_on else 'Off'}", True, text_color), (sound_button.x + 20, sound_button.y + 10))
        screen.blit(font.render(f"Score: {score}", True, text_color), (score_button.x + 50, score_button.y + 10))

        pygame.display.update()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if restart_button.collidepoint(mx, my):
                    return "restart", sound_on
                elif continue_button.collidepoint(mx, my):
                    return "continue", sound_on
                elif sound_button.collidepoint(mx, my):
                    sound_on = not sound_on
                    if sound_on:
                        background_song.set_volume(0.05)
                    else:
                        background_song.set_volume(0)

# --- Explosion ---
def draw_explosion(screen, x, y, num_particles=50):
    """Heftige explosie-effect met lijnen, geen rondje."""
    for _ in range(num_particles):
        length = random.randint(20, 60)           # lengte van elke vonk
        angle = random.uniform(0, 2 * math.pi)    # richting willekeurig
        end_x = x + int(length * math.cos(angle))
        end_y = y + int(length * math.sin(angle))
        # kleur varieert van geel → oranje → rood
        color = (255, random.randint(150, 255), 0)
        pygame.draw.line(screen, color, (x, y), (end_x, end_y), 3)


# Start Background Music
background_song.play(-1)

running = True
game_over = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                start_sound.play()
                basket.x = 350
                falling_objects.clear()
                spawn_timer = 0
                score = 0
                lives = 3
                game_over = False

    if not game_over:
        # Control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            basket.x -= basket_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            basket.x += basket_speed
        
        # Pause key
        if keys[pygame.K_p]:
            action, sound_on = pause_menu(screen, font, big_font, score, background_song)
            if action == "restart":
                basket.x = 350
                falling_objects.clear()
                spawn_timer = 0
                score = 0
                lives = 3
                game_over = False
            

        # Boundaries
        if basket.x < 0:
            basket.x = 0
        if basket.x > screen_width - basket.width:
            basket.x = screen_width - basket.width

        # New Objects 
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            falling_objects.append(spawn_object(screen_width))
            spawn_timer = 0

        # Objects Updating
        for obj in falling_objects[:]:
            obj.update()

            # Touching Basket
            if obj.get_rect().colliderect(basket):
                if obj.type == "bomb":
                    lives -= 1
                    explosion_sound.play()
                    draw_explosion(screen, obj.x + obj.width//2, obj.y + obj.height//2, num_particles=70)
                    pygame.display.update()
                    pygame.time.delay(200)   # short pause
                    if lives <= 0:
                        game_over = True
                else:
                    score += 1
                    catch_sound.play()

                falling_objects.remove(obj)

            # Missed Objects
            elif obj.is_off_screen(screen_height):
                if obj.type != "bomb":
                    missing_sound.play()
                falling_objects.remove(obj)

    # --- Drawing ---
    screen.fill((135, 206, 235))  # blue sky

    # Basket
    pygame.draw.rect(screen, (139, 69, 19), basket)

    # Falling objects
    for obj in falling_objects:
        obj.draw(screen)

    # Score left corner
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Harts right corner
    for i in range(lives):
        draw_heart(screen, screen_width - 80 - (i * 50), 30, 10)

    # Game Over screen
    if game_over:
        game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Druk op R om opnieuw te beginnen", True, (255, 255, 255))
        final_score_text = font.render(f"Eindscore: {score}", True, (255, 255, 255))

        screen.blit(
            game_over_text,
            (
                screen_width // 2 - game_over_text.get_width() // 2,
                screen_height // 2 - 80
            )
        )
        screen.blit(
            final_score_text,
            (
                screen_width // 2 - final_score_text.get_width() // 2,
                screen_height // 2
            )
        )
        screen.blit(
            restart_text,
            (
                screen_width // 2 - restart_text.get_width() // 2,
                screen_height // 2 + 50
            )
        )

    pygame.display.update()

pygame.quit()