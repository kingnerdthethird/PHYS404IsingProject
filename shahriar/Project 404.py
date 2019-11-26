import numpy.linalg as nlg  ;  import matplotlib.pyplot as plt
import numpy as np ; import os ; import copy
pi = np.pi ; from scipy import constants as sc

 
# To average over this many matrices
number_of_Ensemble = 100
# "Size" contains the dimention of the matices
size = [3,10,64]
# Function to create the matrix of spin


def Matrix (m):
    x = np.zeros((m , m))
    for i in range(0, m):
        for j in range(0, m):
            num = np.random.random()
            if num >= 0.5:
                x[i][j] = 1
            else:
                x[i][j] = -1
    return(x)


L = len(size)
Magnitization = np.ones((L ,number_of_Ensemble))  # this two dimentional matrix is to save the magnitization of all marices
summ = 0

# to genrate the matrix based on the dimention
for i in range(0, L):
    counter = 0
    while counter < number_of_Ensemble: # this loop is to create multipole matrices of the same size for the purpose of averaging     
        X = Matrix(size[i])
        row, col= np.shape(X)
        # this loop is to sum all elements of the matrix
        for p in range(0, row):
            for k in range(0, col):
                summ = summ + X[p][k] 
        
        Magnitization[i][counter] = summ
        summ = 0
        counter += 1 

# To save the average value of every size matrices
average = [None]*L

# To save the dispersion value of every size matrices
dispersion = [None]*L

Mag = copy.copy(Magnitization)

# to slice the Magnitization matrix to find averages and dispersions
for i in range(0, L):
    Y = Mag[i:i+1,:]
    average[i] = np.average(Y)
    
    # this part is calculating the disperion
    for j in range(0, len(Y)):
        Y[j] = Y[j]**2 - average[i]**2
    dispersion[i] = np.average(Y) 

# to print the final values.
for i in range(0, L):
    print('For {}x{} Matrix:\n Ave={},   Dis={:0.3f}'. format(size[i], size[i], average[i], np.sqrt(dispersion[i])))
    print('Magnitization of each {} seperate, {}x{} matrices :\n{}\n\n'. format( number_of_Ensemble , size[i], size[i], Magnitization[i,:]))
    
###########################################################################
# This part of the code is to just graph the average as we create more ensemble
    
row, col = np.shape(Magnitization) 
Running_Average = np.ones((row, col)) # this matrix is to save all the running average

# This nested for loop calcultes the running average with respect to the number of matrix and averages
for j in range(0, row):
    for i in range(1, col):
        # Just a dummy variable to save data temporairly so we can find the averages
        dummy = Magnitization[ j,0:i+1 ]
        # Running_Average to save all the averages
        Running_Average[j][i] = np.average(dummy)

# This is the X-axis of our plots
Number_of_averages = np.arange(0, number_of_Ensemble)

plt.figure('Running Average')
for i in range(0, L):
    legend = 'for' + str(size[i]) + 'x' + str(size[i]) + 'Matrix'
    plt.subplot(L ,1, i+1); plt.plot(Number_of_averages, Running_Average[i,:] , label=legend ,marker = '.')
    plt.axhline(y=0, color='k')
    plt.legend(loc = 'upper right', fontsize= 15)
    plt.ylabel('Running Average', fontsize=13)
    plt.grid()
plt.xlabel('Number of Averages', fontsize=13)









          