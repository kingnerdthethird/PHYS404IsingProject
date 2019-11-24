import numpy as np

from . import Analysis as analysis
from . import Backend as backend
from . import Experiment as experiment
from . import Matrix as matrix
from . import PlotData as plotdata

def PrintMatrix(matrices, run_number, i, r, c):
    spins = open("Isaac/SpinMatrices/TextPlots/" + str(run_number) + "/Spin Matrix " + str(run_number) + " for " + str(i) + " Matrices.txt", "w+")
    for input_matrix in matrices:
        for row in input_matrix[0]:
            for col in row:
                spins.write(col)
                spins.write(' ')
            spins.write('\n')
        spins.write('\n')
        spins.write(str(r) + 'x' + str(c) + ': ' + str(matrix[1]) + '\n\n')