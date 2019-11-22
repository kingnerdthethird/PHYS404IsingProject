import numpy.linalg as nlg  ;  import scipy.integrate as si  ;  import matplotlib.pyplot as plt
import numpy as np ; import random  ; import os ; import math ;  from mpl_toolkits.mplot3d import Axes3D
import scipy.optimize as so  ;  import datetime ; import time ; import copy
pi = np.pi ; from scipy import constants as sc
import sympy as sym ; from sympy import pprint
 
 
def Matrix (m):
    x = np.zeros((m , m))
    for i in range(0, m):
        for j in range(0, m):
            num = np.random.random()
            if num >= 0.5:
                x[i]
    return(x)

size = [3, 10, 64]

for i in range(0, 3):
    X = Matrix(size[i])
    print(X)