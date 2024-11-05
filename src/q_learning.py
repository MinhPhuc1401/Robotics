import pygame
import sys
import numpy as np
import random
import math
import os

pygame.init()

width = 1600
height = 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Q learning')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)

goal = pygame.Rect(800, 0, 100, 100)
static_obstacle1_rect = (150, 0, 200, 150)
static_obstacle2_rect = (600, 700, 400, 200)
static_obstacle3_rect = (1100, 0, 50, 500)

dynamic_obstacle1_pos = [300, 250]
dynamic_obstacle2_pos = [1400, 600]
dynamic_obstacle3_pos = [600, 600]
dynamic_obstacle_radius = 30
velocity1 = [-10, 0]
velocity2 = [0, -12]
velocity3 = [18, -10]

agent_pos = [50, 800]
agent_prev_pros = agent_pos.copy()
agent_size = 10
velocity = 15

alpha = 0.9 # Learning Rate
gamma = 0.9 # Discount Factor
epsilon = 0.5 # Exploration Rate
epsilon_decay = 0.95
n_actions = 8

if os.path.exists('q_table.npy'):
    q_table = np.load('q_table.npy')
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
        
def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

def reward_function(agent_pos, agent_prev_pos):
    if goal.collidepoint(agent_pos[0], agent_pos[1]):
        return 10
    for static_obstacle in [static_obstacle1_rect, static_obstacle2_rect, static_obstacle3_rect]:
        if pygame.Rect(static_obstacle).collidepoint(agent_pos[0], agent_pos[1]):
            return float('-inf')
    for dynamic_obstacle in [dynamic_obstacle1_pos, dynamic_obstacle2_pos, dynamic_obstacle3_pos]:
        if math.hypot(agent_pos[0] - dynamic_obstacle[0], agent_pos[1] - dynamic_obstacle[1]) >= dynamic_obstacle_radius + agent_size:
            return float('inf')
    d = distance(agent_prev_pos, (goal[0], goal[1]))
    d_next = distance(agent_pos, (goal[0], goal[1]))
    if d != d_next:
        rd = (d-d_next)/(abs(d-d_next))
    else:
        rd = 0
    delta_x = abs(agent_pos[0] - agent_prev_pos[0])
    delta_y = abs(agent_pos[1] - agent_prev_pos[1])
    if delta_x == velocity*math.sqrt(2) and delta_y == velocity*math.sqrt(2):
        rs = 1/math.sqrt(2)
    elif delta_x == velocity or delta_y == velocity:
        rs = 1
    else:
        rs = 0
    r = rs * (1 + rd)
    return r - 3

def update_q_table(state, action, reward, next_state):
    best_next_action = np.argmax(q_table[next_state[0], next_state[1]])
    td_target = reward + gamma * float(q_table[next_state[0], next_state[1], best_next_action])
    td_delta = td_target - q_table[state[0], state[1], action]
    q_table[state[0], state[1], action] += alpha * td_delta

clock = pygame.time.Clock()
episodes = 50
times = 0
path = []

for episode in range(episodes):
    agent_pos = [50, 800]
    dynamic_obstacle1_pos = [300, 250]
    dynamic_obstacle2_pos = [1200, 600]
    dynamic_obstacle3_pos = [400, 700]
    path.clear()

    while True: 
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
        pygame.draw.circle(screen, red, (agent_pos[0], agent_pos[1]), agent_size)
        
        if path:
            for i in range(len(path) - 1):
                pygame.draw.line(screen, red, path[i], path[i+1], 5)
        
        state = (agent_pos[0] // agent_size, agent_pos[1] // agent_size)
        action = choose_action(state)
        agent_prev_pos = agent_pos.copy()
        
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
        
        reward = reward_function(agent_pos, agent_prev_pos)
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
np.save('q_table.npy', q_table)
print(f"Success: {times}/{episodes}")

pygame.quit()
sys.exit()
