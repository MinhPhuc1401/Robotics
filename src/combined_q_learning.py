import pygame
import sys
import numpy as np
import random
import math
import os

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
velocity1 = [0, 1.5]
velocity2 = [-1.3, 1.3]

agent_pos = [50, 500]
agent_prev_pros = agent_pos.copy()
agent_size = 8
velocity = 1.6

alpha = 0.9 # Learning Rate
gamma = 0.9 # Discount Factor
epsilon = 0.5 # Exploration Rate
epsilon_decay = 0.95
n_actions = 8

if os.path.exists('q_table2.npy'):
    q_table = np.load('q_table2.npy')
else:
    q_table = np.zeros((width // agent_size, height // agent_size, n_actions))
    for i in range(width // agent_size):
        for j in range(height // agent_size):
            dt = abs(i - goal[0]) + abs(j - goal[1]) + (np.sqrt(2) - 2) * min(abs(i - goal[0]), abs(j - goal[1]))
            if dt > 0:
                q_table[i][j] = 1/dt
            else:
                q_table[i][j] = 0

def choose_action(state):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, n_actions - 1) # Exploration
    else:
        return np.argmax(q_table[state[0], state[1]]) # Exploitation
    


clock = pygame.time.Clock()
running = True
episodes = 50
times = 0
path = []

for episode in range(episodes):
    agent_pos = [50, 500]
    dynamic_obstacle1_pos = [220, 100]
    dynamic_obstacle2_pos = [280, 380]
    path.clear()
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
        pygame.draw.circle(screen, red, (agent_pos[0], agent_pos[1]), agent_size)
        
        if path:
            for i in range(len(path) - 1):
                pygame.draw.line(screen, red, path[i], path[i+1], 5)
        
        state = (agent_pos[0] // agent_size, agent_pos[1] // agent_size)
        action = choose_action(state)
        
        if action == 0 and agent_pos[1] > agent_size:  # up
            agent_pos[1] -= velocity
        elif agent_pos[1] == agent_size:
            agent_pos[1] += 30 * velocity
        elif action == 1 and agent_pos[1] < height - agent_size:  # down
            agent_pos[1] += velocity
        elif agent_pos[1] == height - agent_size:
            agent_pos[1] -= 30 * velocity
        elif action == 2 and agent_pos[0] > agent_size:  # left
            agent_pos[0] -= velocity
        elif agent_pos[0] == agent_size:
            agent_pos[0] += 30 * velocity
        elif action == 3 and agent_pos[0] < width - agent_size:  # right
            agent_pos[0] += velocity
        elif agent_pos[0] == width - agent_size:
            agent_pos[0] -= 30 * velocity
        elif action == 4 and agent_pos[0] > agent_size and agent_pos[1] > agent_size:  # up-left
            agent_pos[0] -= velocity
            agent_pos[1] -= velocity
        elif action == 5 and agent_pos[0] < width - agent_size and agent_pos[1] > agent_size:  # up-right
            agent_pos[0] += velocity
            agent_pos[1] -= velocity
        elif action == 6 and agent_pos[0] > agent_size and agent_pos[1] < height - agent_size:  # down-left
            agent_pos[0] -= velocity
            agent_pos[1] += velocity
        elif action == 7 and agent_pos[0] < width - agent_size and agent_pos[1] < height - agent_size:  # down-right
            agent_pos[0] += velocity
            agent_pos[1] += velocity
        
        path.append((agent_pos[0], agent_pos[1]))
        
        reward = reward_function(agent_pos)
        next_state = (agent_pos[0] // agent_size, agent_pos[1] // agent_size)
        
        # Update q-table
        update_q_table(state, action, reward, next_state)

        if reward == 10:
            times += 1
        
        if reward == float('-inf') or reward == 10:
            print(f"Episode {episode+1}/{episodes} is completed")
            # Update epsilon
            epsilon = epsilon * epsilon_decay
            break
        
        pygame.display.flip()
        clock.tick(30)
np.save('q_table2.npy', q_table)

pygame.quit()
sys.exit()
