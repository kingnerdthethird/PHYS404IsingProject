import numpy as np # used for numerical tools

from . import Analysis as analysis # subscript for analyzing data
from . import Backend as backend # subscript for setting up folders
from . import Experiment as experiment # subscript for each part of the project
from . import Matrix as matrix # subscript for managing matrices
from . import PlotData as plotdata # subscript for plotting data
from . import PrintData as printdata # subscript for printing data to text files

def NearestNeighborSpins(spin_matrix, rows, cols, rand_row, rand_col):
    # this computes the value of a(b + c + d + e) where b, c, d, e are nearest neighbors of a
    # modular arithmetic is used to implement the torus shape
    
    a = spin_matrix[rand_row][rand_col] # our target site
    print("Site spin: " + str(a)) # print the spin of the target site
    b = spin_matrix[np.mod(rand_row + 1, rows)][np.mod(rand_col, cols)] # spin below
    print("Spin above site: " + str(b)) # print the spin of the site above the target site
    c = spin_matrix[np.mod(rand_row, rows)][np.mod(rand_col + 1, cols)] # spin to the right
    print("Spin to the right of the site: " + str(c)) # print the spin to the right of the target site
    d = spin_matrix[np.mod(rand_row - 1, rows)][np.mod(rand_col, cols)] # spin above
    print("Spin above the site: " + str(c)) # print the spin above the target site
    e = spin_matrix[np.mod(rand_row, rows)][np.mod(rand_col - 1, cols)] # spin to the left
    print("Spin to the left of the site: " + str(e)) # print to the left of the target site

    neighbor_spins = a * (b + c + d + e) # calculate the nearest neighbor spins
    print("a(b + c + d + e) = " + str(neighbor_spins)) # print a(b + c + d + e)

    return neighbor_spins # return the nearest neighbor spins

def EnergyDifference(spin_matrix, rows, cols, rand_row, rand_col, J):
    # this function computes the cost for the site to flip
    # the cost is given by dE = 2Ja(b + c + d + e)

    ds = NearestNeighborSpins(spin_matrix, rows, cols, rand_row, rand_col) # the nearest neighbor spins
    print("Nearest neighbor spins: " + str(ds)) # print the nearest neightbor spins

    dE = 2 * J * ds # calculate the cost by the formula above
    print("Cost to flip: " + str(dE)) # print the cost to flip

    return dE # return the cost to flip

def TotalEnergy(spin_matrix, rows, cols, J):
    # this function computes the total energy of each matrix

    E = 0 # initialize the total energy

    for i in range(0, rows):
        # iterate through the number of rows

        for j in range(0, cols):
            # iterate through the number of columns

            # E(site) = -1*J*ds(site)
            E += -1 * J * NearestNeighborSpins(spin_matrix, rows, cols, i, j) # add the energy of the site to the sum
            print("Current Energy sum: " + str(E)) # print the current total energy
    
    print("Total Energy: " + str(E)) # print the total energy

    return E # return the total energy

def TotalMagnetization(spin_matrix, rows, cols):
    # this function computes the total magnetization of a matrix

    magnetization = 0 # initialize the total magnetization

    for row in spin_matrix:
        # iterate through the rows of the matrix

        for col in row:
            # iterate through the elements of each row

            magnetization += col # add the spin of the element to the magnetization
            print("Current Magnetization sum: " + str(magnetization))

    print("Total Magnetization: " + str(magnetization)) # print the total magnetization

    return magnetization # return the total magnetization


def FlipSpins(spin_matrix, rand_row, rand_col, dE, beta, energy, magnetization):
    # this function implements the metropolis algorithm

    if dE < 0:
        # if the cost is negative, flip
        spin_matrix[rand_row][rand_col] *= (-1) # flip the spin
        energy += 2 * dE # add the change in energy, equal to 2*dE = 4 * J * a(b + c + d + e)
        print("New Energy: " + str(energy)) # print the new energy
        magnetization += spin_matrix[rand_row][rand_col] # add the change in magnetization
        print("New Magnetization: " + str(magnetization)) # print the new magnetization

    else:
        R = np.random.random() # generate a random number
        if R < np.exp(-1 * beta * dE):
            # if the number is less than the cost, flip
            spin_matrix[rand_row][rand_col] *= (-1) # flip the spin
            energy += 2 * dE # add the change in energy, equal to 2*dE = 4 * J * a(b + c + d + e)
            print("New Energy: " + str(energy)) # print the new energy
            magnetization += spin_matrix[rand_row][rand_col] # add the change in magnetization
            print("New Magnetization: " + str(magnetization)) # print the new magnetization            

    return (spin_matrix, energy, magnetization) # return the new matrix, new energy, and new magnetization as a tuple

def MonteCarlo(spin_matrix, rows, cols, beta, J, energy, magnetization):
    # this fucntion implements the monte carlo method

    rand_row, rand_col = np.random.randint(0, rows), np.random.randint(0, cols) # choose a random site
    print("Random Site: (" + str(rand_row) + ',' + str(rand_col) + ')') # print the chosen site

    dE = EnergyDifference(spin_matrix, rows, cols, rand_row, rand_col, J) # calculate the cost to flip
    print("Cost to flip: " + str(dE)) # print the cost to flip

    # we look at whether or not to flip the site and obtain the new spin matrix, energy, and magnetization
    spin_matrix, energy, magnetization = FlipSpins(spin_matrix, rand_row, rand_col, dE, beta, energy, magnetization)
    print("Spin Matrix: " + str(spin_matrix)) # print the new matrix
    print("Energy: " + str(energy)) # print the new energy
    print("Magnetization: " + str(magnetization)) # print the new magnetization

    return (spin_matrix, energy, magnetization) # return the new matrix, energy, and magnetization as a tuple