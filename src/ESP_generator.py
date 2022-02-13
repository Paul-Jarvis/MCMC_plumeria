#Script that generates ESP's for MCMC simulations

import sys
import numpy as np
import numpy.f2py
import datetime
import math

with open('/home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd/FindT_init.f90', 'r') as fid:
    source = fid.read()
np.f2py.compile(source, modulename='initT', extension='.f90', extra_args = '-I/home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd /home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd/enthfunctions.o /home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd/zfunctions.o /home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd/Module1.o')
import initT

with open('/home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd/enthSubroutines.f90', 'r') as fid:
    source2 = fid.read()
np.f2py.compile(source2, modulename='enthFunc', extension='.f90', extra_args = '-I/home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd /home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd/zfunctions.o /home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd/Module1.o')
import enthFunc

## Inputs
pi                  = 3.14159               #pi
nruns               = 502                   #number of runs to set parameters for (actually needs to be nruns +1)
vent_elevation      = 144                 #vent elevation, km - CMT FROM PAUL: I THINK THIS IS M ACTUALLY - although this isn't actually used
logMER_min          = 5.5                    #minimum log MER (kg/s)
logMER_max          = 10.5                  #maximum log MER (kg/s)
u_min               = 100.0                  #minimum ejection velocity (m/s)
u_max               = 350.0                  #maximum ejection velocity (m/s)

Tmin = 1073 #Minimum magma temperature (K)
Tmax = 1473 #Maximum magma temperature (K)
m_gMin = 0.01 #Minimum magmatic gas fraction
m_gMax = 0.05 #Maximum magmatic gas fraction
m_wMin = 0.0 #Minimum surface water mass fraction
m_wMax = 0.2 #Maximum surface water mass fraction
CpMag = 1000 #Specific heat of magma (J kg^-1 K)
Twater = 273.15 #Temperature of external water mixed with magma at beginning
p0 = 1.013e05 #Pressure at sea level (Pa)
rho_m = 2500 #Denisty (DRE) of magma (kg m^-3)
R_w = 8.314 / 0.0180015 #Gas constant for air (J kg-1 K-1)

#Parameters that need to change if we're adjusting mass fraction water
#Use this guide for the density of erupting mixture, assuming T=900 C, m_g=0.03, vent elevation=144 m
#m_w     0    0.05     0.1    0.20       m_w
#    5.948   2.774   2.108   1.998       rho_mix (kg/m3) - Should the first number be 2.948?
#    144.0   210.9   241.9   248.5       sound speed (m/s)
#. . .  assuming T=900 C, m_w=0.00, vent elevation=144 m
#m_g  0.03    0.10    0.20    0.50    0.70    0.90    m_g
#    5.948   1.814   0.909   0.364    0.260   0.202   rho_mix (kg/m3) - Should the first number be 2.948?
#    144.0   260.8   368.5   582.2    688.8   781.1   sound speed (m/s)

#T_m     = 900.                              #magma temperature
#m_g     = 0.03                              #mass fraction gas
outfile = "../input_files/fullSweep/input.txt"    #name of output file
#rho_mix = 1.998                             #density of erupting mixture
#rho_mix = 1.998                             #density of erupting mixture
# m_w     = 0.20                              #mass fraction water added

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

## Write out table header
f = open(outfile, "w")
#f.write('INPUT VALUES USED IN HTHH PLUMERIA RUNS. T=%5.1f, m_w=%4.2f, m_g=%4.2f, rho_mix=%5.3f' \
#           % T_m, m_w, m_g, rho_mix)
#f.write('INPUT VALUES USED IN HTHH PLUMERIA RUNS. T={:5.1f}, m_w={:4.2f}, m_g={:4.2f}, rho_mix={:5.3f}\n'.format( \
#           T_m, m_w, m_g, rho_mix))
#print('INPUT VALUES USED IN HTHH PLUMERIA RUNS. T={:5.1f}, m_w={:4.2f}, m_g={:4.2f}, rho_mix={:5.3f}'.format( \
#           T_m, m_w, m_g, rho_mix))

#Write out results
#        0        10        20        30        40        50        60        70
#        12345678901234567890123456789012345678901234567890123456789012345678901234567890
f.write('run #         MER         diam     u_exit     T_m     m_w     m_g     rho_mix\n')
f.write('             kg/s           m        m/s       C                        kg/m3\n')
print(   'run #         MER         diam     u_exit     T_m     m_w     m_g     rho_mix')
print(   '             kg/s           m        m/s       C                        kg/m3')
for irun in range(0,nruns-1):
    f.write('{:5d}   {:12.4e}{:10.0f}{:11.1f}    {:4.0f}    {:4.2f}    {:4.2f}      {:5.3f}\n'. \
            format(irun+1,MER[irun],d_vent[irun],u_exit[irun],T_m[irun] - 273.15, m_w[irun],m_g[irun],rho_mix[irun]))
    print( '{:5d}   {:12.4e}{:10.0f}{:11.1f}    {:4.0f}    {:4.2f}    {:4.2f}      {:5.3f}'. \
            format(irun+1,MER[irun],d_vent[irun],u_exit[irun],T_m[irun] - 273.15,m_w[irun],m_g[irun],rho_mix[irun]))
    #    print('%5d   %12.4e%10.0f%11.1f    %4.0f    %4.2f    %4.2f   %5.3f' \
    #           % (irun+1,MER[irun],d_vent[irun],u_exit[irun],T_m,m_w,m_g,rho_mix)
f.close()

