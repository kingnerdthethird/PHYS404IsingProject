import os

from . import Analysis as analysis
from . import Experiment as experiment
from . import Matrix as matrix
from . import Metropolis as metropolis
from . import PlotData as plotdata
from . import PrintData as printdata

def RunNumber():
    runs = open ("Isaac/runs.txt", "r")
    run_number = int(runs.readlines()[-1])
    runs.close()
    runs = open("Isaac/runs.txt", "a")
    runs.write('\n' + str(run_number + 1))

    return run_number

def CreateDirectory(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)
        
def CreateDirectories(main, directories):
    for directory in directories:
        target = main + directory

        CreateDirectory(target)