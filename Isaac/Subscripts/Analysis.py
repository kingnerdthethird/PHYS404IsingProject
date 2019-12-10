import numpy as np # used for numerical tools

from . import Backend as backend # subscript for setting up folders
from . import Experiment as experiment # subscript for each part of the project
from . import Matrix as matrix # subscript for managing matrices
from . import Metropolis as metropolis # subscript for implementing Monte Carlo and Metropolis steps
from . import PlotData as plotdata # subscript for plotting data
from . import PrintData as printdata # subscript for printing data to text files

def Magnetization(spin_matrix):
    # this function computes the total magnetization for a matrix
    # it does *not* divide by the number of elements
    # this division is done later when needed

    m = 0 # initialize magnetization value
    print("Initial m = " + str(m)) # print the initial magnetization

    for row in spin_matrix:
        # each row in spin_matrix is a list
        for col in row:
            # even though this is called col, the iteration is over elements
            m += col # since each site is either +1 or -1, we simply add
            print("Current total magnetization =  " + str(m)) # print the current sum

    print("Magnetization = " + str(m))
    return m # return the magnetization

def AverageMangnetization(magnetizations, N_MC):
    # this function computes the average magnetization from a list of m values
    # N_MC is the number of times a spin was flipped (or not)

    average_magnetization = 0 # initialize average magnetization value
    print("Initial Average Magnetization = " + str(average_magnetization)) # print the initial average magnetization

    for m in magnetizations:
        # since magnetizations is a list we can simply iterate through each element
        average_magnetization += m # we sum up the magnetizations
        print("Current total magnetization = " + str(average_magnetization)) # print the current sum of total magnetizations

    average_magnetization /= N_MC # divide by the number of times we implemented monte carlo steps
    print("Average Magnetization = " + str(average_magnetization)) # print the average magnetizations

    return average_magnetization # return the average magnetization

def AverageEnergy(energies, N_MC):
    # this function will compute the average energy given a list of energies
    # N_MC is the number of monte carlo steps taken

    average_energy = 0 # initialize the average energy value
    print("Initial Average Energy = " + str(average_energy)) # print the initial average energy

    for E in energies:
        # iterate over the elements in energies
        average_energy += E # sum up the energies
        print("Current total energy = " + str(average_energy)) # print the current total of the energies

    average_energy /= N_MC # divide by the monte carlo step number to get the average
    print("Average Energy = " + str(average_energy))
    
    return average_energy # return the average energy

def Dispersion(magnetizations, average_magnetization, i):
    # this function will return the dispersion for a list of magnetizations
    # we require the list of magnetizations, the average magnetization, and i
    # in other functions i = N_MC but this is only used in part 1
    # thus, i is only the number of matrices, not the number of monte carlo steps

    magnetizations_squared = 0 # initialize the value of magnetizations squared
    print("Initial magnetizations squared = " + str(magnetizations_squared)) # print the intital m^2

    for m in magnetizations:
        # iterate through the list
        magnetizations_squared += (m**2) # sum up the magnetizations squared
        print("Current total magnetization squared = " + str(magnetizations_squared)) # print the current total for m^2

    magnetizations_squared /= i # divide by the number of matrices
    print("Average Magnetization Squared = " + str(magnetizations_squared)) # print <m^2>
    
    dispersion = magnetizations_squared - (average_magnetization**2) # caluclate the dispersion using (dm)^2 = <m^2> - <m>^2
    print("Dispersion = " + str(dispersion)) # print (dm)^2

    return dispersion # return the dispersion