import numpy as np
import Subscripts as ising
from numpy.random import rand

"""def Energy ( X ):
    rr, cc= np.shape(X)
    J = 0.5
    Sum_E = 0
    for ii in range(0, rr):
        for jj in range(0, cc):
            
            if ii == 0 and jj == 0:
                E = 2 * J * X[ii][jj] * ( X[rr-1][jj] +X[ii+1][jj] +X[ii][cc-1] +X[ii][jj+1] )  
                print(E)
            elif ii == 0 and jj !=0 and jj!= (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[rr-1][jj] +X[ii+1][jj] +X[ii][jj-1] +X[ii][jj+1] ) 
                print(E)
            elif ii == 0 and jj == (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[rr-1][jj] +X[ii+1][jj] +X[ii][jj-1] +X[ii][0] ) 
                print(E)
            elif ii != 0 and ii !=(rr-1) and jj == (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[ii+1][jj] +X[ii][jj-1] +X[ii][0] ) 
                print(E)
            elif ii == (rr-1) and jj == (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[0][jj] +X[ii][jj-1] +X[ii][0] )
                print(E)
            elif ii == (rr-1) and jj != 0 and jj != (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[0][jj] +X[ii][jj-1] +X[ii][jj+1] )
                print(E)
            elif ii == (rr-1) and jj == 0 :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[0][jj] +X[ii][cc-1] +X[ii][jj+1] ) 
                print(E)
            elif ii != 0 and ii != (rr-1) and jj == 0 :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[ii+1][jj] +X[ii][cc-1] +X[ii][jj+1] ) 
                print(E)
            else :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[ii+1][jj] +X[ii][jj-1] +X[ii][jj+1] )  
                print(E)
            Sum_E = E + Sum_E
    print('sum= {}\n'. format(Sum_E))
    return( Sum_E / (rr*cc) )


# test_matrix = ising.GenerateMatrix(4, 4)

test_matrix = [[-1, -1, 1, -1], [-1, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 1]]
print(test_matrix)
print("\n")

E_1 = 0
eb = Energy(test_matrix)



for i in range(0, 4):
    for j in range(0, 4):
        E_1 += test_matrix[i][j] * (
            test_matrix[np.mod(i + 1, 4)][np.mod(j, 4)] + 
            test_matrix[np.mod(i, 4)][np.mod(j + 1, 4)] +
            test_matrix[np.mod(i - 1, 4)][np.mod(j, 4)] +
            test_matrix[np.mod(i, 4)][np.mod(j - 1, 4)]
        )

        print(test_matrix[i][j] * (
            test_matrix[np.mod(i + 1, 4)][np.mod(j, 4)] + 
            test_matrix[np.mod(i, 4)][np.mod(j + 1, 4)] +
            test_matrix[np.mod(i - 1, 4)][np.mod(j, 4)] +
            test_matrix[np.mod(i, 4)][np.mod(j - 1, 4)]
        ))

print("\n\n")
print(eb)
print(E_1)

test_matrix[0][0] *= -1

print("\n\n\n\n")

E_2 = 0
ea = Energy(test_matrix)



for i in range(0, 4):
    for j in range(0, 4):
        E_2 += test_matrix[i][j] * (
            test_matrix[np.mod(i + 1, 4)][np.mod(j, 4)] + 
            test_matrix[np.mod(i, 4)][np.mod(j + 1, 4)] +
            test_matrix[np.mod(i - 1, 4)][np.mod(j, 4)] +
            test_matrix[np.mod(i, 4)][np.mod(j - 1, 4)]
        )

print(ea)
print(E_2)
dE = (E_2 - E_1)
de = (eb - ea)

print(de)

print(dE)



 """

""" state = 2*np.random.randint(2, size=(4,4))-1
print(state)

print(ising.GenerateMatrix(4, 4))
N = 4
def mcmove(config, beta):
    '''Monte Carlo move using Metropolis algorithm '''
    for i in range(N):
        for j in range(N):
                a = np.random.randint(0, N)
                b = np.random.randint(0, N)
                s =  config[a, b]
                print("s " + str(s))
                nb = config[(a+1)%N,b] + config[a,(b+1)%N] + config[(a-1)%N,b] + config[a,(b-1)%N]
                print("nb: " + str(nb))
                cost = 2*s*nb
                print("cost: " + str(cost))
                if cost < 0:
                    s *= -1
                elif rand() < np.exp(-cost*beta):
                    s *= -1
                config[a, b] = s
    return config

mcmove(state, 1) """

""" test_matrix = [[1, 1, -1], [-1, -1, 1], [1, -1, 1]]

print(ising.TotalEnergy(test_matrix, 3, 3, 1))

print(ising.AverageEnergy([4, 6, 2, -4, 8, -12, 16, 10], 8))

print(ising.TotalMagnetization(test_matrix, 3, 3)) """

test_matrix = ising.GenerateMatrix(10, 10)
print(test_matrix)