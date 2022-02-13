      program MakeInput

!program that makes an input file for each model run

      implicit none
      real*8             :: MER, diam, u_exit, T_m, m_g, m_w, rho_mix
      integer            :: nargs, irun, intRunNumber, inum
      character(len=5)   :: RunNumber
      character(len=78)  :: inputline
      character(len=80)  :: outfile

      !some constants

      !read run number
      nargs=iargc()
      if (nargs.ne.1) then
         write(6,*) 'error in MakeInput.  You must provide an input argument giving the run number.'
         write(6,*) 'Program stopped'
        else
         call getarg(1,RunNumber)
      end if
      read(RunNumber,*) intRunNumber             !convert to integer

      !read input file to get date and time
      open(unit=12, &
           file='/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria/scripts/input_files/fullSweep/input.txt', &
                  action='read')
      read(12,*)                                    !skip the first three lines
      read(12,*)
      do inum=1,intRunNumber                        !Now, skip down to the appropriate run number line
         read(12,*)
      end do
      read(12,'(a78)') inputline
      read(inputline,*)  irun, MER, diam, u_exit, T_m, m_w, m_g, rho_mix

     !Write output (for testing)
!     write(6,10) intRunNumber, irun, MER, diam, u_exit, T_m, m_w, m_g, rho_mix
!10   format( 'intRunNumber=',i5,/, &
!             '        irun=',i5,/, &
!             '         MER=',e12.4,' kg/s',/, &
!             '        diam=',f6.1,' m',/, &
!             '      u_exit=',f6.1,' m/s',/, &
!             '         T_m=',f6.1,' C',/, &
!             '         m_w=',f4.2,/, &
!             '         m_g=',f4.2,/, &
!             '     rho_mix=',f6.3,' kg/m3')

      !Write input file
      print *,T_m

      !Write inputs to screen
      write(6,2)  irun, MER, diam, u_exit, m_w, m_g, T_m
2     format(i5,e12.4,f8.1,f8.2,f8.2,f8.2,f8.1)

      open(unit=10,file='input_HTHH.inp',action='write')
      write(10,1) diam, u_exit, m_w, T_m, m_g

1     format('#  Input file for the Fortran version of Plumeria.',/, &
             '#  Lines that begin with a # are comment lines.',/, &
             '#',/, &
             '#  Output file name',/, &
             'output_file.txt',/, &
             '#',/, &
             '#  Information on whether to read met. input file.',/, &
             '#  The first line should supply a "yes" or "no".  If that line is "yes", the next line',/, &
             '#  should be the name of the input file used.',/, &
             'yes',/, &
             'metfile.txt',/, &
             '#',/, &
             '#  Tropospheric properties (used only if no atmospheric file is used)',/, &
             '#',/, &
             '0.                   #Air temperature at vent, Celsius.',/, &
             '100.                 #Air relative humidity',/, &
             '-0.0065              #thermal lapse rate in troposphere (K/m upward--should be negative)',/, &
             '11000.               #Elevation of tropopause (m asl)',/, &
             '9000.                #Tropopause thickness, m',/, &
             '0.001                #thermal lapse rate above tropopause (K/m--should be positive)',/, &
             '0.00   90.0          #wind speed, m/s, direction (deg. CW from N)',/, &
             '#',/, &
             '#  Vent properties',/, &
             '#',/, &
             '144.0                #Vent elevation (m asl)',/, &
             f8.1,'             #vent diameter (m)',/, &
             f5.1,'                #exit velocity (m/s)',/, &
             f4.2,'                 #mass fraction added water',/, &
             '#',/, &
             '#   Magma properties',/, &
             '#',/, &
             f8.1,'                 #magma temperature',/, &
             f4.2,'                 #mass fraction gas in magma',/, &
             '1000.                #magma specific heat, J/kg K',/, &
             '2500.                #magma density (DRE), kg/m3')

      end program
