# Gnuplot script to plot plume height as a function of MER for different water
# contents

set terminal pngcairo enhanced

set output '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/H20/H20.png'

unset key

set xrange [1e5:1e11]
set yrange [0:60]

set xlabel 'Solid MER /kg s^{-1}'
set ylabel 'Plume height /km'

set xtics("10^{5}" 1e5, "10^{6}" 1e6, "10^{7}" 1e7, "10^{8}" 1e8, "10^{9}" 1e9, "10^{10}" 1e10, "10^{11}" 1e11)

set logscale x

set key top left title 'Initial water fraction'

plot '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/H20/0/summary_table/summary_table.txt'    every ::2 u 10:11 w p title '0.00' ,\
     '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/H20/0_05/summary_table/summary_table.txt' every ::2 u 10:11 w p title '0.05' ,\
     '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/H20/0_10/summary_table/summary_table.txt' every ::2 u 10:11 w p title '0.10' ,\
     '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/H20/0_20/summary_table/summary_table.txt' every ::2 u 10:11 w p title '0.20'  
