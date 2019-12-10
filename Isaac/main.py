import numpy as np # used for numerical tools
import matplotlib as mpl # used for image generation and GIF creation
import matplotlib.pyplot as plt # used for plotting data
import os # used to determine file locations as well as create directories

import Subscripts as ising # this imports all the subscripts for the project

run_number = ising.RunNumber() # the run number is the number of times the code as been run
                               # this is so that I can keep old data around while creating new data
print("Run Number: " + str(run_number)) # print the run number

main = str(os.path.dirname(os.path.abspath(__file__))) # this sets the working directory
print("Working Directory: " + main) # print the working directories

# all the directories are the places that we will need to store data
# since I don't upload data to GitHub because of data size, the folders need to be created on each computer
directories = [
               "/Data", # main folder for data
               "/Data/SpinMatrices", # folder for configurations (not data)
               "/Data/SpinMatrices/Plots", # folder for the plots of the configurations
               "/Data/SpinMatrices/Plots/" + str(run_number), # folder for this specific run
               "/Data/SpinMatrices/TextPlots", # folder for the text plots, which look like
                                               # + - + 
                                               # - + -
                                               # + - +
               "/Data/SpinMatrices/TextPlots/" + str(run_number), # folder for this specific run 
               "/Data/Results", # folder for text files of data
               "/Data/Magnetizations", # folder for text files of magnetization lists
               "/Data/Figures", # folder for the plots
               "/Data/Figures/" + str(run_number) # folder for this specific list
               ]

print("Directories needed: " + str(directories)) # print the directories that will be made

# the following function creates all the directories needed
# the main is concatenated with each directory separately
ising.CreateDirectories(main, directories)

# PART 1
print("Part 1")
# parameters is the various matrix sizes to use
# the format is [rows, cols]
# N is the number of matrices to create to be averaged
# parameters, N = [[4, 4], [8, 8], [16, 16], [32, 32], [64, 64]], 100 # normal parameters
parameters, N = [[10, 10]], 100 # testing parameters
print("Parameters: " + str(parameters)) # print out the parameters for Part 1
print("Number of matrices for each parameter: " + str(N)) # print out the number of matrices per parameter

ising.StepOne(parameters, N, run_number) # this runs the code for Part 1

# PART 2
print("Part 1")
# parameters is the same as above, with [rows, cols]
# X is the number of times each site should be hit on average
# K is given by J/kT
# K_i is the initial K value
# K_f is the final K value
# dK the step size for the K values
# J is the coupling constant and is almost always 1
# parameters, X, K_i, K_f, dK, J = [[4, 4], [8, 8], [16, 16], [32, 32], [64, 64], [32, 32]], 10, 0.01, 1, 0.01, 1 # normal parameters
parameters, X, K_i, K_f, dK, J = [[10, 10]], 10, 0.05, 0.1, 0.01, 1 # testing parameters
print("Parameters: " + str(parameters)) # print the parameters for Part 2
print("Number of hits per site: " + str(X)) # print the amount of times each site should be reached
print("Initital K value: " + str(K_i)) # print the intial K value
print("FInal K value: " + str(K_f)) # print the final K value
print("K value step: " + str(dK)) # print the step value for K
print("Coupling Constant: " + str(J)) # print the coupling constant

# the following tree sets the number of decimals to round to
# otherwise the files get messed up when being read
if K_i >= 0.1:
    decimals = 1
elif K_i >= 0.01:
    decimals = 2
elif K_i >= 0.001:
    decimals = 3
elif K_i >= 0.0001:
    decimals = 4
elif K_i >= 0.00001:
    decimals = 5

print("Decimals: " + str(decimals)) # print the number of decimals to round to

N_K = int((K_f - K_i + dK) / dK) # the number of K values to be checked
print("Number of K values: " + str(N_K)) # print the number of K values to be checked
K_range = np.linspace(K_i, K_f, N_K) # sets the range of K values
                                     # linspace is the reason we need the above tree
print("Range of K values: " + str(K_range)) # print the range of K values
ising.StepTwo(parameters, X, K_range, run_number, J, decimals) # this runs the code for Part 2

# FIXED K VALUES
print("Fixed K Values")
# this is not part of the assigned project
# Tianning and I animated plots for fixed K over "time"

# the format for the parameters changes here:
# [rows, cols, X, Y, K, J] where
# rows is the number of rows for each matrix
# cols is the number of columns for each matrix
# X is the number of "time" steps for each matrix
# Y is the number of spins to flip/not flip per matrix
# K is as above
# J is as above

# parameters = [ [200, 200, 1000, 1, 0.5, 1],
#               [200, 200, 1000, 10, 0.5, 1],
#               [200, 200, 1000, 100, 0.5, 1],
#               [200, 200, 1000, 1000, 0.5, 1],
#               [200, 200, 1000, 10000, 0.5, 1],
#               [200, 200, 1000, 100000, 0.5, 1] ] # normal parameters
parameters = [[10, 10, 100, 100, 0.5, 1], [10, 10, 100, 10, 0.5, 1]] # testing parameters
print("Parameters: " + str(parameters)) # print the parameters for fixed K values

ising.FixedK(parameters, run_number) # this runs the code for fixed K value