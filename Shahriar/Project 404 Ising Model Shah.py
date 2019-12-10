# Issac Paliskin
# Shahriar Keshvari
# Luis Argueta
# Tianing Wang
# Yongxiao Yan

from scipy.optimize import curve_fit;  from datetime import datetime
import numpy.linalg as nlg  ;  import matplotlib.pyplot as plt ; import os
import numpy as np ; import copy ; import random ; from scipy import signal

pi = np.pi
os.chdir('C:\\F\\MC\\Phys 404\\Homework')

# The lenght of the temperture 
dt = 0.0025
# This part is to sweep for the different values of temperture
K_sweep = np.arange(0.00001, 0.1 , dt)
#print(len(K_sweep))
# To average over this many matrices
number_of_Ensemble = 5

# "Size" contains the dimention of the matices
size = [20]
leg = ';  for ' + str(size[0]) + 'X' + str(size[0])

L = len(size)
KK = len(K_sweep)
###################################################################################

# Function to create the matrix of spin with random spins
def Matrix (m):
    x = np.zeros((m , m))
    for i in range(0, m):
        for j in range(0, m):
            num = np.random.random()
            if num >= 0.5:
                x[i][j] = 1
            else:
                x[i][j] = -1
    return(x)
####################################################################################

# this function calculates the energy and Magnetization at the same time. This is the latest function we used
# before we used the commented function below but we realized that this new function is running faster. 
# aslo, at first we had a seperated function for calculating the magnetization but then we combined that 
# with energy functio to save on the number of iterations. 
def CalcEnergy( XX , N ):

    energy = 0 ; Sum_M2 = 0
    for i in range(0, N):
        for j in range(0, N):
            Sum_M2 = Sum_M2 + XX[i][j]
            S = XX[i,j]
            nb = -4 * ( XX[(i+1)%N, j] + XX[i,(j+1)%N] + XX[(i-1)%N, j] + XX[i,(j-1)%N] )
            energy += nb*S
    return (energy/N**2, Sum_M2/N**2)

   
################################################################################

# this is the old function that we used to calculate the energy
"""
def Energy ( X , rr):
    cc = rr
    J = -2 #; Sum_M2 = 0
    Sum_E = 0
    for ii in range(0, rr):
        for jj in range(0, cc):
            #Sum_M2 = Sum_M2 + X[ii][jj]
            
            if ii == 0 and jj == 0:
                E = 2 * J * X[ii][jj] * ( X[rr-1][jj] +X[ii+1][jj] +X[ii][cc-1] +X[ii][jj+1] )  
                #print(E)
            elif ii == 0 and jj !=0 and jj!= (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[rr-1][jj] +X[ii+1][jj] +X[ii][jj-1] +X[ii][jj+1] ) 
                #print(E)
            elif ii == 0 and jj == (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[rr-1][jj] +X[ii+1][jj] +X[ii][jj-1] +X[ii][0] ) 
                #print(E)
            elif ii != 0 and ii !=(rr-1) and jj == (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[ii+1][jj] +X[ii][jj-1] +X[ii][0] ) 
                #print(E)
            elif ii == (rr-1) and jj == (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[0][jj] +X[ii][jj-1] +X[ii][0] )
                #print(E)
            elif ii == (rr-1) and jj != 0 and jj != (cc-1) :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[0][jj] +X[ii][jj-1] +X[ii][jj+1] )
                #print(E)
            elif ii == (rr-1) and jj == 0 :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[0][jj] +X[ii][cc-1] +X[ii][jj+1] ) 
                #print(E)
            elif ii != 0 and ii != (rr-1) and jj == 0 :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[ii+1][jj] +X[ii][cc-1] +X[ii][jj+1] ) 
                #print(E)
            else :
                E = 2 * J * X[ii][jj] * ( X[ii-1][jj] +X[ii+1][jj] +X[ii][jj-1] +X[ii][jj+1] )  
                #print(E)
            Sum_E = E + Sum_E
    #print('sum= {}\n'. format(Sum_E))
    return( Sum_E / (rr*cc) )
"""
      
####################################################################################    

# this is soley to graph the therory in comparison to the data
def Critical_Exponent (xx, H , T_c, beta):
    if T_c <= xx :
        return (0)
    else:
        return (H * (1 - xx / T_c)**(beta) )

###################################################################################

# this is just to do the fit
def Critical_Exponent_Fit (xx , HH, Critical_t, beta):

    return (HH * (1 - xx / Critical_t)**(beta) )

####################################################################################

# To be used for iteration of fliping spins
N_mc = (size[0]**2)*15
# to save all the energy and magnetization for each cycle
E_average = np.ones((KK ,N_mc, number_of_Ensemble))
Magg = np.ones((KK, N_mc, number_of_Ensemble))
# this will be used as the x-axis for the running average and magnetization
in_put = np.arange(0, N_mc)

# to randomly pick the spin from this array
All_spins = np.arange(0, size[0])

# To save all final values of the averages
All_Final_Averages = np.ones((len(K_sweep) ,1))

