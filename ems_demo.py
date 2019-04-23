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
import queue
import os

class Ambulance:
    def __init__(self, is_assigned, location, call, target, priority, hos, bas):
        self.is_assigned = is_assigned
        self.location = location
        self.call = call
        self.hospital = hos
        self.base = bas
        self.priority = priority
        self.target = target
        self.status = 0


def manhattan(p1, p2):
    return abs(p1[0]- p2[0]) + abs(p1[1]- p2[1])

def dispatch(call, priority):
    #Find the nearest ambulance, preempt if needed
    closest_ambulance = None
    for ambulance in ambulances:
        if ambulance.is_assigned == False or (ambulance.status == 0 and ambulance.priority > priority):
            if closest_ambulance is None or manhattan(call, ambulance.location) < manhattan(call,
                                                                                            closest_ambulance.location):
                closest_ambulance = ambulance
    if closest_ambulance is not None:
        if closest_ambulance.is_assigned == True:
            #Prempted
            queueCalls.put((priority, call))
        else:
            bases_count[closest_ambulance.base] -= 1

        closest_ambulance.is_assigned = True
        closest_ambulance.call = call
        closest_ambulance.target = call
        closest_ambulance.priority = priority
        #Find the closest hospital to the call

        closest_hospital = None
        for hospital in hospitals:
            if closest_hospital is None or manhattan(hospital, call) < manhattan(closest_hospital,call):
                closest_hospital = hospital

        closest_ambulance.hospital = closest_hospital
    else:
        queueCalls.put((priority,call))

# Define some colors
BLACK = (0, 0, 0)
HOSPITAL_COL = (0,0,200)
BASE_COL = (12,110,5)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED_1 = (255, 0, 0)
RED_2 = (255, 99, 71)
RED_3 = (255, 255, 0)
RED_4 = (192, 192, 192)

REDS = [RED_1, RED_2, RED_3, RED_4]

AMBULANCE = 1
BASE = 2
HOSPITAL = 3
CALL = 4

#bases = [[4,4], [11,4], [5,12], [11,12]]
#bases_count = [0,0,0,0]

bases = [[4,4], [11,4]]
bases_count = [0,0]

hospitals = [[2,2], [8,2], [4,8], [2, 14], [7,1], [12,13], [13,13]]

ambulances = []

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 60
HEIGHT = 60

# This sets the margin between each cell
MARGIN = 1

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
queueCalls = queue.PriorityQueue()




for row in range(15):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(15):
        grid[row].append(0)  # Append a cell

# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [930, 930]
screen = pygame.display.set_mode(WINDOW_SIZE)
player = pygame.image.load(os.path.join("ambulance.png"))
player2 = pygame.image.load(os.path.join("ambulance_active.png"))
player.convert()
player2.convert()
# Set title of screen
pygame.display.set_caption("EMS Simulation")


font = pygame.font.SysFont("comicsansms", 30)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

priority_rates = np.array([0.1, 0.09, 0.111, 0.5])
def call_generator():
    sum_rates = np.sum(priority_rates)
    ratios = []
    # p = 0
    for x in priority_rates:
        p = x/sum_rates
        ratios.append(p)
    while not done:
        priority = np.random.choice(np.arange(0, 4), p=ratios)
        print(" p : "+ str(priority))
        rate = priority_rates[priority]
        #print(1/rate)
        x, y = random.randint(0, 14), random.randint(0, 14)
        print(x, y)
        if grid[x][y] == 0:
            grid[x][y] = CALL + priority
            dispatch([x,y], priority)
        time.sleep(1 / rate)
        print('done')
    pass

#initialize ambulances in bases
base_id = 0
for base in bases:
    #x, y = random.randint(0, 29), random.randint(0, 29)
    for i in range(1):
        # print('pushing ambulances')
        location = [base[0], base[1]]
        ambulance = Ambulance(False, location, base, base, -1, base, base_id)
        ambulances.append(ambulance)
        bases_count[base_id] +=1
    base_id += 1

thread_call_gen = threading.Thread(target=call_generator)
thread_call_gen.start()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    for ambulance in ambulances:
        print("Active" if ambulance.status == 1 else "Inactive")

    for ambulance in ambulances:
        # grid[ambulance.location[0]][ambulance.location[1]] = 0
        if ambulance.location[0] != ambulance.target[0]:
            if ambulance.target[0] > ambulance.location[0]:
                ambulance.location[0] = ambulance.location[0] + 1
            else:
                ambulance.location[0] = ambulance.location[0] - 1
        elif ambulance.location[1] != ambulance.target[1]:
            if ambulance.target[1] > ambulance.location[1]:
                ambulance.location[1] = ambulance.location[1] + 1
            else:
                ambulance.location[1] = ambulance.location[1] - 1
        else:
            #Check where to move based on where you are
            if ambulance.is_assigned:
                if manhattan(ambulance.location, ambulance.call) == 0:
                    ambulance.target = ambulance.hospital
                    # print("Setting " + str(ambulance.base))
                    ambulance.status = 1
                    grid[ambulance.location[0]][ambulance.location[1]] = 0
                elif manhattan(ambulance.location, ambulance.hospital) == 0:
                    ambulance.status = 0
                    if queueCalls.empty():
                        bases_count[ambulance.base] +=1
                        ambulance.is_assigned = False
                        ambulance.target = bases[ambulance.base]
                    else:
                        priority, nextCall = queueCalls.get()
                        ambulance.target = ambulance.call = nextCall

        #grid[ambulance.location[0]][ambulance.location[1]] = AMBULANCE


    for base in bases:
        grid[base[0]][base[1]] = BASE

    for hospital in hospitals :
        grid[hospital[0]][hospital[1]] = HOSPITAL

    # for priority, waiting_call in queueCalls.queue:
    #     grid[waiting_call[0]][waiting_call[1]] = CALL + priority

    screen.fill(BLACK)

    # Draw the grid
    for row in range(15):
        for column in range(15):
                color = WHITE
                if grid[row][column] == BASE:
                        color = BASE_COL
                elif grid[row][column] == HOSPITAL:
                    color = HOSPITAL_COL
                elif grid[row][column] >= CALL:
                        # print("prior : " + str(grid[row][column] - CALL))
                        color = REDS[grid[row][column] - CALL]
                pygame.draw.rect(screen,
                                 color,
                                 [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])

    for base, count in zip(bases, bases_count):
        text = font.render(str(count), True, (255, 255, 255))
        screen.blit(text, ((MARGIN + WIDTH) * base[1] + MARGIN,(MARGIN + HEIGHT) * base[0] + MARGIN))

    for ambulance in ambulances:
        x,y = ambulance.location
        if ambulance.status == 0:
            screen.blit(player, ((MARGIN + WIDTH) * y + MARGIN,
                         (MARGIN + HEIGHT) * x + MARGIN))
        else:
            screen.blit(player2, ((MARGIN + WIDTH) * y + MARGIN,
                                 (MARGIN + HEIGHT) * x + MARGIN))

    # Limit to 60 frames per second
    clock.tick(1)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()