import numpy as np # used for numerical tools
import copy # used for deepcopy()

from . import Analysis as analysis # subscript for analyzing data
from . import Backend as backend # subscript for setting up folders
from . import Matrix as matrix # subscript for managing matrices
from . import Metropolis as metropolis # subscript for implementing Monte Carlo and Metropolis steps
from . import PlotData as plotdata # subscript for plotting data
from . import PrintData as printdata # subscript for printing data to text files

def StepOne(parameters, N, run_number):
    # this function runs step one of the project

    for parameter in parameters: # iterate through the parameter values
        print("Parameter: " + str(parameter)) # print the parameter values to work with

        rows, cols = parameter # set the number of rows and number of columns
        print("Rows: " + str(rows) + " Columns: " + str(cols)) # print out the size of the matrices for this run

        spin_matrices, magnetizations = [], [] # initialize the lists of matrices and their corresponding magnetizations
        average_magnetizations, dispersions, spreads = [], [], [] # initialize the lists of the statistical data
        data, x_values = [], [] # data is the data to be plotted, x_values will be the x axis

        average_spin = [[0] * cols] * rows # create a special matrix
                                           # this matrix will be plotted later and is the average spin at each site of a matrix
                                           # the average spins are from the matrices that are created
        print("Average spin matrix: " + str(average_spin)) # print a matrix of zeros, effectively

        for i in range(1, N + 1): # we start at 1 for aesthetics
            spin_matrix = matrix.GenerateMatrix(rows, cols) # generate a spin matrix of size rows by cols
            print("Spin Matrix: " + str(spin_matrix))

            pretty_matrix = matrix.GeneratePrettyMatrix(spin_matrix) # generate a matrix for printing to text files
                                                                     # these matrices used + and - to graphically present the spins
            print("Pretty Matrix: " + str(pretty_matrix)) # print the pretty matrix

            m = analysis.Magnetization(spin_matrix) # calculate the magnetization of the above matrix
            print("Magnetization: " + str(m)) # print the magnetization

            plotdata.PlotMatrix(spin_matrix, rows, cols, run_number, N, i) # plot the matrix
            printdata.PrintSpinMatrix(spin_matrix, rows, cols, m, run_number, i) # print the matrix to a text file
            printdata.PrintPrettyMatrix(pretty_matrix, rows, cols, m, run_number, i) # print the pretty matrix to text file

            spin_matrices.append(spin_matrix) # add the spin matrix to the list of spin matrices
            magnetizations.append(m) # add the magnetization to the list of the corresponding magnetizations

            average_magnetization = analysis.AverageMangnetization(magnetizations, i) #calculate the average magnetizations for the matrices so far
            print("Average Magnetization: " + str(average_magnetization)) # print the current average magnetization
            average_magnetizations.append(average_magnetization) # add the average magnetization to the list of averages

            dispersion = analysis.Dispersion(magnetizations, average_magnetization, i) # calculate the dispersion for the matrices so far
            print("Dispersion: " + str(dispersion)) # print the current dispersion
            dispersions.append(dispersion) # append the dispersion to the list of dispersions

            spread = np.sqrt(dispersion) # calculate the spread by taking the square root of the dispersion
            print("Spread: " + str(spread)) # print the current spread value
            spreads.append(spread) # add the spread to the list of spreads

            x_values.append(i) # we need to keep a list of how many matrices we do for plotting

            average_spin = matrix.GenerateAverageMatrix(spin_matrix, average_spin, rows, cols, i) # this generates a matrix that is the average of the compostite matrix
            print("Average Spin Matrix: " + str(average_spin)) # print the average spin matrix
            plotdata.PlotAverageSpin(average_spin, rows, cols, N, run_number, i) # plot the average spin matrix

        data.append(["Magnetizations", magnetizations, [0] * N]) # add the magnetizations to the plot of data, with an expected value of 0
        data.append(["Average Magnetizations", average_magnetizations, [0] * N]) # add the average magnetizations to the plot of data, with an expected value of 0
        data.append(["Dispersion", dispersions, [rows*cols] * N]) # add the dispersions to the plot of data, with an expected value of the size of the matrices
        data.append(["Spreads", spreads, [np.sqrt(rows*cols)] * N]) # add the dispersions to the plot of data, with an expected value of the square root of the size of the matrices

        plotdata.PlotMatrixData(x_values, data, rows, cols, run_number, N) # plot all the data above

        # calculate the frame rate for the GIF
        # the goal is a 15 second GIF, but if there are less than 15 frames we set the fps to 1
        if N >= 10:
            frames_per_second = int(N/10)
        else:
            frames_per_second = 1

        print("Frames Per Second: " + str(frames_per_second)) # print the frame rate

        # the image directory is where the images are saved
        image_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + '/' + "Averages"
        print("Image Directory: " + str(image_directory)) # print the image directory

        # the save directory is where the GIF is to be saved
        save_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + '/' + "Averages"
        print("Save Directory: " + str(save_directory)) # print the save directory
        plotdata.CreateGif(image_directory, save_directory, frames_per_second, "Averages") # create a GIF of the average as it evolves

