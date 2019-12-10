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
        print(parameter)
        rows, cols = parameter
        spin_matrices, magnetizations = [], []
        average_magnetizations, dispersions, spreads = [], [], []
        data, x_values = [], []

        average_spin = [[0] * cols] * rows

        for i in range(1, N + 1):
            spin_matrix = matrix.GenerateMatrix(rows, cols)
            pretty_matrix = matrix.GeneratePrettyMatrix(spin_matrix)
            m = analysis.Magnetization(spin_matrix)

            # ising.PlotMatrix(spin_matrix, rows, cols, run_number, N, i)

            # ising.PrintSpinMatrix(spin_matrix, rows, cols, m, run_number, i)
            # ising.PrintPrettyMatrix(pretty_matrix, rows, cols, m, run_number, i)

            spin_matrices.append(spin_matrix)
            magnetizations.append(m)

            average_magnetization = analysis.AverageMangnetization(magnetizations, i)
            average_magnetizations.append(average_magnetization)

            dispersion = analysis.Dispersion(magnetizations, average_magnetization, i)
            dispersions.append(dispersion)

            spread = np.sqrt(dispersion)
            spreads.append(spread)

            x_values.append(i)

            average_spin = matrix.GenerateAverageMatrix(spin_matrix, average_spin, rows, cols, i)
            plotdata.PlotAverageSpin(average_spin, rows, cols, N, run_number, i)

        data.append(["Magnetizations", magnetizations, [0] * N])
        data.append(["Average Magnetizations", average_magnetizations, [0] * N])
        data.append(["Dispersion", dispersions, [rows*cols] * N])
        data.append(["Spreads", spreads, [np.sqrt(rows*cols)] * N])

        plotdata.PlotMatrixData(x_values, data, rows, cols, run_number, N)

        if N >= 30:
            frames_per_second = int(N/30)
        else:
            frames_per_second = 1

        image_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + '/' + "Averages"
        save_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + '/' + "Averages"
        plotdata.CreateGif(image_directory, save_directory, frames_per_second, "Averages")

def StepTwo(parameters, X, K_range, run_number, J, decimals):
    for parameter in parameters:
        print(parameter)
        rows, cols = parameter

        N = rows * cols
        N_MC = int(N * X)
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
            plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, 0, "K = " + str(round(K, decimals)), decimals, energy, magnetization, N_MC)

            for q in range(1, N_MC + 1):
                spin_matrix, energy, magnetization = metropolis.MonteCarlo(spin_matrix, rows, cols, K, J, energy, magnetization)
                energies.append(energy)
                magnetizations.append(magnetization / N)
                plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, q, "K = " + str(round(K, decimals)), decimals, energy, magnetization, N_MC)
                
            average_energy = analysis.AverageEnergy(energies, N_MC + 1)
            average_magnetization = analysis.AverageMangnetization(magnetizations, N_MC + 1)

            average_energies.append(average_energy)
            average_magnetizations.append(average_magnetization)
            
            image_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/K = " + str(round(K, decimals))
            save_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/Animations/"
            plotdata.CreateGif(image_directory, save_directory, frames_per_second, "Evolution for K = " + str(round(K, decimals)))

        data.append(["Average Energy", "K", average_energies])
        data.append(["Average Magnetizations", "K", average_magnetizations])     

        plotdata.PlotEnsembleData(K_range, data, "Averages over K", rows, cols, run_number, X)
    return 0

def FixedK(parameters, run_number):
    for parameter in parameters:
        print(parameter)
        rows, cols, X, Y, K, J = parameter

        N = rows * cols
        N_MC = int(N * X)

        if X >= 10:
            frames_per_second = int(X/10)
        else:
            frames_per_second = 1

        spin_matrix = matrix.GenerateMatrix(rows, cols)
        average_energies, average_magnetizations, data = [], [], []
        energies, magnetizations = [], []

        energy = metropolis.TotalEnergy(spin_matrix, rows, cols, J)
        magnetization = metropolis.TotalMagnetization(spin_matrix, rows, cols)
        energies.append(energy)
        magnetizations.append(magnetization)

        average_energy = analysis.AverageEnergy(energies, N_MC + 1)
        average_magnetization = analysis.AverageMangnetization(magnetizations, N_MC + 1)
        average_energies.append(average_energy)
        average_magnetizations.append(average_magnetization)

        plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, 0, "K = " + str(round(K, 3)) + " X = " + str(X) + " Y = " + str(Y), 3, energy, magnetization, X)
        for i in range(1, X + 1):
            for j in range(1, Y + 1):
                spin_matrix, energy, magnetization = metropolis.MonteCarlo(spin_matrix, rows, cols, K, J, energy, magnetization)
                
            energies.append(energy)
            magnetizations.append(magnetization / N)

            plotdata.PlotEnsemble(spin_matrix, rows, cols, run_number, i, "K = " + str(round(K, 3)) + " X = " + str(X) + " Y = " + str(Y), 3, energy, magnetization, X)

            average_energy = analysis.AverageEnergy(energies, N_MC + 1)
            average_magnetization = analysis.AverageMangnetization(magnetizations, N_MC + 1)

            average_energies.append(average_energy)
            average_magnetizations.append(average_magnetization)
        
        data.append(["Energy", "Time", energies])
        data.append(["Average Energy", "Time", average_energies])
        data.append(["Magnetizations", "Time", magnetizations])
        data.append(["Average Magnetization", "Time", average_magnetizations])
        plotdata.PlotEnsembleData(range(0, X + 1), data, "Averages over Time (X = " + str(X) + " Y = " + str(Y) + ")", rows, cols, run_number, X)

        image_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/K = " + str(round(K, 3)) + " X = " + str(X) + " Y = " + str(Y)
        save_directory = "Isaac/Data/SpinMatrices/Plots/" + str(run_number) + '/'+ str(rows) + 'x' + str(cols) + " Ensembles/Animations/"
        plotdata.CreateGif(image_directory, save_directory, frames_per_second, "Fixed K = " + str(round(K, 3)) + " X = " + str(X) + " Y = " + str(Y))
