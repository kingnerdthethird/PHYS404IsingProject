import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

import Subscripts as ising

run_number = ising.RunNumber()
# print(run_number)

main = str(os.path.dirname(os.path.abspath(__file__)))
# print(main)
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
# print(directories)

ising.CreateDirectories(main, directories)

# parameters, N = [[1, 1], [2, 2], [4, 4], [8, 8], [16, 16], [32, 32], [64, 64], [128, 128], [256, 256], [512, 512], [1024, 1024]], 1000
parameters, N = [[32, 32]], 100

print("step one")
# ising.StepOne(parameters, N, run_number)
print('\n')

parameters, X, K_i, K_f, dK, J = [[32, 32]], 10, 0.01, 0.5, 0.01, 1

if K_i >= 0.1:
    decimals = 1
elif K_i >= 0.01:
    decimals = 2
elif K_i >= 0.001:
    decimals = 3
elif K_i >= 0.0001:
    decimals = 4
elif K_i >= 0.00001:
    decimals = 5

N_K = int((K_f - K_i + dK) / dK)
K_range = np.linspace(K_i, K_f, N_K)

print("step two")
# ising.StepTwo(parameters, X, K_range, run_number, J, decimals)
print('\n')

parameters = [ [200, 200, 1000, 100, 1, 1],
               [200, 200, 1000, 1000, 1, 1],
               [200, 200, 1000, 10000, 1, 1] ]

print("fixed k")
ising.FixedK(parameters, run_number)
run_number = ising.RunNumber()
ising.FixedK(parameters, run_number)
run_number = ising.RunNumber()
ising.FixedK(parameters, run_number)
run_number = ising.RunNumber()
ising.FixedK(parameters, run_number)