def StepTwo(parameters, X, K_range, run_number, J, decimals):
    # this function implements the second part of the project

    for parameter in parameters:
        # iterate through the parameters
        print("Parameters: " + str(parameter)) # print the parameters 
        rows, cols = parameter # set the size of the matrices to the parameters given
        print("Rows: " + str(rows) + " Columns: " + str(cols)) # print the size of the matrix

        N = rows * cols # this is the number of nodes
        print("Number of nodes: " + str(N)) # print the number of nodes
        N_MC = int(N * X) # this is the number of monte carlo steps
        print("Number of Monte Carlo steps: " + str(N_MC)) # print the number of Monte Carlo steps

        # calculate the framerate
        # the goal is a 15 second GIF, but if the number of frames is less than this we set the fps to 1
        if N_MC >= 10:
            frames_per_second = int(N_MC/10)
        else:
            frames_per_second = 1

        print("Framerate: " + str(frames_per_second)) # print the framerate

        original_matrix = matrix.GenerateMatrix(rows, cols) # we generate an original matrix
                                                            # each time the K is stepped we return to the original matrix
        print("Original Matrix: " + str(original_matrix)) # print the original matrix
        average_energies, average_magnetizations, data = [], [], []  # initialize the lists of averages and data

        for K in K_range:
            # iterate through the K values
            
            print("K value: " + str(K)) # print the K value

            spin_matrix = copy.deepcopy(original_matrix) # we set the spin matrix to the original one
                                                         # we need to use deepcopy() to keep the original matrix intact
            print(spin_matrix) # print the spin matrix

            energies, magnetizations = [], [] # intitialize the list of energies and magnetizations

            energy = metropolis.TotalEnergy(spin_matrix, rows, cols, J) # calculate the initial energy for the matrix
            print("Energy: " + str(energy)) # print the initial energy of the matrix
            magnetization = metropolis.TotalMagnetization(spin_matrix, rows, cols) # calculate the initial magnetization of the matrix
            print("Magnetization: " + str(magnetization)) # print the initial magnetization of the matrix
            energies.append(energy) # add the initial energy to the list of energies
            magnetizations.append(magnetization) # add the initial magnetization to the list of magnetizations

            # plot the initial spin configuration
            plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, 0, "K = " + str(round(K, decimals)), decimals, energy, magnetization, N_MC)

            for q in range(1, N_MC + 1):
                # iterate through the steps for our monte carlo step number

                # the spin_matrix, energy, and magnetization are returned by MonteCarlo
                # it checks a random site for flipping and if it flips it generates the new values
                spin_matrix, energy, magnetization = metropolis.MonteCarlo(spin_matrix, rows, cols, K, J, energy, magnetization)
                print("Spin Matrix: " + str(spin_matrix)) # print the spin matrix
                print("Energy: " + str(energy)) # print the energy of the matrix
                print("Magnetization: " + str(magnetization)) # print the magnetization of the matrix

                energies.append(energy) # add the energy of the matrix to the list of energies
                magnetizations.append(magnetization / N) # add the magnetization per site to the list of magnetizations

                # plot the ensemble
                plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, q, "K = " + str(round(K, decimals)), decimals, energy, magnetization, N_MC)
                
            average_energy = analysis.AverageEnergy(energies, N_MC + 1) # calculate the average energy from the list of energies
            print("Average Energy: " + str(average_energy)) # print average energy
            average_magnetization = analysis.AverageMangnetization(magnetizations, N_MC + 1) # calculate the average magnetization
            print("Average Magnetization: " + str(average_magnetization)) # print the average magnetization

            average_energies.append(average_energy) # add the average energy to the list of average energies
            average_magnetizations.append(average_magnetization) # add the average magnetization to the list of average magnetizations

            # the image directory is the location of the images
            image_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/K = " + str(round(K, decimals))
            print("Image Directory: " + str(image_directory)) # print the image directory
            # the save directory is where we will save the GIF
            save_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/Animations/"
            print("Save Directory: " + str(save_directory))
            plotdata.CreateGif(image_directory, save_directory, frames_per_second, "Evolution for K = " + str(round(K, decimals))) # create the GIF of the ensemble

        data.append(["Average Energy", "K", average_energies]) # add the average energy vs. K to the data to be plotted
        data.append(["Average Magnetizations", "K", average_magnetizations]) # add the average magnetization vs. K to the data to be plotted 

        plotdata.PlotEnsembleData(K_range, data, "Averages over K", rows, cols, run_number, X) # plot the data

