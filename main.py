import pygame
import sys
import random
import math
import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")  # Твій MP3-файл у тій самій папці
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
BARRIER_WIDTH = 20
BARRIER_HEIGHT = 150

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BARRIER_COLOR = (200, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vertical Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 40)

# ДОДАНО: ЗАСТАВКА
menu_background = pygame.image.load("menu_background.jpg")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))


menu_background = pygame.image.load("menu_background.jpg")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

paddle_speed = 5
ball_speed_x = 4 * random.choice([-1, 1])
ball_speed_y = 4 * random.choice([-1, 1])

score_left = 0
score_right = 0
game_active = False
game_over = False
frozen = False
frozen_owner = None
freeze_uses = {"left": 3, "right": 3}
boost_uses = {"left": 3, "right": 3}
boost_active = False
boost_owner = None
wave_uses = {"left": 3, "right": 3}
wave_active = False
wave_owner = None
wave_time = 0
wave_amplitude = 50
wave_frequency = 0.05
original_y = ball.centery

barrier_active = False
barrier = pygame.Rect(0, 0, BARRIER_WIDTH, BARRIER_HEIGHT)
barrier.centerx = WIDTH // 2
barrier_appear_time = 0
BARRIER_SHOW_TIME = 15
BARRIER_INTERVAL = 35
last_barrier_time = 0

vs_bot = False
start_time = 0
last_speedup_time = 0

