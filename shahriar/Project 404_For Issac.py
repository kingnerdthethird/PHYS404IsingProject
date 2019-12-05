# Issac Paliskin
# Shahriar Keshvari
# Luis Argueta
# Tianing Wang
# Yongxiao Yan

from scipy.interpolate import CubicSpline ; from scipy.optimize import curve_fit
import numpy.linalg as nlg  ;  import matplotlib.pyplot as plt ; import os
import numpy as np ; import os ; import copy ; import random
pi = np.pi
os.chdir('C:\\F\\MC\\Phys 404\\Homework\\Final project\\Matrix\\10X10')
#print(os.getcwd())
K_sweep = np.arange(1, 6 , 0.1)
#print(K_sweep)
# To average over this many matrices
number_of_Ensemble = 1
# "Size" contains the dimention of the matices
size = [5]
            
L = len(size)
KK = len(K_sweep)
###################################################################################

# Function to create the matrix of spin
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
    
def Energy ( X ):
    rr, cc= np.shape(X)
    J = -2
    Sum_E = 0
    for ii in range(0, rr):
        for jj in range(0, cc):
            
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

###################################################################################

def Calculate_Magnatization(Sample):
    Sum_M = 0
    row, col= np.shape(Sample)
    for p in range(0, row):
        for k in range(0, col):
            Sum_M = Sum_M + Sample[p][k]     
    return ( Sum_M /(row*col) )
            
####################################################################################    

def Critical_Exponent (xx, H , T_c, beta):
    for iii in range(0, len(xx)):
        if T_c <= xx[iii] :
            return (0)
        else:
            return (H * (1 - xx[iii] / T_c)**(beta) )

####################################################################################


N_mc = (size[0]**2)*30
E_average = np.ones((KK ,N_mc, number_of_Ensemble))
Magg = np.ones((KK, N_mc, number_of_Ensemble))
in_put = np.arange(0, N_mc)


All_Final_Averages = np.ones((len(K_sweep) ,1))

for K in range(0, KK):

    os.mkdir( str(K_sweep[K]) )
    os.chdir( str(K_sweep[K]) )
    
    for i in range(0, number_of_Ensemble):
        X = Matrix(size[0])
        #print(X)
        Beta = 1 / (K_sweep[K])
        All_spins = np.arange(0, size[0])
        
        for j in range(0, 10):
            NAME=str(j)+'.txt'
            np.savetxt(NAME, X)
            #print('j={}'. format(j))
            pick_spin_row = random.choice(All_spins)
            pick_spin_col = random.choice(All_spins)
            #print('\nrow={}  col={}\n'. format(pick_spin_row, pick_spin_col))
            Delta_1 = Energy( X )
            Magg[K][j][i] = Calculate_Magnatization(X)
    
            #print('Energy before flip {}'. format(Delta_1))
            E_average[K][j][i] = Delta_1
            
            if X[pick_spin_row][pick_spin_col] == 1:
                X[pick_spin_row][pick_spin_col] = -1
                Delta_2 = Energy( X )
                #print(X)
                #print('Energy After flip {}\n'. format(Delta_2))
                if Delta_2 < Delta_1 :
                    #print('good')
                    #print('end\n')
                    continue
                else :
                    Boltman_factor = np.exp(-1 * (Delta_2 - Delta_1) * Beta)
                    draw = np.random.random()
                    #print( 'Boltman factor={}   Draw={}' . format(Boltman_factor, draw))
                    if draw < Boltman_factor :
                        #print(X)
                        X[pick_spin_row][pick_spin_col] = -1
                        continue
                    else:
                        X[pick_spin_row][pick_spin_col] = 1
                        #print('end\n')
                    
            elif X[pick_spin_row][pick_spin_col] == -1:
                X[pick_spin_row][pick_spin_col] = 1
                Delta_2 = Energy( X )
                #print(X)
                #print('Energy After flip {}\n'. format(Delta_2))
                if Delta_2 < Delta_1 :
                    #print('good')
                    #print(X)
                    continue
                else :
                    Boltman_factor = np.exp(-1 * (Delta_2 - Delta_1) * Beta)
                    draw = np.random.random()
                    #print( 'Boltman factor={}   Draw={}' . format(Boltman_factor, draw))
                    if draw < Boltman_factor :
                        X[pick_spin_row][pick_spin_col] = 1
                        continue
                    else:
                        X[pick_spin_row][pick_spin_col] = -1

    os.chdir('C:\\F\\MC\\Phys 404\\Homework\\Final project\\Matrix\\10X10')
    
