import os

from . import Analysis as analysis
from . import Experiment as experiment
from . import Matrix as matrix
from . import PlotData as plotdata
from . import PrintData as printdata

def CreateDirectory(directory, debug):
    if not os.path.exists(directory):
        os.mkdir(directory)
        if debug:
            print("Created directory " + directory)
        

def CreateDirectories(main, directories, debug):
    for directory in directories:
        target = main + directory
        if debug:
            print("Target directory: " + target)

        CreateDirectory(target, debug)


def RunNumber(debug):
    runs = open ("Isaac/runs.txt", "r")
    run_number = int(runs.readlines()[-1])
    runs.close()
    runs = open("Isaac/runs.txt", "a")
    runs.write('\n' + str(run_number + 1))

    if debug:
        print("Run number: " + str(runs))

    return run_number