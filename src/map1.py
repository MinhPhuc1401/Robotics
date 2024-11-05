import pygame
import sys

pygame.init()

width = 512
height = 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Map1')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)

goal = pygame.Rect(462, 0, 50, 50)
static_obstacle1_rect = (0, 180, 180, 50)
static_obstacle2_rect = (400, 332, 50, 180)

dynamic_obstacle1_pos = [220, 100]
dynamic_obstacle2_pos = [280, 380]
dynamic_obstacle_radius = 15
velocity1 = [0, 4]
velocity2 = [-6, 6]

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    dynamic_obstacle1_pos[0] += velocity1[0]
    dynamic_obstacle1_pos[1] += velocity1[1]
    
    if dynamic_obstacle1_pos[1] - dynamic_obstacle_radius <= 50 or dynamic_obstacle1_pos[1] + dynamic_obstacle_radius >= 400:
        velocity1[0] = -velocity1[0]
        velocity1[1] = -velocity1[1]
    
    dynamic_obstacle2_pos[0] += velocity2[0]
    dynamic_obstacle2_pos[1] += velocity2[1]
    
    if dynamic_obstacle2_pos[0] - dynamic_obstacle_radius <= 250 or dynamic_obstacle2_pos[0] + dynamic_obstacle_radius >= 450:
        velocity2[0] = -velocity2[0]
        velocity2[1] = -velocity2[1]
    
    screen.fill(black)
    pygame.draw.rect(screen, green, goal)
    pygame.draw.rect(screen, white, static_obstacle1_rect)
    pygame.draw.rect(screen, white, static_obstacle2_rect)
    pygame.draw.circle(screen, grey, (dynamic_obstacle1_pos[0], dynamic_obstacle1_pos[1]), dynamic_obstacle_radius)
    pygame.draw.circle(screen, grey, (dynamic_obstacle2_pos[0], dynamic_obstacle2_pos[1]), dynamic_obstacle_radius)
    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()
sys.exit()
