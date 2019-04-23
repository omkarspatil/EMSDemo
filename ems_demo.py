"""
 Example program to show using an array to back a grid on-screen.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/

 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame

# Define some colors
BLACK = (0, 0, 0)
HOSPITAL = (99,100,5)
BASE = (12,110,5)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


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
WINDOW_SIZE = [400, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("EMS Simulation")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    for base in bases:
        grid[base[0]][base[1]] = 2

    for hospital in hospitals :
        grid[hospital[0]][hospital[1]] = 3

    for ambulance, target in zip(ambulances,ambulances_targets):
        grid[ambulance[0]][ambulance[1]] = 0
        grid[target[0]][target[1]] = 4;
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
        grid[ambulance[0]][ambulance[1]] = 1




















    screen.fill(BLACK)

    # Draw the grid
    for row in range(200):
        for column in range(200):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            elif grid[row][column] == 2:
                    color = BASE
            elif grid[row][column] == 3:
                color = HOSPITAL
            elif grid[row][column] == 4:
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