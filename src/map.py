import pygame
import sys

pygame.init()

width = 1600
height = 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Map')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)

goal = pygame.Rect(1550, 0, 50, 50)
static_obstacle1_rect = (150, 0, 200, 150)
static_obstacle2_rect = (600, 700, 400, 200)
static_obstacle3_rect = (1100, 0, 50, 500)

dynamic_obstacle1_pos = [300, 250]
dynamic_obstacle2_pos = [1400, 600]
dynamic_obstacle3_pos = [600, 600]
dynamic_obstacle_radius = 30
velocity1 = [-4, 0]
velocity2 = [0, -6]
velocity3 = [10, -4]

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dynamic_obstacle1_pos[0] += velocity1[0]
    dynamic_obstacle2_pos[1] += velocity2[1]
    
    if dynamic_obstacle1_pos[0] - dynamic_obstacle_radius <= 250 or dynamic_obstacle1_pos[0] + dynamic_obstacle_radius >= 1000:
        velocity1[0] = -velocity1[0]
    if dynamic_obstacle2_pos[1] - dynamic_obstacle_radius <= 100 or dynamic_obstacle2_pos[1] + dynamic_obstacle_radius >= 800:
        velocity2[1] = -velocity2[1]
    
    dynamic_obstacle3_pos[0] += velocity3[0]
    dynamic_obstacle3_pos[1] += velocity3[1]
    
    if dynamic_obstacle3_pos[0] - dynamic_obstacle_radius <= 200 or dynamic_obstacle3_pos[0] + dynamic_obstacle_radius >= 1000:
        velocity3[0] = -velocity3[0]
        velocity3[1] = -velocity3[1]
    
    screen.fill(black)
    pygame.draw.rect(screen, green, goal)
    pygame.draw.rect(screen, white, static_obstacle1_rect)
    pygame.draw.rect(screen, white, static_obstacle2_rect)
    pygame.draw.rect(screen, white, static_obstacle3_rect)
    pygame.draw.circle(screen, grey, (dynamic_obstacle1_pos[0], dynamic_obstacle1_pos[1]), dynamic_obstacle_radius)
    pygame.draw.circle(screen, grey, (dynamic_obstacle2_pos[0], dynamic_obstacle2_pos[1]), dynamic_obstacle_radius)
    pygame.draw.circle(screen, grey, (dynamic_obstacle3_pos[0], dynamic_obstacle3_pos[1]), dynamic_obstacle_radius)
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
sys.exit()
