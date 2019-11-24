import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from . import Analysis as analysis
from . import Backend as backend
from . import Experiment as experiment
from . import Matrix as matrix
from . import PrintData as printdata

def PlotMatrix(spins, run_number, i, r, c, N, debug):
    directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/' + str(r) + 'x' + str(c) 
    backend.CreateDirectory(directory, debug)
    directory = directory + '/' + str(i) + " Matrices"
    backend.CreateDirectory(directory, debug)


    fig = plt.figure()
    plt.axis('off')
    fig.patch.set_facecolor('xkcd:blue')

    colors = mpl.colors.ListedColormap(['black', 'white'])
    bounds = [-1, 0, 0, 1]
    norm = mpl.colors.BoundaryNorm(bounds, colors.N)

    spin_matrix = plt.imshow(spins, interpolation='nearest', cmap = colors, norm = norm)
    plt.colorbar(spin_matrix, cmap = colors, norm = norm, boundaries = bounds, ticks = [-1, 1])

    fig.savefig("Isaac/Data/SpinMatrices/Plots/" + 
                str(run_number) + '/'+ 
                str(r) + 'x' + str(c) + '/' + str(i) + " Matrices/"
                "Spin Matrix " + str(i) + 
                " Run " + str(run_number) +
                ".png", 
                dpi = 400)
    plt.close()

def PlotMatrixData(x, data_values, r, c, number, debug):
    directory = "Isaac/Data/Figures/" + str(number)    
    
    plt.figure()
    l = len(data_values)
    i = 1
    for data in data_values:
        if data[3]:
            name, y, expected = data[0], data[1], data[2]
            plt.subplot(l, 1, i)
            plt.plot(x, y, 'o')
            plt.plot(x, y, 'blue')
            plt.plot(x, expected, 'black')
            
            plt.xlabel("Number of Matrices")
            plt.ylabel(name)
            plt.title(name + " as a Function of Number of Matrices " + 
                      '(' + str(r) + 'x' + str(c) + ')')
            i += 1

    plt.tight_layout()
    plt.savefig(directory + '/' + str(r) + 'x' + str(c) + ' ' + name + " Run " + str(number) + '.png', bbox_inches='tight')
    plt.close()

def PlotAverageSpin(matrices, r, c, N, run_number, num, debug):
    directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/' + str(r) + 'x' + str(c) 
    backend.CreateDirectory(directory, debug)
    directory = directory + '/' + "Averages"
    backend.CreateDirectory(directory, debug)

    average_spins = []

    for i in range(0, r):
        row = []
        for j in range(0, c):
            average = 0
            for input_matrix in matrices:
                average += input_matrix[i][j]
            average /= N
            row.append(average)
        average_spins.append(row)

    fig = plt.figure()
    plt.axis('off')
    fig.patch.set_facecolor('xkcd:blue')

    colors = mpl.colors.LinearSegmentedColormap.from_list('mycolormap', ['black', 'grey', 'white'], 256)

    spin_matrix = plt.imshow(average_spins, interpolation='nearest', cmap = colors)
    plt.colorbar(spin_matrix, cmap = colors)

    fig.savefig("Isaac/Data/SpinMatrices/Plots/" + 
                str(run_number) + '/'+ 
                str(r) + 'x' + str(c) + '/' + "Averages/" 
                "Average Spins for " + str(num) + " Matrices " +
                "Run " + str(run_number) + 
                ".png", 
                dpi = 400)

    plt.close()