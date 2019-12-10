import numpy as np

from . import Backend as backend
from . import Experiment as experiment
from . import Matrix as matrix
from . import Metropolis as metropolis
from . import PlotData as plotdata
from . import PrintData as printdata

def Magnetization(spin_matrix):
    m = 0
    for row in spin_matrix:
        for col in row:
            m += col

    return m

def AverageMangnetization(magnetizations, N_MC):
    average_magnetization = 0

    for m in magnetizations:
        average_magnetization += m

    average_magnetization /= N_MC

    return average_magnetization

def AverageEnergy(energies, N_MC):
    average_energy = 0

    for E in energies:
        average_energy += E

    average_energy /= N_MC
    
    return average_energy

def Dispersion(magnetizations, average_magnetization, i):
    magnetizations_squared = 0

    for m in magnetizations:
        magnetizations_squared += (m**2)

    magnetizations_squared /= i
    
    dispersion = magnetizations_squared - (average_magnetization**2)

    return dispersion