import numpy as np
import copy

from . import Analysis as analysis
from . import Backend as backend
from . import Matrix as matrix
from . import Metropolis as metropolis
from . import PlotData as plotdata
from . import PrintData as printdata

def StepOne(parameters, N, run_number):
    for parameter in parameters:
        rows, cols = parameter
        print("Rows: " + str(rows) + " Cols: " + str(cols))
        spin_matrices, magnetizations = [], []
        average_magnetizations, dispersions, spreads = [], [], []
        data, x_values = [], []

        average_spin = [[0] * cols] * rows

        for i in range(1, N + 1):
            spin_matrix = matrix.GenerateMatrix(rows, cols)
            print(spin_matrix)
            pretty_matrix = matrix.GeneratePrettyMatrix(spin_matrix)
            print(pretty_matrix)
            m = analysis.Magnetization(spin_matrix)
            print(m)

            # ising.PlotMatrix(spin_matrix, rows, cols, run_number, N, i)

            # ising.PrintSpinMatrix(spin_matrix, rows, cols, m, run_number, i)
            # ising.PrintPrettyMatrix(pretty_matrix, rows, cols, m, run_number, i)

            spin_matrices.append(spin_matrix)
            print(spin_matrices)
            magnetizations.append(m)
            print(magnetizations)

            average_magnetization = analysis.AverageMangnetization(magnetizations, i)
            print(average_magnetization)
            average_magnetizations.append(average_magnetization)
            print(average_magnetizations)

            dispersion = analysis.Dispersion(magnetizations, average_magnetization, i)
            print(dispersion)
            dispersions.append(dispersion)
            print(dispersions)

            spread = np.sqrt(dispersion)
            print(spread)
            spreads.append(spread)
            print(spreads)

            x_values.append(i)
            print(x_values)

            average_spin = matrix.GenerateAverageMatrix(spin_matrix, average_spin, rows, cols, i)
            print(average_spin)
            plotdata.PlotAverageSpin(average_spin, rows, cols, N, run_number, i)
            print('\n')

        data.append(["Magnetizations", magnetizations, [0] * N])
        print(data)
        data.append(["Average Magnetizations", average_magnetizations, [0] * N])
        print(data)
        data.append(["Dispersion", dispersions, [rows*cols] * N])
        print(data)
        data.append(["Spreads", spreads, [np.sqrt(rows*cols)] * N])
        print(data)

        plotdata.PlotMatrixData(x_values, data, rows, cols, run_number, N)

        if N >= 30:
            frames_per_second = int(N/30)
        else:
            frames_per_second = 1

        print(frames_per_second)

        image_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + '/' + "Averages"
        print(image_directory)
        save_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + '/' + "Averages"
        print(save_directory)
        plotdata.CreateGif(image_directory, save_directory, frames_per_second, "Averages")

def StepTwo(parameters, X, K_range, run_number, J, decimals):
    for parameter in parameters:
        rows, cols = parameter

        N = rows * cols
        N_MC = N * X
        if N_MC >= 15:
            frames_per_second = int(N_MC/15)
        else:
            frames_per_second = 1

        original_matrix = matrix.GenerateMatrix(rows, cols)
        average_energies, average_magnetizations, data = [], [], []

        for K in K_range:
            spin_matrix = copy.deepcopy(original_matrix)
            energies, magnetizations = [], []
            energy = metropolis.TotalEnergy(spin_matrix, rows, cols, J)
            magnetization = metropolis.TotalMagnetization(spin_matrix, rows, cols)
            energies.append(energy)
            magnetizations.append(magnetization)
            plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, 0, K, decimals, energy, magnetization, N_MC)

            for q in range(1, N_MC + 1):
                spin_matrix, energy, magnetization = metropolis.MonteCarlo(spin_matrix, rows, cols, K, J, energy, magnetization)
                energies.append(energy)
                magnetizations.append(magnetization / N)
                plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, q, K, decimals, energy, magnetization, N_MC)
                
            average_energy = analysis.AverageEnergy(energies, N_MC + 1)
            average_magnetization = analysis.AverageMangnetization(magnetizations, N_MC + 1)

            average_energies.append(average_energy)
            average_magnetizations.append(average_magnetization)
            
            image_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/K = " + str(round(K, decimals))
            save_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/Animations/"
            plotdata.CreateGif(image_directory, save_directory, frames_per_second, "Evolution for K = " + str(round(K, decimals)))

        data.append(["Average Energy", average_energies])
        data.append(["Average Magnetizations", average_magnetizations])     

        plotdata.PlotEnsembleData(K_range, data, rows, cols, run_number, X)
    return 0