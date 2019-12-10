import numpy as np # used for numerical tools
import matplotlib as mpl # used for plots of matrices
import matplotlib.pyplot as plt # used for plots of data
import imageio # used to output GIFs
import os # used to create directories

from . import Analysis as analysis # subscript for analyzing data
from . import Backend as backend # subscript for setting up folders
from . import Experiment as experiment # subscript for each part of the project
from . import Metropolis as metropolis # subscript for implementing Monte Carlo and Metropolis steps
from . import Matrix as matrix # subscript for managing matrices
from . import PrintData as printdata # subscript for printing data to text files

def PlotMatrixData(x, data, rows, cols, run_number, N):
    # this function plots the data for matrices

    directory = "Isaac/Data/Figures/" + str(run_number) # new directory for the specific run
    print("Matrix Data directory: " + str(directory)) # print the directory for the data
    plt.rcParams.update({'font.size': 24}) # this font might be too big
    
    plt.figure(figsize=(44.0, 34.0)) # set the plot size, which is huge for good resolution
    l = len(data) # length of the data
    print("Length of data: " + str(l)) # print the length of the data
    i = 1 # this is just for subplots

    for input in data:
        # iterate through the different data to plot

        name, y, expected = input[0], input[1], input[2] # gather the information
        print("Name of plot: " + str(name)) # plot the name of the data
        print("Data: " + str(y)) # print the data for the plot
        print("Expected values: " + str(expected)) # print the expected data

        plt.subplot(l, 1, i) # set up the subplots
        plt.plot(x, y, 'o') # plot the data as points
        plt.plot(x, y, 'blue') # plot the lines between the dots
        plt.plot(x, expected, 'black') # plot the expected value
            
        plt.xlabel("Number of Matrices") # label the x axis
        plt.ylabel(name) # label the y axis
        plt.title(name + " as a Function of Number of Matrices " + 
                  '(' + str(rows) + 'x' + str(cols) + ')') # title the plot
        i += 1 # subplot stuff

    plt.tight_layout() # layout is tight to look bettter
    # save the fig to the specific folder:
    plt.savefig(directory + '/' + str(rows) + 'x' + str(cols) + ' ' + " Run " + str(run_number) + ' Data.pdf', bbox_inches='tight', dpi=1000)
    plt.close() # close the plots to save memory

def PlotMatrix(spin_matrix, rows, cols, run_number, N, i):
    # this function plots the matrix itself

    directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/' + str(rows) + 'x' + str(cols) # directory to save plot
    print("Matrix Plot directory: " + str(directory)) # print the directory

    backend.CreateDirectory(directory) # create the above directory
    # this is useful, maybe? but I don't use it
    # directory = directory + '/' + str(i) + " Matrices"
    # backend.CreateDirectory(directory)
    plt.rcParams.update({'font.size': 12}) # maybe too large


    fig = plt.figure(figsize=(5.5, 4.25)) # set the plot, smaller than above to save storage
    plt.axis('off') # turn off the axes
    fig.patch.set_facecolor('xkcd:blue') # this doesn't work

    colors = mpl.colors.ListedColormap(['blue', 'red']) # choose the colors for the colormap
    bounds = [-1, 0, 1] # set the bounds, which is just the spin values
    norm = mpl.colors.BoundaryNorm(bounds, colors.N) # create a norm (not needed?)

    # create a colorplot
    plot_matrix = plt.imshow(spin_matrix, interpolation='nearest', cmap = colors, norm = norm)
    # create a colorbar for a legend of sorts
    plt.colorbar(plot_matrix, cmap = colors, norm = norm, boundaries = bounds, ticks = [-1, 1])

    # save the figure
    fig.savefig("Isaac/Data/SpinMatrices/Plots/" + 
                str(run_number) + '/'+ 
                str(rows) + 'x' + str(cols) + '/' +
                "Spin Matrix " + str(i) + 
                " Run " + str(run_number) +
                ".png", 
                dpi = 200)

    plt.close() # close the plots to save memory

def PlotAverageSpin(average_spins, rows, cols, N, run_number, num):
    # this function plots the average spins

    directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/' + str(rows) + 'x' + str(cols) # directory for the plots
    print("Average Matrix directory: " + str(directory)) # print the average matrix directory
    backend.CreateDirectory(directory) # create the directory
    directory = directory + '/' + "Averages" # another directory for the average plots
    print("Average Matrices directory: " + str(directory)) # print the average matrices directory
    backend.CreateDirectory(directory) # create the directory
    plt.rcParams.update({'font.size': 12}) # maybe too large

    fig = plt.figure(figsize=(5.5, 4.25)) # create the size of the figure, which is small to save space
    plt.axis('off') # turn off the axes
    fig.patch.set_facecolor('xkcd:blue') # doesn't work
    plt.title(str(rows) + "x" + str(cols) + " Matrix " + str(num)) # set the title of the plot

    colors = mpl.colors.LinearSegmentedColormap.from_list('mycolormap', ['blue', 'purple', 'red'], 256) # creates a continuous color map

    # create a colormesh for the average matrix
    plot_matrix = plt.imshow(average_spins, interpolation='nearest', cmap = colors, vmin = -1, vmax = 1) 
    plt.colorbar(plot_matrix, cmap = colors) # legend of sorts

    # save the figure
    fig.savefig("Isaac/Data/SpinMatrices/Plots/" + 
                str(run_number) + '/'+ 
                str(rows) + 'x' + str(cols) + '/' + "Averages/" 
                "Average Spins for " + str(num).zfill(len(str(N))) + " Matrices " +
                "Run " + str(run_number) + 
                ".png", 
                dpi = 100)

    plt.close() # close the plot to save memory