def FixedK(parameters, run_number):
    # this fucntion runs the monte carlo stuff for a fixed K value

    for parameter in parameters:
        # iterate through the parameters to be used

        print("Parameters: " + str(parameter)) # print the parameters
        rows, cols, X, Y, K, J = parameter # retrieve the parameters
        print("Rows: " + str(rows) + " Columns: " + str(cols)) # print the size of the matrix
        print("Number of time steps: " + str(X)) # print the number of times we iterate through the matrix
        print("Number of Monte Carlo steps per time step: " + str(Y)) # print how many times we flip spins per time step
        print("K value: " + str(K)) # print the fixed value of K
        print("Coupling Constatn: " + str(J)) # print the coupling constant for the system

        N = rows * cols # the size of the matrix
        print("Number of nodes: " + str(N)) # print the number of nodes
        N_MC = int(N * Y) # the number of monte carlo steps
        print("Monte Carlo steps: " + str(N_MC)) # print the number of monte carlo steps (I don't think this is used?)

        # calculate the framerate with a goal of 10 seconds
        if X >= 10:
            frames_per_second = int(X/10)
        else:
            frames_per_second = 1

        print("Framerate: " + str(frames_per_second)) # print the framerate

        spin_matrix = matrix.GenerateMatrix(rows, cols) # generate a spin matrix to use
        print("Spin Matrix: " + str(spin_matrix)) # print the spin matrix

        average_energies, average_magnetizations, data = [], [], [] # initialize the lists of data points
        energies, magnetizations = [], [] # initialize the lists of energies and magnetizations

        energy = metropolis.TotalEnergy(spin_matrix, rows, cols, J) # calculate the initial total energy of the spin matrix
        print("Initial Energy: " + str(energy)) # print the initial energy of the spin matrix
        magnetization = metropolis.TotalMagnetization(spin_matrix, rows, cols) # calculate the initial total magnetization of the spin matrix
        print("Initial Magnetization: " + str(magnetization)) # print the initial magnetization of the spin matrix
        energies.append(energy) # add the initial energy to the list of energies
        magnetizations.append(magnetization / N) # add the initial magnetization per node to the list of magnetizations

        average_energy = analysis.AverageEnergy(energies, N_MC + 1) # calculate the initial average energy of the spin matrix
        print("Initial Average Energy: " + str(average_energy)) # print the initial average energy
        average_magnetization = analysis.AverageMangnetization(magnetizations, N_MC + 1) # calculate the initial average magnetization of the spin matrix
        print("Initial Average Magnetization: " + str(average_magnetization)) # print the initial average magnetization
        average_energies.append(average_energy) # add the initial average energy to the list of average energies
        average_magnetizations.append(average_magnetization) # add the initial average magnetization to the list of average magnetizations

        # plot the initial ensemble
        plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, 0, "K = " + str(round(K, 3)) + " X = " + str(X) + " Y = " + str(Y), 3, energy, magnetization, X)
        
        for i in range(1, X + 1):
            # iterate through the time values

            for j in range(1, Y):
                # iterate through the Y values
                
                # run the monte carlo stuff
                spin_matrix, energy, magnetization = metropolis.MonteCarlo(spin_matrix, rows, cols, K, J, energy, magnetization)
                print("Spin Matrix: " + str(spin_matrix)) # print the spin matrix
                print("Energy: " + str(energy)) # print the energy
                print("Magnetization: " + str(magnetization)) # print the magnetization
                
            energies.append(energy) # add the energy to the list of energies
            magnetizations.append(magnetization / N) # add the magnetization to the list of magnetizations

            # plot the ensemble
            plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, i, "K = " + str(round(K, 3)) + " X = " + str(X) + " Y = " + str(Y), 3, energy, magnetization, X)

            average_energy = analysis.AverageEnergy(energies, N_MC + 1) # calculate the average energy
            print("Average Energy: " + str(average_energy)) # print the average energy
            average_magnetization = analysis.AverageMangnetization(magnetizations, N_MC + 1) # calculate the average magnetization
            print("Average Magnetization: " + str(average_magnetization)) # print the average magnetization

            average_energies.append(average_energy) # add the average energy to the list of average energies
            average_magnetizations.append(average_magnetization) # add the average magnetization to the list of average magnetizations
        
        data.append(["Energy", "Time", energies]) # add the energy vs time to the data to plot
        data.append(["Average Energy", "Time", average_energies]) # add the average energy vs time to the data to plot
        data.append(["Magnetizations", "Time", magnetizations]) # add the magnetization vs time to the data to plot
        data.append(["Average Magnetization", "Time", average_magnetizations]) # add the average magnetixation vs time to the data to plot

        # plot the data above
        plotdata.PlotEnsembleData(range(0, X + 1), data, "Averages over Time (X = " + str(X) + " Y = " + str(Y) + ")", rows, cols, run_number, X)

        # the image directory is the location of the images
        image_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/K = " + str(round(K, 3)) + " X = " + str(X) + " Y = " + str(Y)
        print("Image Directory: " + str(image_directory)) # print the image directory
        # the save directory is where to save the GIF
        save_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/Animations/"
        print("Save Directory: " + str(save_directory)) # print the save directory

        # create the GIF of the evolution over time
        plotdata.CreateGif(image_directory, save_directory, frames_per_second, "Fixed K = " + str(round(K, 3)) + " X = " + str(X) + " Y = " + str(Y))