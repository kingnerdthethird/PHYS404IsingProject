import numpy as np

from . import Analysis as analysis
from . import Backend as backend
from . import Experiment as experiment
from . import Matrix as matrix
from . import Metropolis as metropolis
from . import PlotData as plotdata

def PrintSpinMatrix(spin_matrix, rows, cols, m, run_number, i):
    print(str(rows) + "x" + str(cols) + " Matrix " + str(i) + ": " + str(m))
    for row in spin_matrix:
        for col in row:
            if col == 1:
                print("+1", end=' ')
            else:
                print("-1", end = ' ')
        print('\n')

def PrintPrettyMatrix(pretty_matrix, rows, cols, m, run_number, i):
    spins = open("Isaac/Data/SpinMatrices/TextPlots/" + str(run_number) +
                 "/PrettyMatrices.txt", "a")

    for row in pretty_matrix:
        for col in row:
            spins.write(str(col))
            spins.write(' ')
        spins.write('\n')
    spins.write('\n')
    spins.write(str(rows) + "x" + str(cols) + " Matrix " + str(i) + ": " + str(m) + '\n\n')