import numpy as np

from . import Analysis as analysis
from . import Backend as backend
from . import Experiment as experiment
from . import Matrix as matrix
from . import PlotData as plotdata
from . import PrintData as printdata

def NearestNeighborSpins(spin_matrix, rows, cols, rand_row, rand_col):
    a = spin_matrix[rand_row][rand_col]
    b = spin_matrix[np.mod(rand_row + 1, rows)][np.mod(rand_col, cols)]
    c = spin_matrix[np.mod(rand_row, rows)][np.mod(rand_col + 1, cols)]
    d = spin_matrix[np.mod(rand_row - 1, rows)][np.mod(rand_col, cols)]
    e = spin_matrix[np.mod(rand_row, rows)][np.mod(rand_col - 1, cols)]

    neighbor_spins = a * (b + c + d + e)

    return neighbor_spins

def EnergyDifference(spin_matrix, rows, cols, rand_row, rand_col, J):
    ds = NearestNeighborSpins(spin_matrix, rows, cols, rand_row, rand_col)

    dE = 2 * J * ds

    return dE

def TotalEnergy(spin_matrix, rows, cols, J):
    E = 0

    for i in range(0, rows):
        for j in range(0, cols):
            E += -1 * J * NearestNeighborSpins(spin_matrix, rows, cols, i, j)

    return E

def TotalMagnetization(spin_matrix, rows, cols):
    magnetization = 0

    for row in spin_matrix:
        for col in row:
            magnetization += col

    magnetization

    return magnetization


def FlipSpins(spin_matrix, rand_row, rand_col, dE, beta, energy, magnetization):
    if dE < 0:
        spin_matrix[rand_row][rand_col] *= (-1)
        energy += 2 * dE
        magnetization += spin_matrix[rand_row][rand_col]        

    else:
        R = np.random.random()
        if R < np.exp(-1 * beta * dE):
            spin_matrix[rand_row][rand_col] *= (-1)
            energy += 2 * dE
            magnetization += spin_matrix[rand_row][rand_col]
            

    return (spin_matrix, energy, magnetization)

def MonteCarlo(spin_matrix, rows, cols, beta, J, energy, magnetization):
    rand_row, rand_col = np.random.randint(0, rows), np.random.randint(0, cols)

    dE = EnergyDifference(spin_matrix, rows, cols, rand_row, rand_col, J)

    spin_matrix, energy, magnetization = FlipSpins(spin_matrix, rand_row, rand_col, dE, beta, energy, magnetization)

    return (spin_matrix, energy, magnetization)