def reset_positions():
    global ball, ball_speed_x, ball_speed_y, original_y
    global frozen, frozen_owner, boost_active, boost_owner
    global wave_active, wave_owner, wave_time
    left_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    right_paddle.y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    ball.center = (WIDTH // 2, HEIGHT // 2)
    original_y = ball.centery
    ball_speed_x = 4 * random.choice([-1, 1])
    ball_speed_y = 4 * random.choice([-1, 1])
    frozen = False
    frozen_owner = None
    boost_active = False
    boost_owner = None
    wave_active = False
    wave_owner = None
    wave_time = 0

def spawn_barrier():
    global barrier_active, barrier, barrier_appear_time
    barrier_active = True
    y = random.randint(BARRIER_HEIGHT // 2 + 10, HEIGHT - BARRIER_HEIGHT // 2 - 10)
    barrier.centerx = WIDTH // 2
    barrier.centery = y
    barrier_appear_time = time.time()

while True:
    screen.blit(menu_background, (0, 0))
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_active and not game_over:
        title = big_font.render("Vertical Pong", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))

        mode_text = font.render("Press '1' for 2 Players or '2' to Play vs Bot", True, WHITE)
        screen.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, 90))

        left_instr = [
            "Left Player Controls:",
            "W/S - Move Up/Down",
            "F - Boost Ball Speed (3x)",
            "E - Freeze Ball (3x)",
            "R - Release Frozen Ball",
            "D - Sinusoidal Ball Motion (3x)"
        ]
        right_instr = [
            "Right Player Controls:",
            "Arrow Up/Down - Move Up/Down",
            "I - Boost Ball Speed (3x)",
            "L - Freeze Ball (3x)",
            "K - Release Frozen Ball",
            "O - Sinusoidal Ball Motion (3x)"
        ]
        for i, line in enumerate(left_instr):
            text = font.render(line, True, WHITE)
            screen.blit(text, (50, 140 + i * 30))
        for i, line in enumerate(right_instr):
            text = font.render(line, True, WHITE)
            screen.blit(text, (420, 140 + i * 30))
        if keys[pygame.K_1]:
            vs_bot = False
            score_left = score_right = 0
            freeze_uses = {"left": 3, "right": 3}
            boost_uses = {"left": 3, "right": 3}
            wave_uses = {"left": 3, "right": 3}
            reset_positions()
            last_barrier_time = time.time()
            start_time = time.time()
            last_speedup_time = start_time
            barrier_active = False
            game_active = True
        elif keys[pygame.K_2]:
            vs_bot = True
            score_left = score_right = 0
            freeze_uses = {"left": 3, "right": 3}
            boost_uses = {"left": 3, "right": 3}
            wave_uses = {"left": 3, "right": 3}
            reset_positions()
            last_barrier_time = time.time()
            start_time = time.time()
            last_speedup_time = start_time
            barrier_active = False
            game_active = True

    elif game_active:
        current_time = time.time()
        if current_time - start_time > 120 and current_time - last_speedup_time > 10:
            if not frozen:
                ball_speed_x *= 1.1
                ball_speed_y *= 1.1
                last_speedup_time = current_time

        if barrier_active and current_time - barrier_appear_time > BARRIER_SHOW_TIME:
            barrier_active = False
            last_barrier_time = current_time
        if not barrier_active and current_time - last_barrier_time > BARRIER_INTERVAL:
            spawn_barrier()

        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed

        if not vs_bot:
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= paddle_speed
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += paddle_speed
        else:
            if ball.centery < right_paddle.centery and right_paddle.top > 0:
                right_paddle.y -= paddle_speed
            elif ball.centery > right_paddle.centery and right_paddle.bottom < HEIGHT:
                right_paddle.y += paddle_speed

            if boost_uses["right"] > 0 and not boost_active and not frozen and random.random() < 0.002:
                ball_speed_x *= 1.5
                ball_speed_y *= 1.5
                boost_active = True
                boost_owner = "right"
                boost_uses["right"] -= 1
            if freeze_uses["right"] > 0 and not frozen and random.random() < 0.002:
                frozen = True
                frozen_owner = "right"
                freeze_uses["right"] -= 1
                ball_speed_x = 0
                ball_speed_y = 0
            if frozen and frozen_owner == "right" and random.random() < 0.01:
                ball_speed_x = -5
                ball_speed_y = 5
                frozen = False
            if wave_uses["right"] > 0 and not frozen and not wave_active and random.random() < 0.002:
                wave_active = True
                wave_owner = "right"
                wave_uses["right"] -= 1
                ball_speed_x *= 1.2
                ball_speed_y = 0
                original_y = ball.centery
                wave_time = 0

        if keys[pygame.K_f] and boost_uses["left"] > 0 and not boost_active and not frozen:
            ball_speed_x *= 1.5
            ball_speed_y *= 1.5
            boost_active = True
            boost_owner = "left"
            boost_uses["left"] -= 1

        if keys[pygame.K_e] and freeze_uses["left"] > 0 and not frozen:
            frozen = True
            frozen_owner = "left"
            freeze_uses["left"] -= 1
            ball_speed_x = 0
            ball_speed_y = 0
        if frozen and frozen_owner == "left" and keys[pygame.K_r]:
            ball_speed_x = 5
            ball_speed_y = 5
            frozen = False

        if keys[pygame.K_d] and wave_uses["left"] > 0 and not wave_active and not frozen:
            wave_active = True
            wave_owner = "left"
            wave_uses["left"] -= 1
            ball_speed_x *= 1.2
            ball_speed_y = 0
            original_y = ball.centery
            wave_time = 0

        if not frozen:
            ball.x += ball_speed_x
            if wave_active:
                wave_time += 1
                ball.y = original_y + wave_amplitude * math.sin(wave_frequency * wave_time)
            else:
                ball.y += ball_speed_y

        if not frozen and (ball.top <= 0 or ball.bottom >= HEIGHT):
            if not wave_active:
                ball_speed_y *= -1

        if ball.colliderect(left_paddle):
            ball_speed_x = abs(ball_speed_x)
            if boost_active and boost_owner != "left":
                boost_active = False
            if wave_active and wave_owner != "left":
                wave_active = False
        if ball.colliderect(right_paddle):
            ball_speed_x = -abs(ball_speed_x)
            if boost_active and boost_owner != "right":
                boost_active = False
            if wave_active and wave_owner != "right":
                wave_active = False

        if barrier_active and ball.colliderect(barrier):
            if ball.centerx < barrier.centerx:
                ball.right = barrier.left
                ball_speed_x = -abs(ball_speed_x)
            else:
                ball.left = barrier.right
                ball_speed_x = abs(ball_speed_x)

        if ball.left <= 0:
            score_right += 1
            reset_positions()
        if ball.right >= WIDTH:
            score_left += 1
            reset_positions()
        if score_left >= 10 or score_right >= 10:
            game_active = False
            game_over = True

        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
        if barrier_active:
            pygame.draw.rect(screen, BARRIER_COLOR, barrier)
        score_text = big_font.render(f"{score_left} : {score_right}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        if frozen:
            freeze_msg = font.render("\u2744\ufe0f Ball frozen", True, WHITE)
            screen.blit(freeze_msg, (WIDTH // 2 - freeze_msg.get_width() // 2, HEIGHT // 2 - 20))
        if wave_active:
            wave_msg = font.render("Sinusoidal motion", True, WHITE)

            screen.blit(wave_msg, (WIDTH // 2 - wave_msg.get_width() // 2, HEIGHT // 2 + 20))

    elif game_over:
        winner = "Left player" if score_left > score_right else "Right player"
        win_text = big_font.render(f"{winner} win!", True, WHITE)
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))
        if keys[pygame.K_r]:
            game_over = False
            game_active = False

    pygame.display.flip()
    clock.tick(60)

















