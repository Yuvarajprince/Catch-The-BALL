import pygame
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
width = 600
height = 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the Ball")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0,255,0)

# Load sound effects
catch_sound = pygame.mixer.Sound("catch.mp3")
miss_sound = pygame.mixer.Sound("miss.mp3")

# Ball properties
ball_radius = 10
ball_speed = 5
ball_x = 0
ball_y = 0
def reset_ball():
    global ball_x,ball_y
    ball_x = random.randint(0, width)
    ball_y = 0
reset_ball()

# Paddle properties
paddle_width = 80
paddle_height = 15
paddle_x = width // 2 - paddle_width // 2
paddle_y = height - paddle_height - 10
paddle_speed = 10

# Game variables
score = 0
lives = 3
font = pygame.font.Font(None, 36)
speed_increase_rate = 1
score_for_speed_increase = 5
game_state = "start_menu"  # Start in the start menu state

# Function to display text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "start_menu" or game_state=="game_over": #check game state
                    game_state = "playing"
                    score = 0
                    lives = 3
                    ball_speed = 5
                    reset_ball()

    if game_state == "playing":
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < width - paddle_width:
            paddle_x += paddle_speed

        # Ball movement
        ball_y += ball_speed
        if ball_y > height:
            reset_ball()
            lives -= 1
            miss_sound.play()
            if lives <= 0:
                game_state = "game_over"

        # Collision detection
        if ball_y + ball_radius >= paddle_y and ball_x >= paddle_x and ball_x <= paddle_x + paddle_width:
            reset_ball()
            score += 1
            catch_sound.play()
            if score % score_for_speed_increase == 0 and score != 0:
                ball_speed += speed_increase_rate

    # Drawing
    screen.fill(white)

    if game_state == "start_menu":
        draw_text("Catch the Ball", pygame.font.Font(None, 72), black, width // 2 - 180, height // 2 - 100)
        draw_text("Press SPACE to Start", font, black, width // 2 - 120, height // 2 + 50)

    elif game_state == "playing":
        pygame.draw.circle(screen, red, (ball_x, ball_y), ball_radius)
        pygame.draw.rect(screen, black, (paddle_x, paddle_y, paddle_width, paddle_height))
        draw_text("Score: " + str(score), font, black, 10, 10)
        draw_text("Lives: " + str(lives), font, black, width - 100, 10)

    elif game_state == "game_over":
        draw_text("Game Over", pygame.font.Font(None, 72), red, width // 2 - 150, height // 2 - 100)
        draw_text("Final Score: " + str(score), font, black, width // 2 - 100, height // 2 + 50)
        draw_text("Press SPACE to restart",font,green,width//2-120,height//2+100)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