# to loop through temperture
for K in range(0, KK):
    # this timing is just to keep track to see how long each loop for temperture takes.
    print('\n\nTemp= {:.5f},    Left= {}    ,time= {}'. format(K_sweep[K], KK-K , datetime.now()))
    
    # to loop through number of avering per temp
    for i in range(0, number_of_Ensemble):
        #print('Ensemlbe= {},    time= {} '. format(i, datetime.now()))
        X = Matrix(size[0])
        Beta = 1 / (K_sweep[K])
        
        # to loop for flipping spins
        for j in range(0, N_mc):
            # randomly picking to value to flipp the spin
            pick_spin_row = random.choice(All_spins)
            pick_spin_col = random.choice(All_spins)
            # finding the Energy
            Delta_1, Magg[K][j][i] = CalcEnergy( X , size[0] )
            # saving the average values
            E_average[K][j][i] = Delta_1
            
            # to flip the spin to it's opposite value
            if X[pick_spin_row][pick_spin_col] == 1:
                X[pick_spin_row][pick_spin_col] = -1
                # finding the energy after the spin is flipped
                Delta_2 , kick = CalcEnergy (X, size[0])
                
                # compare the two energies       
                # if the change in energy is good leave the spin un changed
                if Delta_2 < Delta_1 :
                    continue
                
                # otherwise use bolts man factor to flipp spin or not
                else :   
                    Boltman_factor = np.exp(-1 * (Delta_2 - Delta_1) * Beta)
                    draw = np.random.random()
                    if draw < Boltman_factor :
                        continue
                    else:
                        X[pick_spin_row][pick_spin_col] = 1

             # to flip the spin to it's opposite value      
            elif X[pick_spin_row][pick_spin_col] == -1:
                X[pick_spin_row][pick_spin_col] = 1
                Delta_2 , kick = CalcEnergy( X , size[0])
                # compare the two energies       
                # if the change in energy is good leave the spin un changed
                if Delta_2 < Delta_1 :

                    continue
                else :
                    Boltman_factor = np.exp(-1 * (Delta_2 - Delta_1) * Beta)
                    draw = np.random.random()

                    if draw < Boltman_factor :

                        continue
                    else:
                        X[pick_spin_row][pick_spin_col] = -1


####################################################################

# creating new arraies to save runinng magnetization and avergaes
Running_Magg = np.ones((KK, N_mc, number_of_Ensemble))
Running_Average = np.ones((KK, N_mc, number_of_Ensemble))

# this nested loop just finds the runinng averages
for K in range(0, KK):
    for j in range(0, number_of_Ensemble):
        for i in range(0, N_mc):
            dummy = E_average[ K, 0:i+1, j ] 
            Running_Average[K][i][j] = ( np.average(dummy) )
            
            dummy = Magg[ K, 0:i+1, j ] 
            Running_Magg[K][i][j] = ( np.average(dummy) )

# To be used for Specific heat and final Mag
Final_Ave_Specifir_Heat = [None]*KK
Final_Ave_Magnetization = [None]*KK

# this loop finds the final averages over every temperture of each ensemble
for i in range(0, KK):
    for j in range(0, number_of_Ensemble):
        Final_Ave_Specifir_Heat[i] = np.average( Running_Average[i, N_mc-1, j ] )
        Final_Ave_Magnetization[i] = np.sqrt(( Running_Magg[ i, N_mc-1, j ] )**2) 

###############################################################################

# The figure name is clear what this part of the code does
Text1 = 'Phase Transition Using Magnetization\n' + str(K_sweep[0]) + ' - ' + str(round(K_sweep[KK-1], 3)) + leg
plt.figure('Phase Transition Using Magnetization', figsize=(9, 8) )

for K in range(0, KK):
    for j in range(0, number_of_Ensemble):
        plt.scatter( K_sweep[K] , Running_Magg[K, N_mc-1, j ], color='k')
        
plt.ylabel('Magnetizatoin', fontsize=14)
plt.xlabel('Temperture', fontsize=14)
plt.grid()
plt.title( Text1 , fontsize= 14)
plt.savefig('Phase Transition Using Magnetization', dpi=None, facecolor='w', edgecolor='w')


###############################################################################

# The figure name is clear what this part of the code does
Text2 = 'Phase Transition Using Energy\n' + str(K_sweep[0]) + ' - ' + str(round(K_sweep[KK-1], 3)) + leg
plt.figure('Phase Transition Using Energy', figsize=(9, 8) )

for K in range(0, KK):
    for j in range(0, number_of_Ensemble):

        plt.scatter( K_sweep[K] , Running_Average[K, N_mc-1, j ], color='k')        
plt.ylabel('Average Energy', fontsize=14)
plt.xlabel('Temperture', fontsize=14)
plt.grid()
plt.title( Text2 , fontsize= 14)
plt.savefig('Phase Transition Using Energy', dpi=None, facecolor='w', edgecolor='w')

##############################################################################

# this determines the the order of the polynimial we used to denoise  data
pol = 5

Text3 = 'Phase Transition Using Averaged Energy\n' +  str(K_sweep[0]) + ' - ' + str(round(K_sweep[KK-1], 3)) + leg
Specific_Heat = signal.savgol_filter(Final_Ave_Specifir_Heat, KK-1, pol)

