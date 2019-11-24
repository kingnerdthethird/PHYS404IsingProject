import numpy as np

from . import Backend as backend
from . import Experiment as experiment
from . import Matrix as matrix
from . import PlotData as plotdata
from . import PrintData as printdata

def AverageMangnetization(m_values, N, debug):
    avg_m, avg_m_2, dispersion = 0, 0, 0

    for m in m_values:
        avg_m += m
        avg_m_2 += m**2

        if debug:
            print("Magnetization: " + str(m))
            print("Average magnetization: " + str(avg_m))
            print("Average magnetiation squared: " + str(avg_m_2))

    avg_m /= N
    avg_m_2 /= N
    dispersion = avg_m_2 - (avg_m**2)
    spread = np.sqrt(dispersion)

    if debug:
        print("Average magnetization: " + str(avg_m))
        print("Average magnetiation squared: " + str(avg_m_2))
        print("Dispersion: " + str(dispersion))
        print("Spread: " + str(spread))

    return (avg_m, dispersion, spread)

