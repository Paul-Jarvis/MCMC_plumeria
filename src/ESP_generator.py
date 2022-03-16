#Script that generates ESP's for MCMC simulations

## Import required modules
import sys
import numpy as np
import numpy.f2py
import datetime
import math

## Create wrappers for parts of Fortran Plumeria code such that they can be#####
## loaded as Python modules ####################################################

#EDIT THIS VARIABLE TO STORE PATH TO PLUMERIA SOURCE CODE
plumeriaSrc = '/home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd'

initTfile = plumeriaSrc + '/FindT_init.f90'
initTargs = '-I' + plumeriaSrc + ' ' + plumeriaSrc + '/enthfunctions.o' + ' ' + \
    plumeriaSrc + '/zfunctions.o' + ' ' + plumeriaSrc + '/Module1.o'
with open(initTfile, 'r') as fid:
    source = fid.read()
np.f2py.compile(source, modulename='initT', extension='.f90', \
                extra_args = initTargs)
import initT

enthFuncFile = plumeriaSrc + '/enthSubroutines.f90'
enthFuncArgs = '-I' + plumeriaSrc + ' ' + plumeriaSrc + '/zfunctions.o' + ' ' + \
    plumeriaSrc + '/Module1.o'
with open(enthFuncFile, 'r') as fid:
    source2 = fid.read()
np.f2py.compile(source2, modulename='enthFunc', extension='.f90', \
                extra_args = enthFuncArgs)
import enthFunc

## Name of output file (including path) ########################################
outfile = "../input_files/fullSweep5000/input.txt"    #name of output file

## Inputs - fixed###############################################################
pi             = 3.14159           #pi
nruns          = 5002              #number of runs to set parameters for
                                   #(actually needs to be nruns +1)
vent_elevation = 144               #vent elevation, m
CpMag          = 1000              #Specific heat of magma (J kg^-1 K)
Twater         = 273.15            #Temperature of external water mixed with
                                   #magma at beginning
p0             = 1.013e05          #Pressure at sea level (Pa)
rho_m          = 2500              #Denisty (DRE) of magma (kg m^-3)
R_w            = 8.314 / 0.0180015 #Gas constant for air (J kg-1 K-1)

## Ranges of inputs which are sampled###########################################
logMER_min = 5.5  #minimum log MER (kg/s)
logMER_max = 10.5 #maximum log MER (kg/s)

u_min = 100.0 #minimum ejection velocity (m/s)
u_max = 350.0 #maximum ejection velocity (m/s)

Tmin = 1073 #Minimum magma temperature (K)
Tmax = 1473 #Maximum magma temperature (K)

m_gMin = 0.01 #Minimum magmatic gas fraction
m_gMax = 0.05 #Maximum magmatic gas fraction

m_wMin = 0.0 #Minimum surface water mass fraction
m_wMax = 0.2 #Maximum surface water mass fraction

## Calculate the magma temperature
T_m = Tmin + (Tmax - Tmin) * np.random.random_sample((nruns,))

## Calculate the gas mass fraction
m_g = m_gMin + (m_gMax - m_gMin) * np.random.random_sample((nruns,))

## Calculate the added water mass fraction
m_w = m_wMin + (m_wMax - m_wMin) * np.random.random_sample((nruns,))

## Calculate magma, vapour and liquid enthalpies
magEnth = np.zeros_like(T_m)
vapEnth = np.zeros_like(T_m)

for i in range(0, nruns):
    magEnth[i] = enthFunc.findh_m(T_m[i], vent_elevation, CpMag)
    vapEnth[i] = enthFunc.findh_v(T_m[i])

liqEnth = enthFunc.findh_a(Twater)


## Calculate mixture enthalpy
hmix = (1.0 - m_g - m_w) * magEnth + m_g * vapEnth + m_w * liqEnth

## Calculate the mixture temperature
#print(initT.findt_init.__doc__)
Tmix = np.zeros_like(hmix)

for i in range(0, nruns):
    Tmix[i] = initT.findt_init(1.0 - m_g[i] - m_w[i], 0.0, m_w[i] + m_g[i], hmix[i], p0, m_g[i], 0.0, 0.0)

## Calculate the mixture density
# print((m_g + m_w) * R_w * Tmix / p0)
rho_mix = 1.0 / ((1.0 - m_g - m_w) / rho_m + (m_g + m_w) * R_w * Tmix / p0)

## Calculate the MER and eruption velocity
logMER = logMER_min + (logMER_max-logMER_min) * \
              np.random.random_sample((nruns,))  #generate nruns of random numbers
#logMER = np.array([6.0,6.5,7.0,7.5,8.0,8.5,9.0])
MER = np.exp(np.log(10)*logMER)
u_exit = u_min + (u_max-u_min)*np.random.random_sample((nruns,))

## Calculate vent cross-sectional area
xs_area = MER/(u_exit*rho_mix)
d_vent = 2*np.sqrt(xs_area/pi)

## Convert temperatures to C
Tmin = Tmin - 273.15
Tmax = Tmax - 273.15

## Write out table header
f = open(outfile, "w")
f.write('run #         MER         diam     u_exit     T_m     m_w     m_g     rho_mix\n')
f.write('             kg/s           m        m/s       C                        kg/m3\n')
print(   'run #         MER         diam     u_exit     T_m     m_w     m_g     rho_mix')
print(   '             kg/s           m        m/s       C                        kg/m3')
for irun in range(0,nruns-1):
    f.write('{:5d}   {:12.4e}{:10.0f}{:11.1f}    {:4.0f}    {:4.2f}    {:4.2f}      {:5.3f}\n'. \
            format(irun+1,MER[irun],d_vent[irun],u_exit[irun],T_m[irun] - 273.15, m_w[irun],m_g[irun],rho_mix[irun]))
    print( '{:5d}   {:12.4e}{:10.0f}{:11.1f}    {:4.0f}    {:4.2f}    {:4.2f}      {:5.3f}'. \
            format(irun+1,MER[irun],d_vent[irun],u_exit[irun],T_m[irun] - 273.15,m_w[irun],m_g[irun],rho_mix[irun]))
f.close()

