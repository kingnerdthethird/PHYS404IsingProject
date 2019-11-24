import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
import os

def CreateDirectory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

def GenerateMatrix(r, c):
    matrix = []
    pretty_matrix = []
    m = 0
    for row in range(0, r):
        column = []
        pretty_column = []
        for col in range(0, c):
            if np.random.random() >= 0.5:
                spin = +1
                pretty_spin = "+"
            else:
                spin = -1
                pretty_spin = "-"

            m += spin
            column.append(spin)
            pretty_column.append(pretty_spin)

        matrix.append(column)
        pretty_matrix.append(pretty_column)

    return (matrix, pretty_matrix, m)

def AverageMangnetization(m_values, N):
    avg_m, avg_m_2, dispersion = 0, 0, 0

    for m in m_values:
        avg_m += m
        avg_m_2 += m**2

    avg_m /= N
    avg_m_2 /= N
    dispersion = avg_m_2 - (avg_m**2)
    spread = np.sqrt(dispersion)

    return (avg_m, dispersion, spread)

def PrintMatrix(matrix, spins):
    for row in matrix:
        for col in row:
            spins.write(col)
            spins.write(' ')
        spins.write('\n')

def PlotMatrix(spins, run_number, i, r, c, N):
    directory = "Isaac/SpinMatrices/Plots/" + str(run_number) + '/' + str(r) + 'x' + str(c) 
    CreateDirectory(directory)
    directory = directory + '/' + str(N) + " Matrices"
    CreateDirectory(directory)


    fig = plt.figure()
    plt.axis('off')
    fig.patch.set_facecolor('xkcd:blue')

    colors = mpl.colors.ListedColormap(['black', 'white'])
    bounds = [-1, 0, 0, 1]
    norm = mpl.colors.BoundaryNorm(bounds, colors.N)

    spin_matrix = plt.imshow(spins, interpolation='nearest', cmap = colors, norm = norm)
    plt.colorbar(spin_matrix, cmap = colors, norm = norm, boundaries = bounds, ticks = [-1, 1])

    fig.savefig("Isaac/SpinMatrices/Plots/" + 
                str(run_number) + '/'+ 
                str(r) + 'x' + str(c) + '/' + str(N) + " Matrices/"
                "Spin Matrix " + str(i) + 
                " Run " + str(run_number) +
                ".png", 
                dpi = 400)
    plt.close()

def PlotMatrixData(x, y, expected, r, c, name, number):    
    plt.figure()
    plt.plot(x, y, 'o')
    plt.plot(x, y, 'blue')
    plt.plot(x, expected)
    
    plt.xlabel("Number of Matrices")
    plt.ylabel(name)
    plt.title(name + " as a Function of Number of Matrices")

    plt.savefig(directory + '/' + str(r) + 'x' + str(c) + ' ' + name + " Run " + str(number) + '.png')
    plt.close()

def PlotAverageSpin(matrices, r, c, N, run_number):
    directory = "Isaac/SpinMatrices/Plots/" + str(run_number) + '/' + str(r) + 'x' + str(c) 
    CreateDirectory(directory)
    directory = directory + '/' + str(N) + " Matrices"
    CreateDirectory(directory)

    average_spins = []

    for i in range(0, r):
        row = []
        for j in range(0, c):
            average = 0
            for matrix in matrices:
                average += matrix[i][j]
            average /= N
            row.append(average)
        average_spins.append(row)

    fig = plt.figure()
    plt.axis('off')
    fig.patch.set_facecolor('xkcd:blue')

    colors = mpl.colors.LinearSegmentedColormap.from_list('mycolormap', ['black', 'grey', 'white'], 256)

    spin_matrix = plt.imshow(average_spins, interpolation='nearest', cmap = colors)
    plt.colorbar(spin_matrix, cmap = colors)

    fig.savefig("Isaac/SpinMatrices/Plots/" + 
                str(run_number) + '/'+ 
                str(r) + 'x' + str(c) + '/' + str(N) + " Matrices/" 
                "Average Spins for " + str(N) + " Matrices " +
                "Run " + str(run_number) + 
                ".png", 
                dpi = 400)

    plt.close()

def Experiment(r, c, N, spins, results, magnetizations, print_on, run_number):
    matrices, m_values, dispersion = [], [], 0

    for i in range(0, N):
        matrix, pretty_matrix, m = GenerateMatrix(r, c)
        if print_on:
            PrintMatrix(pretty_matrix, spins)
            spins.write('\n')
            spins.write(str(r) + 'x' + str(c) + ': ' + str(m) + '\n\n')
        PlotMatrix(matrix, run_number, i + 1, r, c, N)
        m_values.append(m)
        matrices.append(matrix)
    
    average, dispersion, spread = AverageMangnetization(m_values, N)
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

runs = open ("Isaac/runs.txt", "r")
run_number = int(runs.readlines()[-1])
runs.close()
runs = open("Isaac/runs.txt", "a")
runs.write('\n' + str(run_number + 1))

print_on = False
plot_on = True

user = "Isaac"
directories = ["/SpinMatrices", 
               "/SpinMatrices/Plots", 
               "/SpinMatrices/Plots/" + str(run_number), 
               "/Results", 
               "/Magnetizations", 
               "/Figures", 
               "/Figures/" + str(run_number)]
for directory in directories:
    CreateDirectory(user + directory)

if print_on:
    spin_matrices = open("Isaac/SpinMatrices/Spin Matrix " + str(run_number) + ".txt", "w+")
else:
    spin_matrices = 0
outcomes = open("Isaac/Results/Outcome " + str(run_number) + ".txt", "w+")
magnetizations = open("Isaac/Magnetizations/Magnetizations " + str(run_number) + ".txt", "w+")

# parameters, N = [[3, 3]], 2 # testing parameters
parameters, N = [[3, 3], [10, 10], [64, 64]], 1000

for parameter in parameters:
    dispersions, spreads, averages, Ns = [], [], [], []
    r, c = parameter[0], parameter[1]
    nodes, expected_spread = [r*c] * N, [np.sqrt(r*c)] * N


    for i in range(1, N + 1):
        data = Experiment(r, c, i, spin_matrices, outcomes, magnetizations, print_on, run_number)
        dispersion, spread, average, m_s, matrices = data[0], data[1], data[2], data[3], data[4]
        dispersions.append(dispersion)
        spreads.append(spread)
        averages.append(average)
        Ns.append(i)
        PlotAverageSpin(matrices, r, c, N, run_number)
        print("Size: " + str(r) + 'x' + str(c) + 
              " Matrices: " + str(i) + 
              " Average: " + str(average) + 
              " Dispersion: " + str(dispersion) + 
              " Spread: " + str(spread) + 
              " Magnetizations: ")
        print(m_s)

    if plot_on:
        PlotMatrixData(Ns, dispersions, nodes, r, c, "Dispersions", run_number)
        PlotMatrixData(Ns, spreads, expected_spread, r, c, "Spreads", run_number)
        PlotMatrixData(Ns, averages, [0] * N, r, c, "Averages", run_number)

# plt.show()