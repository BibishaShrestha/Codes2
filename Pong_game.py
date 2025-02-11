import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong Game')


# Define colors and constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY=(128,128,128)
FPS = 60

# Define font
font= pygame.font.SysFont("Times New Roman",40)

# Initialize scores
left_score = 0
right_score = 0

# Define the paddle 
paddle_height = 100
paddle_width = 15
paddle_speed= 7
ball_radius= 10
ball_speed_x= 3
ball_speed_y= 3
Max_Speed= 4.5
Speed_Increase=0.5

# Create the paddles and ball
left_paddle = pygame.Rect(50, HEIGHT/2 - paddle_height/2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 50 - paddle_width, HEIGHT/2 - paddle_height/2, paddle_width, paddle_height)
ball = pygame.Rect(WIDTH/2 - ball_radius/2, HEIGHT/2 - ball_radius/2, ball_radius, ball_radius)

#Load the background image
background_image = pygame.image.load('bg.png')  
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  


# Function to draw
def draw():
    screen.fill(BLACK)
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, WHITE,left_paddle)
    pygame.draw.rect(screen, WHITE,right_paddle)
    pygame.draw.ellipse(screen,WHITE, ball)
    pygame.draw.line(screen, GREY, (WIDTH/2,0), (WIDTH/2,HEIGHT),7)
    # Draw the border around the screen
    pygame.draw.rect(screen, GREY, (0, 0, WIDTH, HEIGHT), 12)
    score_text = font.render(f"{left_score} - {right_score}", True, WHITE)
    screen.blit(score_text, (WIDTH/2 - score_text.get_width()/2, 20))
    pygame.display.flip()

# Function to display the winner
def display_winner(winner):
    winner_text = font.render(f"{winner} Wins!", True, WHITE)
    screen.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.flip()

# Main section
clock = pygame.time.Clock()
running = True

# Initialize the pygame mixer for music
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load('music.mp3')  
pygame.mixer.music.set_volume(0.3)  
pygame.mixer.music.play(-1, 0)  

while running:
    clock.tick(FPS)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

 # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += paddle_speed

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
        if abs(ball_speed_x) < Max_Speed:
            ball_speed_x += Speed_Increase* (1 if ball_speed_x > 0 else -1)
        if abs(ball_speed_y) < Max_Speed:
            ball_speed_y += Speed_Increase * (1 if ball_speed_y > 0 else -1)

    # Ball out of the boundary 
    if ball.left <= 0:
        right_score += 1
        ball = pygame.Rect(WIDTH/2 - ball_radius/2, HEIGHT/2 - ball_radius/2, ball_radius, ball_radius)
        ball_speed_x *= random.choice([1, -1])  # Random direction
    elif ball.right >= WIDTH:
        left_score += 1
        ball = pygame.Rect(WIDTH/2 - ball_radius/2, HEIGHT/2 - ball_radius/2, ball_radius, ball_radius)
        ball_speed_x*= random.choice([1, -1])  # Random direction

    # Check if a player has won
    if left_score == 5:
        display_winner("Player 1 (Left)")
        pygame.time.wait(4000) 
        running = False
    elif right_score == 5:
        display_winner("Player 2 (Right)")
        pygame.time.wait(4000)  
        running = False
    
    draw()     

# Quit pygame
pygame.quit()
sys.exit()