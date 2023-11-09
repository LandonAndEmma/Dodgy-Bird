import pygame
import math
import random

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music/music.wav")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
FPS = 240
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodgy Bird")

bg = pygame.image.load("sprites/bg.png").convert()
bird = pygame.image.load("sprites/bird.png").convert()
enemy = pygame.image.load("sprites/enemy.png").convert()
bg_width = bg.get_width()
bird_width = bird.get_width()
bird_height = bird.get_height()
bg_rect = bg.get_rect()
bird_rect = bird.get_rect()
bird_pos_x = SCREEN_WIDTH / 2
bird_pos_x = bird_pos_x - bird_width
bird_pos_y = SCREEN_HEIGHT / 2
bird_pos_y = bird_pos_y - bird_height
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

# Create a list to store enemy positions, speeds, and rectangles
enemies = []

score = 0


def spawn_enemy():
    enemy_pos_x = SCREEN_WIDTH
    enemy_pos_y = random.randint(0, SCREEN_HEIGHT - enemy.get_height())
    enemy_speed = 5
    enemy_rect = enemy.get_rect()
    enemy_rect.topleft = (enemy_pos_x, enemy_pos_y)
    enemies.append((enemy, enemy_rect, enemy_speed))


def check_collision():
    for _, enemy_rect, _ in enemies:
        if bird_rect.colliderect(enemy_rect):
            return True
    return False


def show_game_over_screen():
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over - Push R to restart", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen.blit(text, text_rect)


def restart_game():
    global bird_pos_y, bird_pos_x, scroll, enemies, score, game_over, bird
    bird = pygame.image.load("sprites/bird.png").convert()
    bird_pos_y = SCREEN_HEIGHT / 2 - bird_height
    bird_pos_x = SCREEN_WIDTH / 2 - bird_width
    scroll = 0
    enemies = []
    score = 0
    game_over = False


game_over = False
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            if game_over:
                restart_game()

    if not game_over:
        key = pygame.key.get_pressed()

        if key[pygame.K_UP] and bird_pos_y > 0:
            bird_pos_y -= 2
        if key[pygame.K_DOWN] and bird_pos_y < SCREEN_HEIGHT - bird_height:
            bird_pos_y += 2
        if key[pygame.K_LEFT] and bird_pos_x > 0:
            bird = pygame.image.load("sprites/flipped.png").convert()
            bird_pos_x -= 2
        if key[pygame.K_RIGHT] and bird_pos_x < SCREEN_WIDTH - bird_width:
            bird = pygame.image.load("sprites/bird.png").convert()
            bird_pos_x += 2

        for i in range(tiles):
            bg_x = i * bg_width - scroll
            screen.blit(bg, (bg_x, 0))

        # Scroll the background
        scroll += 2
        if scroll >= bg_width:
            scroll = 0

        # Spawn enemies periodically
        if random.randint(1, 120) == 1:
            spawn_enemy()

        # Update and draw enemies
        for enemy, enemy_rect, enemy_speed in enemies:
            enemy_rect.x -= enemy_speed
            screen.blit(enemy, enemy_rect)

            if enemy_rect.right <= 0:
                score += 1
                enemies.remove((enemy, enemy_rect, enemy_speed))

        # Update bird's rectangle position
        bird_rect.topleft = (bird_pos_x, bird_pos_y)

        # Check for collisions
        if check_collision():
            game_over = True

        # Draw the bird on top
        screen.blit(bird, bird_rect)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    if game_over:
        show_game_over_screen()
        pygame.display.flip()

pygame.quit()
