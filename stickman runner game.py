import pygame
import random
import sys
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stickman Runner Game")
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
clock = pygame.time.Clock()
FPS = 60
stickman_frames = []
for i in range(1, 6):
    img = pygame.image.load(f"png {i}.png").convert_alpha()
    img = pygame.transform.scale(img, (50, 60))
    stickman_frames.append(img)
obstacle_img = pygame.image.load("obstacle.png").convert_alpha()
obstacle_img = pygame.transform.scale(obstacle_img, (30, 50))
font = pygame.font.SysFont("arial", 30)
def draw_button(screen, rect, text, color, text_color):
    pygame.draw.rect(screen, color, rect)
    button_font = pygame.font.SysFont(None, 50)
    text_surf = button_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
def wait_for_retry():
    retry_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 60)
    while True:
        screen.fill((0, 0, 0))
        game_over_text = font.render("Game Over!", True, RED)
        text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(game_over_text, text_rect)
        draw_button(screen, retry_rect, "Retry", GREEN, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return
def game():
    stickman_width = 50
    stickman_height = 60
    stickman_x = 100
    stickman_y = HEIGHT - stickman_height - 50
    stickman_vel_y = 0
    gravity = 0.8
    jump_power = -15
    is_jumping = False
    obstacle_width = 30
    obstacle_height = 50
    obstacle_speed = 7
    obstacle_list = []
    current_frame = 0
    frame_count = 0
    frame_delay = 5
    score = 0
    spawn_timer = 0
    run = True
    while run:
        clock.tick(FPS)
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, (0, HEIGHT-50, WIDTH, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping:
            stickman_vel_y = jump_power
            is_jumping = True
        stickman_y += stickman_vel_y
        stickman_vel_y += gravity
        if stickman_y >= HEIGHT - stickman_height - 50:
            stickman_y = HEIGHT - stickman_height - 50
            stickman_vel_y = 0
            is_jumping = False
        spawn_timer += 1
        if spawn_timer > 90:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - obstacle_height - 50
            obstacle_list.append(
                pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)
            )
            spawn_timer = 0
        stickman_rect = pygame.Rect(
            stickman_x, stickman_y, stickman_width, stickman_height
        )
        for obs in obstacle_list[:]:
            obs.x -= obstacle_speed
            screen.blit(obstacle_img, (obs.x, obs.y))
            if obs.x + obstacle_width < 0:
                obstacle_list.remove(obs)
                score += 1
            if stickman_rect.colliderect(obs):
                run = False
        screen.blit(stickman_frames[current_frame], (stickman_x, stickman_y))
        frame_count += 1
        if frame_count >= frame_delay:
            current_frame = (current_frame + 1) % len(stickman_frames)
            frame_count = 0
        score_text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
while True:
    game()
    wait_for_retry()