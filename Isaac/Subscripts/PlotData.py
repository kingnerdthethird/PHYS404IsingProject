import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import imageio
import os

from . import Analysis as analysis
from . import Backend as backend
from . import Experiment as experiment
from . import Matrix as matrix
from . import PrintData as printdata

def PlotMatrixData(x, data, rows, cols, run_number, N):
    directory = "Isaac/Data/Figures/" + str(run_number)
    plt.rcParams.update({'font.size': 24})
    
    plt.figure(figsize=(44.0, 34.0))
    l = len(data)
    i = 1

    for input in data:
        name, y, expected = input[0], input[1], input[2]
        # print(y)
        plt.subplot(l, 1, i)
        plt.plot(x, y, 'o')
        plt.plot(x, y, 'blue')
        plt.plot(x, expected, 'black')
            
        plt.xlabel("Number of Matrices")
        plt.ylabel(name)
        plt.title(name + " as a Function of Number of Matrices " + 
                  '(' + str(rows) + 'x' + str(cols) + ')')
        i += 1

    plt.tight_layout()
    plt.savefig(directory + '/' + str(rows) + 'x' + str(cols) + ' ' + name + " Run " + str(run_number) + '.pdf', bbox_inches='tight', dpi=1000)
    plt.close()
    # plt.show()

def PlotMatrix(spin_matrix, rows, cols, run_number, N, i):
    directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/' + str(rows) + 'x' + str(cols) 
    backend.CreateDirectory(directory)
    # directory = directory + '/' + str(i) + " Matrices"
    # backend.CreateDirectory(directory)
    plt.rcParams.update({'font.size': 12})


    fig = plt.figure(figsize=(5.5, 4.25))
    plt.axis('off')
    fig.patch.set_facecolor('xkcd:blue')

    colors = mpl.colors.ListedColormap(['blue', 'red'])
    bounds = [-1, 0, 1]
    norm = mpl.colors.BoundaryNorm(bounds, colors.N)

    spin_matrix = plt.imshow(spin_matrix, interpolation='nearest', cmap = colors, norm = norm)
    plt.colorbar(spin_matrix, cmap = colors, norm = norm, boundaries = bounds, ticks = [-1, 1])

    fig.savefig("Isaac/Data/SpinMatrices/Plots/" + 
                str(run_number) + '/'+ 
                str(rows) + 'x' + str(cols) + '/' +
                "Spin Matrix " + str(i) + 
                " Run " + str(run_number) +
                ".png", 
                dpi = 200)
    plt.close()

def PlotAverageSpin(average_spins, rows, cols, N, run_number, num):
    directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/' + str(rows) + 'x' + str(cols) 
    backend.CreateDirectory(directory)
    directory = directory + '/' + "Averages"
    backend.CreateDirectory(directory)
    plt.rcParams.update({'font.size': 12})

    # print(average_spins)

    fig = plt.figure(figsize=(5.5, 4.25))
    plt.axis('off')
    fig.patch.set_facecolor('xkcd:blue')
    plt.title(str(rows) + "x" + str(cols) + " Matrix " + str(num))

    colors = mpl.colors.LinearSegmentedColormap.from_list('mycolormap', ['blue', 'purple', 'red'], 256)

    spin_matrix = plt.imshow(average_spins, interpolation='nearest', cmap = colors, vmin = -1, vmax = 1)
    plt.colorbar(spin_matrix, cmap = colors)

    fig.savefig("Isaac/Data/SpinMatrices/Plots/" + 
                str(run_number) + '/'+ 
                str(rows) + 'x' + str(cols) + '/' + "Averages/" 
                "Average Spins for " + str(num).zfill(len(str(N))) + " Matrices " +
                "Run " + str(run_number) + 
                ".png", 
                dpi = 100)

    plt.close()

def CreateGif(image_directory, save_directory, frames_per_second):
    images = []

    # print(os.listdir(image_directory))

    for file_name in os.listdir(image_directory):
        print(file_name)
        if file_name.endswith('.png'):
            file_path = os.path.join(image_directory, file_name)
            images.append(imageio.imread(file_path))

    imageio.mimsave(save_directory + "/Averages.gif", images, fps=frames_per_second)