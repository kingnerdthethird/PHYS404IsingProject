import os # used to create folders

from . import Analysis as analysis # subscript for analyzing data
from . import Experiment as experiment # subscript for each part of the project
from . import Matrix as matrix # subscript for managing matrices
from . import Metropolis as metropolis # subscript for implementing Monte Carlo and Metropolis steps
from . import PlotData as plotdata # subscript for plotting data
from . import PrintData as printdata # subscript for printing data to text files

def RunNumber():
    # this function reads the run number and updates it

    runs = open ("Isaac/runs.txt", "r") # open the file of run numbers
    run_number = int(runs.readlines()[-1]) # read the last line
    print("Run Number: " + str(run_number)) # print the run number
    runs.close() # close the file

    runs = open("Isaac/runs.txt", "a") # reopen file in append mode
    runs.write('\n' + str(run_number + 1)) # add the next run number

    return run_number # return the run_number

def CreateDirectory(directory):
    # this function creates a directory
    # directory is a string

    if not os.path.exists(directory):
        # if the folder does not exist proceed
        os.mkdir(directory) # make the folder
        
def CreateDirectories(main, directories):
    # this function creates a group of directories

    for directory in directories:
        # iterate through the directories to be created

        target = main + directory # combine the working directory and the folder to be made
        print("Target Directory: " + str(target)) # print the target directory to be created

        CreateDirectory(target) # create the target