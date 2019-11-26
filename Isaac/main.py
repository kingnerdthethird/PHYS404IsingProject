import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
# plt.rcParams.update({'font.size': 22})
import os
import Subscripts as ising
# from Subscripts.Backend import RunNumber

debug = True

print_on = False
print_size_on = False
print_matrices_on = False
print_average_on = False
print_dispersion_on = False
print_spread_on = False
print_ms_on = False
plot_on = False
plot_matrix_on = False
plot_dispersions_on = False
plot_spreads_on = False
plot_averages_on = False

run_number = ising.RunNumber(debug)

main = str(os.path.dirname(os.path.abspath(__file__)))
directories = ["/Data",
               "/Data/SpinMatrices", 
               "/Data/SpinMatrices/Plots", 
               "/Data/SpinMatrices/Plots/" + str(run_number),
               "/Data/SpinMatrices/TextPlots", 
               "/Data/SpinMatrices/TextPlots/" + str(run_number),  
               "/Data/Results", 
               "/Data/Magnetizations", 
               "/Data/Figures", 
               "/Data/Figures/" + str(run_number)]

ising.CreateDirectories(main, directories, debug)

outcomes = open("Isaac/Data/Results/Outcome " + str(run_number) + ".txt", "w+")
magnetizations = open("Isaac/Data/Magnetizations/Magnetizations " + str(run_number) + ".txt", "w+")

# level one testing parameters
#parameters, N = [[3, 3]], 5 
# level two testing parameters
#parameters, N = [[3, 3]], 10 
# level three testing parameters
parameters, N = [[10, 10]], 10 
# level four testing parameters
#parameters, N = [[10, 10]], 100 
# small experiment parameters
#parameters, N = [[3, 3], [10, 10], [64, 64]], 1000 
# large experiment parameters
#parameters, N = [[3, 3], [10, 10], [64, 64]], 100000 
# extreme experiment parameters
#parameters, N = [[3, 3], [10, 10], [64, 64], [128, 128], [256, 256]], 1000 
# maximum experiment parameters
#parameters, N = [[3, 3], [10, 10], [64, 64], [128, 128], [256, 256]], 100000 

""" for parameter in parameters:
    dispersions, spreads, averages, Ns, matrices = [], [], [], [], []
    r, c = parameter[0], parameter[1]
    nodes, expected_spread = [r*c] * N, [np.sqrt(r*c)] * N


    for i in range(1, N + 1):
        data = ising.Experiment(r, c, i, outcomes, magnetizations, print_on, plot_matrix_on, run_number, debug)
        dispersion, spread, average, m_s, matrices = data[0], data[1], data[2], data[3], data[4]
        dispersions.append(dispersion)
        spreads.append(spread)
        averages.append(average)
        Ns.append(i)
        # matrices.append(spin_matrix)
        ising.PlotAverageSpin(matrices, r, c, N, run_number, i, debug)
        if print_size_on:
            print("Size: " + str(r) + 'x' + str(c), end = ' ')
        if print_matrices_on:
            print("Matrices: " + str(i), end = ' ')
        if print_average_on: 
            print("Average: " + str(average), end = ' ')
        if print_dispersion_on: 
            print("Dispersion: " + str(dispersion), end = ' ')
        if print_spread_on:
            print("Spread: " + str(spread), end = ' ')
        if print_ms_on:
            print("Magnetizations: " + m_s)
        print('\n')

    if plot_on:
        run_data = [["Dispersions", dispersions, nodes, plot_dispersions_on],
                    ["Spreads", spreads, expected_spread, plot_spreads_on],
                    ["Averages", averages, [0] * N, plot_averages_on]]
        ising.PlotMatrixData(Ns, run_data, r, c, run_number, debug)
 """
""" for parameter in parameters:
    dispersions, spreads, averages, Ns, matrices = [], [], [], [], []
    r, c = parameter[0], parameter[1]
    nodes, expected_spread = [r*c] * N, [np.sqrt(r*c)] * N """

average = ising.Magnetization([[1, -1, 1], [-1, 1, -1], [1, -1, 1]], debug)

# plt.show()