def CreateGif(image_directory, save_directory, frames_per_second, name):
    # this function create the GIF

    images = [] # initialize the list of images for the gif

    for file_name in os.listdir(image_directory):
        # iterate through the images in the directory

        if file_name.endswith('.png'):
            # make sure it's an image

            file_path = os.path.join(image_directory, file_name) # the file path for the image
            print("Image File Path: " + str(file_path)) # print the file path for the image
            images.append(imageio.imread(file_path)) # add the image to the list of images

    # use imageio to create a GIF
    imageio.mimsave(save_directory + str(name) + ".gif", images, fps=frames_per_second)

def PlotEnsembleData(x, data, file_name, rows, cols, run_number, X):
    # this function plots the data for an ensemble

    directory = "Isaac/Data/Figures/" + str(run_number) # directory for this specific run
    print("Directory for Ensemble Data: " + str(directory)) # print the new directory
    plt.rcParams.update({'font.size': 24}) # maybe too large
    
    plt.figure(figsize=(44.0, 34.0)) # set the figure to be huge for good resolution
    l = len(data) # length of the data
    print("Length of the data: " + str(l))
    i = 1 # subplot thing

    for input in data:
        # iterate through the data to be plotted

        name, variable, y = input[0], input[1], input[2] # retrieve the data
        print(str(name) + " vs. " + str(variable)) # print what the data is
        print("Data: " + str(y)) # print the data to be plotted

        plt.subplot(l, 1, i) # create subplot
        plt.plot(x, y, 'o') # plot the data points
        plt.plot(x, y, 'blue') # plot the lines between the points
            
        plt.xlabel(variable) # set x axis label
        plt.ylabel(name) # set y axis label
        plt.title(name + " as a function of " + str(variable) + ' ' + 
                  '(' + str(rows) + 'x' + str(cols) + ')') # set the subplot title
        i += 1 # subplot thing

    plt.tight_layout() # tight to look better
    # save the figure
    plt.savefig(directory + '/' + str(rows) + 'x' + str(cols) + " Ensemble " + file_name + " Run " + str(run_number) + '.pdf', bbox_inches='tight', dpi=1000)
    plt.close() # close to save memory 

def PlotEnsemble(spin_matrix, rows, cols, run_number, i, identifier, decimals, energy, magnetization, N_MC):
    # this plots an ensemble

    # directory for ensembles
    directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/' + str(rows) + 'x' + str(cols) + " Ensembles"
    print("Directory for Ensembles: " + str(directory)) # print the directory for the ensembles
    backend.CreateDirectory(directory) # create the directory for ensembles
    # directory for ensemble animations
    directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/Animations"
    print("Directory for Ensemble Animations: " + str(directory)) # print the directory for ensemble animations
    backend.CreateDirectory(directory) # create the directory for ensemble animations
    # directory for this specific type of ensembles
    directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/' + str(rows) + 'x' + str(cols) + " Ensembles/" + str(identifier) + '/'
    print("Specific Ensemble directory: " + str(directory)) # print the specific directory for these ensembles
    backend.CreateDirectory(directory) # create the specific directory for these ensembles

    # not used anymore
    # directory = directory + '/' + str(i) + " Matrices"
    # backend.CreateDirectory(directory)
    plt.rcParams.update({'font.size': 8}) # maybe too large


    fig = plt.figure(figsize=(5, 5)) # create the figure size, small to save space

    R, C = np.meshgrid(range(rows + 1), range(cols + 1)) # number of rows and columns for the plot
    print("R: " + str(R) + " C: " + str(C)) # print the size of the plot
    colors = mpl.colors.ListedColormap(['blue', 'red']) # create the colormap
    bounds = [-1, 0, 1] # set the bounds, which is the spins
    norm = mpl.colors.BoundaryNorm(bounds, colors.N) # create a norm (not needed?)

    # turn off the ugly axis ticks
    plt.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
    # plot a colormesh
    plt.pcolormesh(R, C, spin_matrix, cmap = colors, norm = norm, vmin = -1, vmax = 1)
    plt.axis('tight') # tight to look better
    # set the plot title
    plt.title(str(identifier) + " Ensemble: " + str(i) + " Energy: " + str(energy) + " Magnetization: " + str(magnetization))

    # save the figure
    fig.savefig("Isaac/Data/SpinMatrices/Plots/" + 
                str(run_number) + '/'+ 
                str(rows) + 'x' + str(cols) + " Ensembles/" + str(identifier) + '/' +
                "Spin Ensemble " + str(i).zfill(len(str(N_MC))) +
                " Run " + str(run_number) +
                ".png", 
                dpi = 200)
                
    plt.close() # close the figure to save memory