# -*- coding: utf-8 -*-
"""
Created on Sun May  5 18:30:28 2019

@author: atche
"""

import numpy as np
import matplotlib.pyplot as plt

def burn(grid, r):
    """
        Input
        -----
            grid: the grid of burning forest 
            
            r: the percentage for a cell to burning if an adjacent cell is 
                burning
        Output
        ------
            a new grid containing the updated grid after one iteration of 
            simulation
        Algorithm
        ---------
            for all the center cells that are 0, decide if the cell should be 
            burning now. For example, if r = 0.3 and there are 3 adjacent tiles
            burning, the probability for this tile to start burning is 
            1 - (1 - 0.3)^3. 
            
            after that, update the borders using periodic border condition
    """
    new_grid = np.copy(grid)
    not_burn = 1 - r #prob for not burning
    
    i_range = np.arange(17) + 1
    j_range = np.arange(17) + 1
    
    #update center cells
    for i in i_range:
        for j in j_range:
            if grid[i][j] == 0:
                adj = grid[i - 1][j] + grid[i + 1][j] + grid[i][j - 1] + \
                    grid[i][j + 1]
                
                #if a random number is greater than the probability of the tile 
                #not burning (under influence of all 4 adjacent cells)
                if np.random.random() > not_burn**adj:
                    new_grid[i][j] = 1
                
    #update border condition
    for i in i_range:
        new_grid[i][0] = new_grid[i][17]
        new_grid[i][18] = new_grid[i][1]
    for j in range(19):
        new_grid[0][j] = new_grid[17][j]
        new_grid[18][j] = new_grid[1][j]
    
    return new_grid

def get_burn_percent(grid):
    """
        Input
        -----
            A grid of the burning forest
        Output
        ------
            The percentage of the forest that is burning (disregarding border)
        Algorithm
        ---------
            since 1 is used to represent burning tree and 0 is a normal tree, 
            we can divide the sum of all center cells by the number of cells
            to return the percentage
    """
    total_burn = np.sum(grid[1:17][1:17])
    return total_burn / (17**2)

if __name__ == '__main__':
    grid = np.zeros((19, 19)) #0 means a not burning tree
    grid[9][9] = 1 #1 means a burning tree
    prob = (np.arange(9) + 1) * 0.1
    
    plt.figure()
    
    for r in prob:
        this_grid = np.copy(grid)
        burning_percentage = []
        counter = 0
        while True:
            counter += 1
            this_grid = burn(this_grid, r)
            burning_percentage.append(get_burn_percent(this_grid))
            #when over 98% of the forest is burning
            #run time tends to skyrocket when set to a higher value
            if burning_percentage[-1] > 0.98: 
                break
        burning_percentage = np.array(burning_percentage)
        plt.plot(burning_percentage)
    
    plt.show()