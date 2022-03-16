# Gnuplot script to plot plume height as a function of MER for different water
# contents

set terminal pngcairo enhanced

set output '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/fullSweep5000/fullSweep5000.png'

unset key

set xrange [1e5:1e11]
set yrange [0:*]
set cbrange [0:0.2]

set xlabel 'Solid MER /kg s^{-1}'
set ylabel 'Plume height /km'
set cblabel 'Water mass fraction'

set xtics("10^{5}" 1e5, "10^{6}" 1e6, "10^{7}" 1e7, "10^{8}" 1e8, "10^{9}" 1e9, "10^{10}" 1e10, "10^{11}" 1e11)

set logscale x

set palette

plot '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/fullSweep5000/summary_table/summary_table.txt' every ::2 u 10:11:5 w p lc palette notitle  



set output '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/fullSweep5000/NBL.png'

set ylabel 'NBL height /km'

plot '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/fullSweep5000/summary_table/summary_table.txt' every ::2 u 10:12:5 w p lc palette notitle  


set output '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/fullSweep5000/volFlux.png'

set ylabel 'Volume flux at NBL /m^{3} s^{-1}'

set logscale y

set yrange [1e7:1e13]

set ytics("10^{7}" 1e7, "10^{8}" 1e8, "10^{9}" 1e9, "10^{10}" 1e10, "10^{11}" 1e11, "10^{12}" 1e12, "10^{13}" 1e13)

set arrow from 1e5, 5e11 to 1e11, 5e11 nohead dt 2 lc 7 lw 2

set arrow from 10**9.4, 1e7 to 10**9.4, 1e13 nohead dt 2 lc 6 lw 2

set arrow from 10**10.4, 1e7 to 10**10.4, 1e13 nohead dt 2 lc 6 lw 2

set label '5 X 10^{11} m^{3} s^{-1}' at 1e6, 7e11 textcolor rgb "red"

set label '10^{9.4}'  at 10**8.8, 1e9 textcolor rgb "blue"
set label '10^{10.4}' at 10**9.7, 1e9 textcolor rgb "blue"

plot '/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/run_output/fullSweep5000/summary_table/summary_table.txt' every ::2 u 10:13:5 w p lc palette notitle  
