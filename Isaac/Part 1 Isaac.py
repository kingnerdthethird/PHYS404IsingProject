import numpy as np

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
        # print(*row, sep = ' ')

        for col in row:
            spins.write(col)
            spins.write(' ')
        spins.write('\n')

def Experiment(r, c, N, spins, results, magnetizations):
    spin_matrices, m_values, dispersion = [], [], 0

    for i in range(0, N):
        matrix, pretty_matrix, m = GenerateMatrix(r, c)
        PrintMatrix(pretty_matrix, spins)
        spins.write('\n')
        m_values.append(m)
        spins.write(str(r) + 'x' + str(c) + ': ' + str(m) + '\n\n')
    
    average, dispersion, spread = AverageMangnetization(m_values, N)
    results.write("Size: " + str(r) + 'x' + str(c) + " Runs: " + str(N) + " Average: " + str(average) + " Dispersion: " + str(dispersion) + " Spread: " + str(spread))
    results.write('\n\n')
    magnetizations.write(" Magnetizations: " + '\n')
    for m in m_values:
        magnetizations.write(str(m) + ' ')
    magnetizations.write('\n\n')
    return (dispersion, spread, average, m_values)

runs = open ("Isaac/runs.txt", "r")
run_number = int(runs.readlines()[-1])
runs.close()
runs = open("Isaac/runs.txt", "a")
runs.write('\n' + str(run_number + 1))

spin_matrices = open("Isaac/SpinMatrices/spin matrix " + str(run_number) + ".txt", "w+")
outcomes = open("Isaac/Results/outcome " + str(run_number) + ".txt", "w+")
magnetizations = open("Isaac/Magnetizations/magnetizations " + str(run_number) + ".txt", "w+")

parameters = [[3, 3], [10, 10], [64, 64]]
N = 100000

for parameter in parameters:
    r, c = parameter[0], parameter[1]
    dispersion, spread, average, m_values = Experiment(r, c, N, spin_matrices, outcomes, magnetizations)
    print("Size: " + str(r) + 'x' + str(c) + " Runs: " + str(N) + " Average: " + str(average) + " Dispersion: " + str(dispersion) + " Spread: " + str(spread) + " Magnetizations: ")
    print(m_values)

spin_matrices.write('\n')