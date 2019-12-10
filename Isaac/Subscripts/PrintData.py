import numpy as np

from . import Analysis as analysis # subscript for analyzing data
from . import Backend as backend # subscript for setting up folders
from . import Experiment as experiment # subscript for each part of the project
from . import Metropolis as metropolis # subscript for implementing Monte Carlo and Metropolis steps
from . import Matrix as matrix # subscript for managing matrices
from . import PlotData as plotdata # subscript for plotting data

def PrintSpinMatrix(spin_matrix, rows, cols, m, run_number, i):
    # this function prints the spin matrix, it's pretty simple
    print(str(rows) + "x" + str(cols) + " Matrix " + str(i) + ": " + str(m))
    for row in spin_matrix:
        for col in row:
            if col == 1:
                print("+1", end=' ')
            else:
                print("-1", end = ' ')
        print('\n')

def PrintPrettyMatrix(pretty_matrix, rows, cols, m, run_number, i):
    # this function prints to a text file the pretty matrix, it's pretty simple
    spins = open("Isaac/Data/SpinMatrices/TextPlots/" + str(run_number) +
                 "/PrettyMatrices.txt", "a")

    for row in pretty_matrix:
        for col in row:
            spins.write(str(col))
            spins.write(' ')
        spins.write('\n')
    spins.write('\n')
    spins.write(str(rows) + "x" + str(cols) + " Matrix " + str(i) + ": " + str(m) + '\n\n')