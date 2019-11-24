import numpy as np

from . import Analysis as analysis
from . import Backend as backend
from . import Matrix as matrix
from . import PlotData as plotdata
from . import PrintData as printdata

def Experiment(r, c, N, results, magnetizations, print_on, plot_matrix_on, run_number, debug):
    matrices, pretty_matrices, m_values, dispersion = [], [], [], 0

    for i in range(0, N):
        spin_matrix, pretty_matrix, m = matrix.GenerateMatrix(r, c)
        
        if plot_matrix_on:
            plotdata.PlotMatrix(spin_matrix, run_number, i + 1, r, c, N)
        m_values.append(m)
        matrices.append(spin_matrix)
        pretty_matrices.append([pretty_matrix, m])
        
        if print_on:
            printdata.PrintMatrix(pretty_matrices, run_number, i + 1, r, c)
    
    average, dispersion, spread = analysis.AverageMangnetization(m_values, N, debug)
    results.write("Size: " + str(r) + 'x' + str(c) + 
                  " Matrices: " + str(N) + 
                  " Average: " + str(average) + 
                  " Dispersion: " + str(dispersion) + 
                  " Spread: " + str(spread))
    results.write('\n\n')
    magnetizations.write(" Magnetizations: " + '\n')
    for m in m_values:
        magnetizations.write(str(m) + ' ')
    magnetizations.write('\n\n')
    return (dispersion, spread, average, m_values, matrices)
