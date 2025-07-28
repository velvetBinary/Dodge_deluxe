import pygame
import random
import sys
import os

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Safe sound loader
def load_sound_safe(filename):
    if os.path.exists(filename):
        return pygame.mixer.Sound(filename)
    else:
        return type('', (), {"play": lambda self: None})()

# Load sounds safely
hit_sound = load_sound_safe('hit.wav')
score_sound = load_sound_safe('score.wav')
background_music = 'background.mp3'
if os.path.exists(background_music):
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌈 Crazy Dodger Deluxe 🌟")

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (255, 80, 80)
GREEN = (80, 255, 180)
BLUE = (80, 180, 255)
PURPLE = (200, 100, 255)
YELLOW = (255, 255, 100)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 36)
large_font = pygame.font.SysFont("Comic Sans MS", 64)

# Player settings
player_size = 50
player = pygame.Rect(WIDTH // 2, HEIGHT - 70, player_size, player_size)
player_speed = 7

# Object settings
enemy_size = 30
powerup_size = 25
enemies = []
powerups = []
spawn_rate = 20
powerup_spawn_rate = 150

# Background stars
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(100)]

# Score and power
score = 0
power = 1

def draw_background():
    screen.fill(BLACK)
    for star in stars:
        pygame.draw.circle(screen, PURPLE, (star[0], star[1]), star[2])
        star[1] += star[2]
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0

def draw_player():
    pygame.draw.ellipse(screen, BLUE, player)
    pygame.draw.rect(screen, WHITE, player, 2)

def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy, border_radius=6)
        pygame.draw.rect(screen, WHITE, enemy, 2, border_radius=6)

def draw_powerups():
    for p in powerups:
        pygame.draw.circle(screen, YELLOW, (p.x + powerup_size//2, p.y + powerup_size//2), powerup_size // 2)
        pygame.draw.circle(screen, WHITE, (p.x + powerup_size//2, p.y + powerup_size//2), powerup_size // 2, 2)

def show_score():
    score_text = font.render(f"Score: {score}  ⚡{power}", True, GREEN)
    screen.blit(score_text, (10, 10))

def game_over():
    hit_sound.play()
    msg = large_font.render("💥 GAME OVER 💥", True, RED)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

# Game loop
frame = 0
running = True
while running:
    clock.tick(60)
    draw_background()
    frame += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += player_speed

    # Spawn enemies
    if frame % spawn_rate == 0:
        x_pos = random.randint(0, WIDTH - enemy_size)
        enemies.append(pygame.Rect(x_pos, 0, enemy_size, enemy_size))

    # Spawn powerups
    if frame % powerup_spawn_rate == 0:
        x_pos = random.randint(0, WIDTH - powerup_size)
        powerups.append(pygame.Rect(x_pos, 0, powerup_size, powerup_size))

    # Move enemies
    for enemy in enemies[:]:
        enemy.y += 6
        if enemy.colliderect(player):
            game_over()
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            score += 1
            score_sound.play()

    # Move powerups
    for p in powerups[:]:
        p.y += 4
        if p.colliderect(player):
            power += 1
            powerups.remove(p)
            score_sound.play()
        elif p.y > HEIGHT:
            powerups.remove(p)

    draw_player()
    draw_enemies()
    draw_powerups()
    show_score()
    pygame.display.update()

pygame.quit()