"""   
####################################################################

Running_Magg = np.ones((KK, N_mc, number_of_Ensemble))
Running_Average = np.ones((KK, N_mc, number_of_Ensemble))

for K in range(0, KK):
    for j in range(0, number_of_Ensemble):
        for i in range(0, N_mc):
            dummy = E_average[ K, 0:i+1, j ] 
            Running_Average[K][i][j] = ( np.average(dummy) )
            
            dummy = Magg[ K, 0:i+1, j ] 
            Running_Magg[K][i][j] = ( np.average(dummy) )


#####################################################################


Text = 'Running Average of Energy range with respect to temperture = ' + str(K_sweep[0]) + ' - ' + str(round(K_sweep[KK-1], 3))
for K in range(0, KK):
    for i in range(0, number_of_Ensemble):
        if K_sweep[K] < 1.1 :
            plt.figure('Running Energy Average' , figsize=(9, 8))
            plt.plot( in_put , Running_Average[K,:,i], color='b')
        else:
            plt.figure('Running Energy Average' , figsize=(9, 8))
            plt.plot( in_put , Running_Average[K,:,i], color='k')
plt.title( Text , fontsize= 14)
plt.savefig('Running Energy Average', dpi=None, facecolor='w', edgecolor='w')

######################################################################

Text = 'Running Average of Magnetization with respect to temprature = ' + str(K_sweep[0]) + ' - ' + str(round(K_sweep[KK-1], 3))
for K in range(0, KK):
    for i in range(0, number_of_Ensemble):
        if K_sweep[K] < 1.1 :   
            plt.figure('Running Magnetization Average' , figsize=(9, 8) )
            plt.plot( in_put , Running_Magg[K,:,i], color='b')
        else :
            plt.figure('Running Magnetization Average' , figsize=(9, 8) )
            plt.plot( in_put , Running_Magg[K,:,i], color='k')
plt.title( Text , fontsize= 14)
plt.savefig('Running Magnetization Average', dpi=None, facecolor='w', edgecolor='w')

#######################################################################

for K in range(0, KK):
    for j in range(0, number_of_Ensemble):
        plt.figure('Phase Transition Using Magnetization', figsize=(9, 8) )
        plt.scatter( K_sweep[K] , Running_Magg[K, N_mc-1, j ], color='k')
        plt.ylabel('Magnetizatoin', fontsize=14)
        plt.xlabel('Temperture', fontsize=14)
plt.grid()
plt.savefig('Phase Transition Using Magnetization', dpi=None, facecolor='w', edgecolor='w')


#####################################################################

for K in range(0, KK):
    for j in range(0, number_of_Ensemble):
        plt.figure('Phase Transition Using Energy', figsize=(9, 8) )
        plt.scatter( K_sweep[K] , Running_Average[K, N_mc-1, j ], color='k')
        plt.ylabel('Average Energy', fontsize=14)
        plt.xlabel('Temperture', fontsize=14)
plt.grid()
plt.savefig('Phase Transition Using Energy', dpi=None, facecolor='w', edgecolor='w')
#####################################################################

Temperture_for_Interpolation = np.arange(K_sweep[0], K_sweep[KK-1], 0.1)
Final_Ave_Specifir_Heat = [None]*KK
Final_Ave_Magnetization = [None]*KK

for i in range(0, KK):
    for j in range(0, number_of_Ensemble):
        Final_Ave_Specifir_Heat[i] = np.average( Running_Average[i, N_mc-1, j ] )
        Final_Ave_Magnetization[i] = np.sqrt(( Running_Magg[ i, N_mc-1, j ] )**2) 


params, params_covariance = curve_fit( Critical_Exponent , K_sweep , Final_Ave_Magnetization , p0 = [ 1 , 1.5  , 1/8 ] )
print(params)



Text1 = ' Magnetization with respect to temprature = ' + str(K_sweep[0]) + ' - ' + str(round(K_sweep[KK-1], 3))
plt.figure('Sigma')
plt.scatter(K_sweep, Final_Ave_Magnetization )    
plt.ylabel(r'$\overline{\sigma}$', fontsize=14)
plt.xlabel('Temperture',fontsize=14 )
plt.title(Text1, fontsize=14)
plt.grid() 
plt.savefig('Sigma', dpi=None, facecolor='w', edgecolor='w')


###############################################################################


Temperture_for_Interpolation = np.arange(K_sweep[0], K_sweep[KK-1], 0.1)
Specific_Heat = CubicSpline(K_sweep, Final_Ave_Specifir_Heat)
Out_Put_Specific_Heat =  Specific_Heat(Temperture_for_Interpolation)



plt.figure('Interpolatad and Simulation', figsize=(9, 8))
plt.plot( Temperture_for_Interpolation, Out_Put_Specific_Heat, label='After Interpolation' )

plt.scatter( K_sweep ,Final_Ave_Specifir_Heat , label='Data from simulation', color='k')
plt.ylabel('Magnetization', fontsize=14)
plt.xlabel('Temperture',fontsize=14 )
plt.legend(fontsize=14, shadow= True)
plt.grid()
plt.savefig('Interpolatad and Simulation', dpi=None, facecolor='w', edgecolor='w')



Slope= [None]* len(Out_Put_Specific_Heat)

for i in range(0, len(Out_Put_Specific_Heat)-1):
    Slope[i] = ( Out_Put_Specific_Heat[i+1] - Out_Put_Specific_Heat[i] ) / ( Temperture_for_Interpolation[i+1] - Temperture_for_Interpolation[i] )

plt.figure('Specific Heat')
plt.plot(Temperture_for_Interpolation, Slope, label='Peak at 0.11 Kelvin')
plt.ylabel('Specific Heat', fontsize=14)
plt.xlabel('Temperture',fontsize=14 )
plt.grid()
plt.legend(fontsize=14, shadow= True)
plt.savefig('Specific Heat', dpi=None, facecolor='w', edgecolor='w')

########################################################################
"""












          