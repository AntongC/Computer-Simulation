# -*- coding: utf-8 -*-
"""
Created on Sat May  4 22:36:08 2019

@author: atche
"""

import numpy as np
import matplotlib.pyplot as plt

def diffuse_rand(grid, r = 0.1):
    """
        Input
        -----
            grid: the grid plot of the cell temperatures
            
            r: the diffusion rate of temperature
        Output
        ------
            the new grid after one iteration of heat diffusion
        Algorithm
        ---------
            same as diffuse_const, except that the diffusion rate has a random
            error that follows the distribution in rand()
    """
    new_grid = np.copy(grid)
    i_range = np.arange(10) + 1
    j_range = np.arange(30) + 1
    
    #update center cells
    for i in i_range:
        for j in j_range:
            new_grid[i][j] = (1 - 8 * r) * grid[i][j] + r * ( \
                    rand() * grid[i + 1][j] + rand() * grid[i + 1][j + 1] + \
                    rand() * grid[i + 1][j - 1] + rand() * grid[i][j + 1] + \
                    rand() * grid[i][j - 1] + rand() * grid[i - 1][j] + \
                    rand() * grid[i - 1][j + 1] + rand() * grid[i - 1][j - 1])
            
    #update border condition
    for i in i_range:
        new_grid[i][0] = new_grid[i][1]
        new_grid[i][31] = new_grid[i][30]
    for j in range(32):
        new_grid[0][j] = new_grid[1][j]
        new_grid[10][j] = new_grid[11][j]
        
    return (new_grid)

def diffuse_const(grid, r = 0.1):
    """
        Input
        -----
            grid: the grid plot of the cell temperatures
            
            r: the diffusion rate of temperature
        Output
        ------
            the new grid after one iteration of heat diffusion
        Algorithm
        ---------
            applies the Newton's Law of Heating and Cooling on each cell in 
            the center, and then update the border cells to be of equal
            temperature to its neighbor in the center
    """
    new_grid = np.copy(grid)
    i_range = np.arange(10) + 1
    j_range = np.arange(30) + 1
    
    #update center cells
    for i in i_range:
        for j in j_range:
            new_grid[i][j] = (1 - 8 * r) * grid[i][j] + r * ( \
                    grid[i + 1][j] + grid[i + 1][j + 1] + \
                    grid[i + 1][j - 1] + grid[i][j + 1] + \
                    grid[i][j - 1] + grid[i - 1][j] + \
                    grid[i - 1][j + 1] + grid[i - 1][j - 1])
            
    #update border condition
    for i in i_range:
        new_grid[i][0] = new_grid[i][1]
        new_grid[i][31] = new_grid[i][30]
    for j in range(32):
        new_grid[0][j] = new_grid[1][j]
        new_grid[10][j] = new_grid[11][j]
        
    return (new_grid)

def rand():
    """
        Input
        -----
            None.
        Output
        ------
            A random variable from a standard normal distribution with mean of
            1 and standard deviation of 0.5.
        Algorithm
        ---------
            Since in calculation we use the random variable as (1 + rand), we 
            can simply generate a random variable at mean = 1 
    """
    return np.random.normal(loc = 1, scale = 0.5)

if __name__ == '__main__':
    #initializing 
    grid = np.zeros((12, 32)) #10 x 30 grid with border conditions
    grid += 25 #set all cells to 25 celsius, then special cases
    grid[4:7][1] = 50
    grid[1][28] = 50
    grid[10][9:14] = 0
    
    mean_rand = np.zeros(20)
    mean_const = np.zeros(20)
    
    for i in range(100):
        for j in range(20):
            grid = diffuse_rand(grid)
            mean_rand[j] += np.average(grid[1:11][1:31])
    
    #reset grid
    grid = np.zeros((12, 32))
    grid += 25
    grid[4:7][1] = 50
    grid[1][28] = 50
    grid[10][9:14] = 0
    for i in range(100):
        for j in range(20):
            grid= diffuse_const(grid)
            mean_const[j] += np.average(grid[1:11][1:31])
    
    time = np.arange(20) + 1
    mean_rand = np.array(mean_rand) / 100
    mean_const = np.array(mean_const) / 100
    
    plt.figure()
    plt.plot(time, mean_rand)
    plt.plot(time, mean_const)
    plt.show()