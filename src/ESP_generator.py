#Script that generates ESP's for MCMC simulations

import sys
import numpy as np
import datetime
import math

## Inputs
pi                  = 3.14159               #pi
nruns               = 501                   #number of runs to set parameters for (actually needs to be nruns +1)
vent_elevation      = 144                 #vent elevation, km - CMT FROM PAUL: I THINK THIS IS M ACTUALLY - although this isn't actually used
logMER_min          = 5.5                    #minimum log MER (kg/s)
logMER_max          = 10.5                  #maximum log MER (kg/s)
u_min               = 100.0                  #minimum ejection velocity (m/s)
u_max               = 350.0                  #maximum ejection velocity (m/s)

#Parameters that need to change if we're adjusting mass fraction water
#Use this guide for the density of erupting mixture, assuming T=900 C, m_g=0.03, vent elevation=144 m
#m_w     0    0.05     0.1    0.20       m_w
#    5.948   2.774   2.108   1.998       rho_mix (kg/m3) - Should the first number be 2.948
#    144.0   210.9   241.9   248.5       sound speed (m/s)
#. . .  assuming T=900 C, m_w=0.00, vent elevation=144 m
#m_g  0.03    0.10    0.20    0.50    0.70    0.90    m_g
#    5.948   1.814   0.909   0.364    0.260   0.202   rho_mix (kg/m3)
#    144.0   260.8   368.5   582.2    688.8   781.1   sound speed (m/s)

T_m     = 900.                              #magma temperature
m_g     = 0.03                              #mass fraction gas
outfile = "../input_files/H20/0_20.txt"    #name of output file
#rho_mix = 1.998                             #density of erupting mixture
rho_mix = 1.998                             #density of erupting mixture
m_w     = 0.20                              #mass fraction water added

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
f.write('INPUT VALUES USED IN HTHH PLUMERIA RUNS. T={:5.1f}, m_w={:4.2f}, m_g={:4.2f}, rho_mix={:5.3f}\n'.format( \
           T_m, m_w, m_g, rho_mix))
print('INPUT VALUES USED IN HTHH PLUMERIA RUNS. T={:5.1f}, m_w={:4.2f}, m_g={:4.2f}, rho_mix={:5.3f}'.format( \
           T_m, m_w, m_g, rho_mix))

#Write out results
#        0        10        20        30        40        50        60        70
#        12345678901234567890123456789012345678901234567890123456789012345678901234567890
f.write('run #         MER         diam     u_exit     T_m     m_w     m_g     rho_mix\n')
f.write('             kg/s           m        m/s       C                        kg/m3\n')
print(   'run #         MER         diam     u_exit     T_m     m_w     m_g     rho_mix')
print(   '             kg/s           m        m/s       C                        kg/m3')
for irun in range(0,nruns-1):
    f.write('{:5d}   {:12.4e}{:10.0f}{:11.1f}    {:4.0f}    {:4.2f}    {:4.2f}      {:5.3f}\n'. \
            format(irun+1,MER[irun],d_vent[irun],u_exit[irun],T_m,m_w,m_g,rho_mix))
    print( '{:5d}   {:12.4e}{:10.0f}{:11.1f}    {:4.0f}    {:4.2f}    {:4.2f}      {:5.3f}'. \
            format(irun+1,MER[irun],d_vent[irun],u_exit[irun],T_m,m_w,m_g,rho_mix))
    #    print('%5d   %12.4e%10.0f%11.1f    %4.0f    %4.2f    %4.2f   %5.3f' \
    #           % (irun+1,MER[irun],d_vent[irun],u_exit[irun],T_m,m_w,m_g,rho_mix)
f.close()

