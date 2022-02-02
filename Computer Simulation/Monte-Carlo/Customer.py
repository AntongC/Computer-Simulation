"""
    Copyright
    ---------
        Antong Cheng
        April 29th 2019
"""

import numpy as np
import numpy.random as ra
import matplotlib.pyplot as plt

def sim_cumu(days = 1000, casual_prob = .002):
    """
        Input
        -----
            days to simulate and probability of a casual customer entering
        Output
        ------
            3 arrays containing core, casual, and total customer counts
        Algorithm
        ---------
            For each day in the simulation, call the sim_day function and 
            collect the result in an array
    """
    core = np.arange(days*20, dtype='float').reshape(days,20)
    core[:] = 0
    casual = np.arange(days*20, dtype='float').reshape(days,20)
    casual[:] = 0
    for i in range(days):
        core[i], casual[i] = sim_day(casual_prob)
    total = core + casual
    return core, casual, total
    
def sim_day(prob=.002):
    """
        Input
        -----
            probability of a casual customer entering the mall
        Output
        ------
            two arrays containing core and casual customers
        Algorithm
        ---------
            Simulates a given day in the mall with pre-defined parameters. 
    """
    n_casual = np.array([100.0,100.0,150.0,150.0,50.0,50.0,50.0,50.0,50.0,
                         50.0,50.0,50.0,150.0,150.0,150.0,150.0,150.0,150.0,
                         100.0,100.0])
    p_casual = 0.002
    mu = n_casual/10.0
    
    sigma = np.array(n_casual)
    sigma[sigma == 100.0] = 2.3
    sigma[sigma == 150.0] = 2.8
    sigma[sigma == 50.0] = 1.6
    
    p_core = [1 - (sigma[0]**2/mu[0])]
    n_core = [mu[0] / p_core[0]]
    
    core = np.zeros(20)
    core[0] = ra.binomial(n_core[0], p_core[0])
    casual = np.zeros(20)
    casual[0] = 0.01*n_casual[0]

    for i in np.arange(1, 20):
        p_core.append(1 - (sigma[i]**2 / mu[i]))
        n_core.append([mu[i] / p_core[i]])
        core[i] = ra.binomial(n_core[i], p_core[i])
        p_casual = prob * ((core[i - 1] + casual[i - 1])) + 0.01
        casual[i] = (n_casual[i] * p_casual)
    return core, casual
    
def display(core, casual, total):
    """
        Input
        -----
            Three arrays each containing core, casual, and total customers
        Output
        ------
            None
        Algorithm
        ---------
            Print out a chart like the one described in the article
    """
    print ('\n\nTime\tMean Core\tMean Casual\tMean Total')
    mean_core = []
    mean_casual= []
    mean_total= []
    
    for i in np.arange(20):
        mean_core.append(np.mean(core[:,i]))
        mean_casual.append(np.mean(casual[:,i]))
        mean_total.append(np.mean(total[:,i]))
        line = '{:>18}  {:>18}  {:>18}'.format(mean_core[i], mean_casual[i], \
                mean_total[i])
        print(i + 1, line)
        
    total_line = '{:>18}  {:>18}  {:>18}'.format(np.sum(mean_core), \
                  np.sum(mean_casual), np.sum(mean_total))
    print('Totals', total_line)
    plt.plot(mean_total)

core, casual, total = sim_cumu(1000, 0.002)
display(core,casual,total)


plt.title('Total Customers on Average') 
plt.ylabel('Total Customers on Average')
plt.xlabel('Time')
plt.show()