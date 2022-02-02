# -*- coding: utf-8 -*-
"""
Created on Sat May 11 18:04:48 2019

@author: atche
"""

import numpy as np
from random import randint
import matplotlib.pyplot as plt

"""
    The color theme looks absolutely hideous, but at least it works
    
    the average after 100 trails was 17.88 frogs at the end of 100 step trails
"""

NUM_TOADS = 20 #total number of toads
GRID_I = 40 #number of grid columns
GRID_J = 40 #number of grid rows

AMT_AWP = 1.0 # moisture value for water, such as an AWP 
AMT_AWP_ADJACENT = 0.4 # moisture value of neighboring cell to water 
AMT_AWP_OVER2 = 0.2 # moisture value of cell 2 cells away from water 
AMT_DRINK = 0.05 # maximum amount toad drinks in 1 time step 
AMT_EAT = 0.01 # maximum amount toad eats in 1 time step 
AMT_MIN_INIT = 0.88	# minimum initial toad energy and water values 
DESICCATE = 0.6 # level at which desiccation occurs  
FOOD_CELL = 0.05 # food value for initializing constant food grid 
INIT_RANGE = 0.12 #range of initial toad energy and water values
MAY_HOP = 0.5 # probability of hopping if not thirsty or hungry 
STARVE = 0.6 # level at which starvation occurs 
WATER_HOPPING = 0.002 # maximum water used by toad in a hop
ENERGY_HOPPING = 0.002 # maximum energy used by toad in a hop 
WOULD_LIKE_DRINK = 0.9 # water level at which toad would like to drink 
WOULD_LIKE_EAT = 0.9 # food level at which toad would like to eat

def consume(grid, toads):
    """
        Input
        -----
            grid: an array containing information about the food and water
                resources on the desert tiles
            toads: an array containing information about the life vitals and
                the positions of the toads
        Output
        ------
            None
        Algorithm
        ---------
            Simulates the consuming action of the toads, adding values to the
            toads' vitals and deducting corresponding resouces from the tiles
    """
    for i in toads:
        if i[4] == True:
            if(i[0] < WOULD_LIKE_DRINK):
                random = np.random.random()
                i[0] += random * WATER_HOPPING
                grid[int(i[2]), int(i[3]), 0] -= random * WATER_HOPPING
            if(i[1] < WOULD_LIKE_EAT):
                random = np.random.random()
                i[1] += random * ENERGY_HOPPING
                grid[int(i[2]), int(i[3]), 1] -= random * ENERGY_HOPPING

def move(grid, toads):
    """
        Input
        -----
            grid: an array containing information about the food and water
                resources on the desert tiles
            toads: an array containing information about the life vitals and
                the positions of the toads
        Output
        ------
            None
        Algorithm
        ---------
            Simulates the moving process of the toads, deducting vital values
            from the toads and moving their coordinate position
    """
    for i in toads:
        if i[4] == True:
            if np.random.random() < MAY_HOP:
                i[0] -= WATER_HOPPING
                i[1] -= ENERGY_HOPPING
                random = np.random.random()
                if random < 0.25:
                    if i[2] < 39:
                        i[2] += 1
                if random >= 0.25 and random < 0.5:
                    if i[2] > 0:
                        i[2] -= 1
                if random >= 0.5 and random < 0.75:
                    if i[3] < 39:
                        i[3] += 1
                if random >= 0.75:
                    if i[3] > 0:
                        i[3] -= 1

def check_live(toads):
    """
        Input
        -----
            toads: an array containing information about the life vitals and
                the positions of the toads
        Output
        ------
            None
        Algorithm
        ---------
            Check if the toads' vital signs are below the threshold. If so, 
            declare the toad as deceased. 
    """
    for i in toads:
        if i[0] < DESICCATE or i[2] < STARVE:
            i[4] = False

plt.ion()
fig = plt.figure(figsize = (10, 10))
ax = fig.add_axes((0, 0, 1, 1), frameon = False)

display = np.zeros((GRID_I, GRID_J, 3), 'f')
test = ax.imshow(display, interpolation = 'none', extent = [0, 39, 0, 39], \
                 aspect = 'auto', zorder = 0)
ax.axis('off')

toads_living = []

grid = np.zeros((GRID_I, GRID_J, 2)) #:, :, 0 is water, :, :, 1 is food
grid[:, :, 1] += FOOD_CELL

awp = np.array([[12, 33], [9, 12], [22, 34], [30, 2], [21, 34], [39, 1]])
    
for c in range(len(awp)):
    grid[awp[c, 0] - 2 : awp[c, 0] + 3, awp[c, 1] - 2 : awp[c, 1] + 3, 0] \
        = AMT_AWP_OVER2
for c in range(len(awp)):
    grid[awp[c, 0] - 1 : awp[c, 0] + 2, awp[c, 1] - 1 : awp[c, 1] + 2, 0] \
        = AMT_AWP_ADJACENT
for c in range(len(awp)):
    grid[awp[c, 0], awp[c, 1], 0] = AMT_AWP

toads = np.zeros((NUM_TOADS, 5)) 
#0 is water, 1 is food, 2 is y coord, 3 is x, 4 is living status
    
for c in range(NUM_TOADS):
    toads[:, 0:2] = AMT_MIN_INIT + np.random.random() * INIT_RANGE
for c in range(NUM_TOADS):
    toads[c, 2] = randint(0, 39)

toads[:, 3] = 39
toads[:, 4] = True
    
for b in range(1000):
    consume(grid, toads)
    move(grid, toads)
    check_live(toads)
    display = np.zeros((GRID_I, GRID_J, 3), 'f')
    for i in range(GRID_I):
        for j in range(GRID_J):
            display[i, j, 0] = grid[i, j, 0]
            if grid[i, j, 0] < 1:
                display[i, j, :] += grid[i, j, 0]
    for i in range(NUM_TOADS):
        display[int(toads[i, 2]), int(toads[i, 3]), :] = \
        np.array([0, 0, 1])
    test.set_data(display)
    plt.draw()
    
    toads_living.append(np.sum(toads[:, 4]))

toads_living = np.array(toads_living)

plt.figure()
plt.scatter(toads_living[:-1], toads_living[1:])
plt.xlabel('number of living toads in the current step')
plt.ylabel('number of living toads one step later')
plt.show()