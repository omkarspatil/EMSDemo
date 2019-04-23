"""
 Example program to show using an array to back a grid on-screen.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
import threading
import numpy as np
import random
import time

# Define some colors
BLACK = (0, 0, 0)
HOSPITAL_COL = (99,100,5)
BASE_COL = (12,110,5)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

AMBULANCE = 1
BASE = 2
HOSPITAL = 3
CALL = 4

bases = [[1,1], [3,4], [5,3]]
hospitals = [[3,1], [6,4], [7,7]]

ambulances = [[0,0], [4,4]]
ambulances_targets = [[5,5], [0,0]]

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 1

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(200):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(200):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [1000, 1000]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("EMS Simulation")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

priority_rates = np.array([0.05, 0.09, 0.11, 0.04])
def call_generator():
    sum_rates = np.sum(priority_rates)
    ratios = []
    # p = 0
    for x in priority_rates:
        p = x/sum_rates
        ratios.append(p)
    while not done:
        rand = np.random.choice(np.arange(0, 4), p=ratios)
        rate = priority_rates[rand]
        print(1/rate)
        x, y = random.randint(0, 9), random.randint(0, 9)
        print(x, y)
        if grid[x][y] not in [HOSPITAL, BASE]:
            grid[x][y] = CALL
        time.sleep(1 / rate)
        print('done')
    pass

thread_call_gen = threading.Thread(target=call_generator)
thread_call_gen.start()
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    for base in bases:
        grid[base[0]][base[1]] = BASE

    for hospital in hospitals :
        grid[hospital[0]][hospital[1]] = HOSPITAL

    for ambulance, target in zip(ambulances,ambulances_targets):
        grid[ambulance[0]][ambulance[1]] = 0
        grid[target[0]][target[1]] = CALL;
        if ambulance[0] != target[0]:
            if target[0] > ambulance[0]:
                ambulance[0] = ambulance[0] + 1
            else:
                ambulance[0] = ambulance[0] - 1
        elif ambulance[1] != target[1]:
            if target[1] > ambulance[1]:
                ambulance[1] = ambulance[1] + 1
            else:
                ambulance[1] = ambulance[1] - 1
        grid[ambulance[0]][ambulance[1]] = AMBULANCE




















    screen.fill(BLACK)

    # Draw the grid
    for row in range(200):
        for column in range(200):
            color = WHITE
            if grid[row][column] == AMBULANCE:
                color = GREEN
            elif grid[row][column] == BASE:
                    color = BASE_COL
            elif grid[row][column] == HOSPITAL:
                color = HOSPITAL_COL
            elif grid[row][column] == CALL:
                    color = RED
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

    # Limit to 60 frames per second
    clock.tick(10)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()