import numpy as np

from . import Analysis as analysis
from . import Backend as backend
from . import Experiment as experiment
from . import PlotData as plotdata
from . import PrintData as printdata

def GenerateMatrix(r, c):
    matrix = []
    pretty_matrix = []
    m = 0
    for row in range(0, r):
        column = []
        pretty_column = []
        for col in range(0, c):
            if np.random.random() >= 0.5:
                spin = +1
                pretty_spin = "+"
            else:
                spin = -1
                pretty_spin = "-"

            m += spin
            column.append(spin)
            pretty_column.append(pretty_spin)

        matrix.append(column)
        pretty_matrix.append(pretty_column)

    return (matrix, pretty_matrix, m)