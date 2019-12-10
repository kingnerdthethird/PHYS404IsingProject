import numpy as np

from . import Analysis as analysis # subscript for analyzing data
from . import Backend as backend # subscript for setting up folders
from . import Experiment as experiment # subscript for each part of the project
from . import Metropolis as metropolis # subscript for implementing Monte Carlo and Metropolis steps
from . import PlotData as plotdata # subscript for plotting data
from . import PrintData as printdata # subscript for printing data to text files

def GenerateMatrix(r, c):
    # this function generates a matrix of all up or all down and then flips a random amount of them

    spin_matrix = [] # initialize the spin matrix

    random_spin = 0 # this will become either +1 or -1

    if np.random.random() >= 0.5:
        random_spin = +1 # the matrix will be mostly +1 
    else:
        random_spin = -1 # the matrix will be mostly -1

    print("Random spin: " + str(random_spin)) # print the choice of random spin


    for row in range(0, r):
        # iterate r times
        column = [random_spin] * r # create a column of all -1 or +1
        print("Column: " + str(column)) # print the column
        spin_matrix.append(column) # add the column to the spin matrix

    N = r * c # the number of nodes in the spin matrix
    print("Number of nodes: " + str(N)) # print the number of nodes

    percentage = np.random.random() * 0.2 # choose a random percentage between 0 and 20%
    print("Percentage of nodes to flip: " + str(percentage)) # print the random percentage

    flips = int(N * percentage) + 1 # number of times to flip a random node, +1 is added so the minimum is 1
    print("Number of nodes to flip: " + str(flips)) # print the number of nodes to flip

    for i in range(0, flips):
        # iterate the chosen number of times

        rand_row, rand_col = np.random.randint(0, r), np.random.randint(0, c) # choose a random node
        print("Random node to be flipped (" + str(rand_row) + ", " + str(rand_col) + ")") # print the random node to flip

        spin_matrix[rand_row][rand_col] *= -1 # flip the random node

    return spin_matrix # return the generated spin matrix

def GeneratePrettyMatrix(spin_matrix):
    # this function generates a matrix of + and - to print out nicely

    pretty_matrix = [] # initialize the pretty matrix

    for row in spin_matrix:
        # iterate through the rows of the spin matrix
        pretty_column = [] # initialize the pretty column
        for col in row:
            # iterate through the elements of the row
            if col == 1:
                pretty_column.append('+') # add a + to the row
            else:
                pretty_column.append('-') # add a - to the row
        
        pretty_matrix.append(pretty_column) # add the pretty column to the matrix

    print("Pretty Matrix: " + str(pretty_matrix)) # print the pretty matrix
    return pretty_matrix # return the pretty matrix

def GenerateAverageMatrix(spin_matrix, previous_average, rows, cols, num):
    # this function generates an average matrix from the composition of a bunch of matrices

    average_spins = [] # initialize the average matrix

    for i in range(0, rows):
        #iterate through the number of rows

        row = [] # intialize the average row

        for j in range(0, cols): 
            #iterate through the number of columns

            average = previous_average[i][j] * (num - 1) # this reverts how you divide by the number of matrices before
            print("Old Total Spin: " + str(average)) # print the old total
            average += spin_matrix[i][j] # add the spin of the new matrix to the previous composition
            print("New Total Spin: " + str(average)) # print the new total spin
            average /= num # divide the total spin by the number of matrices
            print("New Average: " + str(average)) # print the new average spin
            row.append(average) # add the site to the average column

        average_spins.append(row) # add the average row to the average matrix

    print("Average Matrix: " + str(average_spins)) # print the average matrix

    return average_spins # return the average matrix