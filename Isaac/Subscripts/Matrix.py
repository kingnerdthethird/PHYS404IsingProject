import numpy as np

from . import Analysis as analysis
from . import Backend as backend
from . import Experiment as experiment
from . import PlotData as plotdata
from . import PrintData as printdata

def GenerateMatrix(r, c):
    spin_matrix = []

    for row in range(0, r):
        column = []
        for col in range(0, c):
            if np.random.random() >= 0.5:
                spin = +1
            else:
                spin = -1

            column.append(spin)

        spin_matrix.append(column)

    return spin_matrix

def GeneratePrettyMatrix(spin_matrix):
    pretty_matrix = []

    for row in spin_matrix:
        pretty_column = []
        for col in row:
            if col == 1:
                pretty_column.append('+')
            else:
                pretty_column.append('-')
        
        pretty_matrix.append(pretty_column)

    return pretty_matrix

def GenerateAverageMatrix(spin_matrix, previous_average, rows, cols, num):
    average_spins = []

    for i in range(0, rows):
        row = []
        for j in range(0, cols): 
            average = previous_average[i][j] * (num - 1)
            average += spin_matrix[i][j]
            average /= num
            row.append(average)
        average_spins.append(row)

    return average_spins