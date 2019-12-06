import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

import Subscripts as ising

run_number = ising.RunNumber()
print(run_number)

main = str(os.path.dirname(os.path.abspath(__file__)))
print(main)
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
print(directories)

ising.CreateDirectories(main, directories)

parameters, N = [[1, 1], [2, 2], [4, 4], [8, 8], [16, 16], [32, 32], [64, 64], [128, 128], [256, 256], [512, 512], [1024, 1024]], 1000
print(parameters)
print(N)
print('\n')
# parameters, N = [[64, 64]], 100

for parameter in parameters:
    rows, cols = parameter[0], parameter[1]
    print("Rows: " + str(rows) + " Cols: " + str(cols))
    spin_matrices, magnetizations = [], []
    average_magnetizations, dispersions, spreads = [], [], []
    data, x_values = [], []

    average_spin = [[0] * cols] * rows

    for i in range(1, N + 1):
        spin_matrix = ising.GenerateMatrix(rows, cols)
        print(spin_matrix)
        pretty_matrix = ising.GeneratePrettyMatrix(spin_matrix)
        print(pretty_matrix)
        m = ising.Magnetization(spin_matrix)
        print(m)

        # ising.PlotMatrix(spin_matrix, rows, cols, run_number, N, i)

        # ising.PrintSpinMatrix(spin_matrix, rows, cols, m, run_number, i)
        # ising.PrintPrettyMatrix(pretty_matrix, rows, cols, m, run_number, i)

        spin_matrices.append(spin_matrix)
        print(spin_matrices)
        magnetizations.append(m)
        print(magnetizations)

        average_magnetization = ising.AverageMangnetization(magnetizations, i)
        print(average_magnetization)
        average_magnetizations.append(average_magnetization)
        print(average_magnetizations)

        dispersion = ising.Dispersion(magnetizations, average_magnetization, i)
        print(dispersion)
        dispersions.append(dispersion)
        print(dispersions)

        spread = np.sqrt(dispersion)
        print(spread)
        spreads.append(spread)
        print(spreads)

        x_values.append(i)
        print(x_values)

        average_spin = ising.GenerateAverageMatrix(spin_matrix, average_spin, rows, cols, i)
        print(average_spin)
        ising.PlotAverageSpin(average_spin, rows, cols, N, run_number, i)
        print('\n')

    data.append(["Magnetizations", magnetizations, [0] * N])
    print(data)
    data.append(["Average Magnetizations", average_magnetizations, [0] * N])
    print(data)
    data.append(["Dispersion", dispersions, [rows*cols] * N])
    print(data)
    data.append(["Spreads", spreads, [np.sqrt(rows*cols)] * N])
    print(data)

    ising.PlotMatrixData(x_values, data, rows, cols, run_number, N)

    if N >= 30:
        frames_per_second = int(N/30)
    else:
        frames_per_second = 1

    print(frames_per_second)

    image_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + '/' + "Averages"
    print(image_directory)
    save_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + '/' + "Averages"
    print(save_directory)
    ising.CreateGif(image_directory, save_directory, frames_per_second)