import numpy as np

from . import Backend as backend
from . import Experiment as experiment
from . import Matrix as matrix
from . import PlotData as plotdata
from . import PrintData as printdata

def Magnetization(spin_matrix):
    m = 0
    for row in spin_matrix:
        for col in row:
            m += col
            print(m)

    print('\n')
    return m

def AverageMangnetization(magnetizations, i):
    average_magnetization = 0

    for m in magnetizations:
        average_magnetization += m
        print(average_magnetization)

    average_magnetization /= i
    print(average_magnetization)

    print('\n')
    return average_magnetization

def Dispersion(magnetizations, average_magnetization, i):
    magnetizations_squared = 0

    for m in magnetizations:
        magnetizations_squared += (m**2)
        print(magnetizations_squared)

    magnetizations_squared /= i
    print(magnetizations_squared)
    
    dispersion = magnetizations_squared - (average_magnetization**2)
    print(dispersion)

    print('\n')
    return dispersion