plt.figure('Interpolatad and Simulation1', figsize=(9, 8))
plt.plot(K_sweep , Specific_Heat, label='After Denoising', color='r' )
plt.scatter( K_sweep ,Final_Ave_Specifir_Heat , label='Data from simulation', color='k')
plt.ylabel('Average Energy', fontsize=14)
plt.xlabel('Temperture',fontsize=14 )
plt.legend(fontsize=14, shadow= True)
plt.grid()
plt.title( Text3 , fontsize= 14)
plt.savefig('Phase Transition Using Averaged Energy', dpi=None, facecolor='w', edgecolor='w')


###############################################################################


Text4 = 'Phase Transition Using Specific Heat'

# to save all the slope values
Slope= np.ones(( KK))

# this loop calculated the slope values
for i in range(0, KK-1):
    Slope[i] = ( Specific_Heat[i+1] - Specific_Heat[i] ) / ( K_sweep[i+1] - K_sweep[i] )

Slope[KK-1] = Slope[KK-2]

# finding the criticl temperture according to the maximum of the specific heat graph
for i in range(0, KK-1):
    if Slope[i] == max(Slope):
        I = i
    else:
        pass

# T_C is the critical temperture
T_C = copy.copy(K_sweep[I])
T_C = str(round(T_C, 4))
Peak = r'$\ T_c $'+ ' =' +  T_C + ' K' +leg
plt.figure('Specific Heat', figsize=(9,8))
plt.plot(K_sweep, Slope, label = Peak, marker='.')
plt.ylabel('Specific Heat', fontsize=14)
plt.xlabel('Temperture',fontsize=14 )
plt.grid()
plt.legend(fontsize=14, shadow= True)
plt.title( Text4 , fontsize= 14)
plt.savefig('Specific Heat', dpi=None, facecolor='w', edgecolor='w')


##############################################################################

# this is to do the fit for our data
New_Temp_For_Fitting = np.linspace(0, K_sweep[I], I)
New_Y = Final_Ave_Magnetization[ 0:I ]
#print(len(New_Temp_For_Fitting))
#print(len(New_Y))
params, params_covariance = curve_fit( Critical_Exponent_Fit , New_Temp_For_Fitting , New_Y , p0 = [ 1 , K_sweep[I] , 1/6 ] )
print(params)

#############################################################################

# this is the critical temp
TT = K_sweep[I]
# to save output values of the theory
sigma = [None]*KK

# using the "Critical_Exponent" to find the theory values
for e in range(0, KK ): 
    sigma[e] = Critical_Exponent(K_sweep[e], params[0], params[1] , params[2])


Text1 = ' Magnetization Vs. temprature (Theory & Data Comparison) = ' + str(K_sweep[0]) + ' - ' + str(round(K_sweep[KK-1], 3)) + leg
theory = 'For theory\n'+ 'H= ' + str(round(params[0],4)) +'\n' + r'$T_c= $' + str(round(params[1],4)) +'\nCritical Ex= ' + str(round(params[2],4))

plt.figure('Sigma', figsize=(9,8))
plt.scatter(K_sweep, Final_Ave_Magnetization, label = 'Data from Simulation' )    
plt.plot(K_sweep, sigma, label= theory , color= 'k' )    
plt.ylabel(r'$\overline{\sigma}$', fontsize=14)
plt.xlabel('Temperture',fontsize=14 )
plt.title(Text1, fontsize=14)
plt.grid() 
plt.legend( fontsize=14)
plt.savefig('Sigma', dpi=None, facecolor='w', edgecolor='w')


###############################################################################

# This is the value for critical temp
# these two graph below are plotting the running average and seperating the graph for below T_c and Above
# those blue and black graph comes from here
TT = K_sweep[I]
Text = 'Running Average of Energy range with respect to temperture = ' + str(K_sweep[0]) + ' - ' + str(round(K_sweep[KK-1], 3)) +'K' + leg
plt.figure('Running Energy Average' , figsize=(9, 8))

for K in range(0, KK):
    for i in range(0, number_of_Ensemble):
        if K_sweep[K] < TT :
            plt.plot( in_put , Running_Average[K,:,i], color='b')
        else:
            plt.plot( in_put , Running_Average[K,:,i], color='k')
plt.title( Text , fontsize= 14)
plt.savefig('Running Energy Average', dpi=None, facecolor='w', edgecolor='w')


Text = 'Running Average of Magnetization with respect to temprature = ' + str(K_sweep[0]) + ' - ' + str(round(K_sweep[KK-1], 3)) + 'K' + leg
for K in range(0, KK):
    for i in range(0, number_of_Ensemble):
        if K_sweep[K] < TT :   
            plt.figure('Running Magnetization Average' , figsize=(9, 8) )
            plt.plot( in_put , Running_Magg[K,:,i], color='b')
        else :
            plt.figure('Running Magnetization Average' , figsize=(9, 8) )
            plt.plot( in_put , Running_Magg[K,:,i], color='k')
plt.title( Text , fontsize= 14)
plt.savefig('Running Magnetization Average', dpi=None, facecolor='w', edgecolor='w')


###############################################################################



          