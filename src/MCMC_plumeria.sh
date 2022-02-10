#!/bin/bash

#MCMC driver: a script that drives a series of plumeria simulations for Monte Carlo analysis

#This script runs jobs in parallel on up to multiple processors and then combines the results afterwards.

###THINGS TO CHECK BEFORE STARTING A RUN
#1)  ESP_generator.py has correct density and m_w or m_g
#2)  ESP_generator.py has been run and input list is in "input_files" directory.
#3)  MakeInput is reading from correct input table
#4)  MakeInput is compiled and tested
#5)  OUTFILEDIR is correctly set
#6)  readme.txt comments are correct for this run (lines 97-98)
#7)  RunStartNumber is okay
#8)  dirmax and cyclemax are all okay
#9)  "run" command is set to output log file.
#10)  Outputs from sample run are being correctly written to the correct output directories:
#	${OUTPUTDIR}/output_files
#  	${OUTPUTDIR}/run_logs
#	${OUTPUTDIR}/summary_table

#####STARTING VALUE FOR RUNS
#Total number of runs performed = dirmax*(cyclemax+1)
#Runs are numbered from RunStartNumber to (RunStartNumber + dirmax*(cyclemax+1))
RunStartNumber=1     #Run number for first run in the series
dirmax=20            #Number of simultaneous runs (1 to 50)
cyclemax=9           #Number of cycles (0 to ????)

#####Directories of programs and utilities

PLUMEPROG="/home/paulj/Documents/tonga2022/plumeModeling/plumeria_wd/plume_wd"       #name and location of plumeria executable
MAINDIR="/home/paulj/Documents/tonga2022/plumeModeling/MCMC_plumeria"                     #name and location of other utility programs
METFILE="${MAINDIR}/scripts/input_files/gfs_sounding.txt"            #name and location of met. file
MAKEINPUTPROG="${MAINDIR}/scripts/src/MakeInput"                     #name and location of MakeInput file
OUTPUTREADER="${MAINDIR}/scripts/src/read_output.py"                 #name and location of python script that reads output
OUTFILENAME="output_file.txt"                                        #name of output file created by plumeria (must agree with
                                                                     #      the name given in the plumeria input file
LOGFILENAME="run_log.txt"                                            #name of log file, when plumeria is run in background

#####Run and Output directories
FileDate=`date "+%Y%b%d"`                                               #date, to be appended to file names
RUNDIRS=${MAINDIR}/RunDirs                  #location of directories where program will be run

## NOTE FROM PAUL - HAVE REPLACED COMMENTED LINES WITH EDITS BELOW
#OUTFILEDIR=${OUTPUTDIR}/output_files                                    #Name and location of subdirectories in ${OUTFILEDIR}
#OUTPUTDIR=${OUTFILEDIR}/H2O0.20_mg0.03     #location of output file directory
OUTPUTDIR=${MAINDIR}/run_output
OUTFILEDIR=${OUTPUTDIR}/output_files                                    #Name and location of subdirectories in ${OUTFILEDIR}

OUTLOGDIR=${OUTPUTDIR}/run_logs
SUMMARYTABLEDIR=${OUTPUTDIR}/summary_table
SUMMARYTABLE=${OUTPUTDIR}/summary_table/summary_table.txt

##############################################################################
###################VERIFY THAT KEY DIRECTORIES AND FILES EXIST ###############

#Make sure metfile exists
echo "Making sure the metfile exists at ${METFILE}"
if test -r ${METFILE}; then
    echo "   It does.  Good"
  else
    echo "   It does not.  Exiting"
    exit 1
fi

#Make sure MakeInput program exists
echo "Making sure the MakeInput program exists at ${MAKEINPUTPROG}"
if test -r ${MAKEINPUTPROG}; then
    echo "   It does.  Good"
  else
    echo "   It does not.  Exiting"
    exit 1
fi

#Make sure plumeria program exists
echo "Making sure the plumeria program exists at ${PLUMEPROG}"
if test -r ${PLUMEPROG}; then
    echo "   It does.  Good"
  else
    echo "   It does not.  Exiting"
    exit 1
fi

#See if the output directory exists.  If so, clean it out.  If not, create it.
if test -r ${OUTPUTDIR}; then                                                        #See if this directory exists
       echo "${OUTPUTDIR} exists.  Cleaning it."                                         #If so, clean it out.
       rm -f ${OUTFILEDIR}/Run*
       rm -f ${OUTLOGDIR}/Run*
       rm -f ${SUMMARYTABLEDIR}/*
    else
       echo "creating directory ${OUTPUTDIR} and its subdirectories"                      #If not, make it . . .
       mkdir ${OUTPUTDIR}                                                      #main directory with run output
       mkdir ${OUTFILEDIR}                                                     #subdirectory with plumeria output files
       mkdir ${OUTLOGDIR}                                                      #subdirectory with plumeria log files
       mkdir ${SUMMARYTABLEDIR}                                                #subdirectory with output summary table
fi
rm -f ${SUMMARYTABLEDIR}/*                                                     #remove all summary tables

#####################   Create new summary files  ################################
echo "creating new summary files"
#create summary log file
echo "SUMMARY OF INPUT VALUES USED IN PLUMERIA RUNS ON ${FileDate}" > ${SUMMARYTABLE}
#write table headers for input values
echo "setting up and running models"
echo "run #          MER        diam     u_exit    m_w    m_g    T_m   sound_speed   vent_elevation    mdot_solids    H_t        H_nbl     Vdot_nbl" >> ${SUMMARYTABLE}
echo "              kg/s          m        m/s                    C        m/s             m             kg/s          km         km         m3/s" >> ${SUMMARYTABLE}

####################   Create new readme.txt file #################################
echo "This folder gives output for Plumeria simulations" > ${OUTPUTDIR}/readme.txt
echo "using m_w=0.20, T_m=900 C, m_g=0.03" >> ${OUTPUTDIR}/readme.txt

#Check to see whether any files are missing

SECONDS=0                        #start time counter
t0=`date`                        #date, printed at end of run
date

#####################   Make the directories  ####################################
echo "making directories"
for (( idir=1;idir<=$dirmax;idir++ ))
do
   if [[ ${idir} -lt 10 ]]; then
      DirNumber="0${idir}"
    else
      DirNumber="${idir}"
   fi
   if test -r  ${RUNDIRS}/Dir${DirNumber}; then
         #echo "${RUNDIRS}/Dir${DirNumber} exists.  Cleaning"
         rm -f ${RUNDIRS}/Dir${DirNumber}/*
         cd    ${RUNDIRS}/Dir${DirNumber}
         ln -s ${METFILE} metfile.txt
      else
         #echo "creating ${RUNDIRS}/Dir${DirNumber}"
         mkdir ${RUNDIRS}/Dir${DirNumber}
         cd    ${RUNDIRS}/Dir${DirNumber}
         ln -s ${METFILE} metfile.txt
   fi
done

##############################################################################
#####################   Set up and run models  ####################################

for (( icycle=0;icycle<=$cyclemax;icycle++ )); do

   #write table headers for input values
   echo "setting up and running models"
   echo "run #     MER        diam     u_exit    m_w    m_g    T_m"
   echo "         kg/s          m        m/s                    C"

   #Start looping through directories
   for (( idir=1;idir<=$dirmax;idir++ )); do
         irun=`echo "$RunStartNumber - 1 + $icycle * $dirmax + $idir" | bc -l`
         #Make run numbers into five-digit numbers
         if [[ $irun -lt 10 ]]; then
            RunNumber="0000${irun}"
          elif [[ $irun -lt 100 ]]; then
            RunNumber="000${irun}"
          elif [[ $irun -lt 1000 ]]; then
            RunNumber="00${irun}"
          elif [[ $irun -lt 10000 ]]; then
            RunNumber="0${irun}"
          else
            RunNumber=${irun}
         fi
         #make dir names into three-digit numbers
         if [[ ${idir} -lt 10 ]]; then
            DirNumber="0${idir}"
          else
            DirNumber="${idir}"
         fi

         #move to the new directory
         cd ${RUNDIRS}/Dir${DirNumber}

         #remove old output files
         rm -f ${RUNDIRS}Dir${DirNumber}/*

         #make the new input file
         ${MAKEINPUTPROG} ${RunNumber}        

         #run the model
         #echo "running ${ASH3DDIR}/bin/Ash3d"
         #${PLUMEPROG} input_HTHH.inp
         ${PLUMEPROG} input_HTHH.inp > ${LOGFILENAME} 2>&1 &


   done
   echo "All done setting up and starting jobs. Waiting . . ."
   wait            #wait until background jobs have completed
   echo "Done waiting. Zipping and cleaning output"

   ##################################################################################
   #####################  Wrap up results and post them  ############################

   for (( idir=1;idir<=$dirmax;idir++ )); do
         irun=`echo "$RunStartNumber - 1 + $icycle * $dirmax + $idir" | bc -l`
         #Make run numbers into five-digit numbers
         if [[ $irun -lt 10 ]]; then
            RunNumber="0000${irun}"
          elif [[ $irun -lt 100 ]]; then
            RunNumber="000${irun}"
          elif [[ $irun -lt 1000 ]]; then
            RunNumber="00${irun}"
          elif [[ $irun -lt 10000 ]]; then
            RunNumber="0${irun}"
          else
            RunNumber=${irun}
         fi
         #make dir names into three-digit numbers
         if [[ ${idir} -lt 10 ]]; then
            DirNumber="0${idir}"
          else
            DirNumber="${idir}"
         fi
         #move to the new directory
         echo "     moving to ${RUNDIRS}/Dir${DirNumber}"
         cd ${RUNDIRS}/Dir${DirNumber}

         #read output and write to summary table
         echo "Reading output, writing to summary table"
         python ${OUTPUTREADER} ${RunNumber} ${SUMMARYTABLE}

         #move the log & output files
         cp -f ${LOGFILENAME} ${OUTLOGDIR}/Run${RunNumber}.txt
         cp -f ${OUTFILENAME} ${OUTFILEDIR}/Run${RunNumber}.txt

         echo "     all done with plumeria run ${RunNumber}"
   done
   t1=`date`
   echo "MCMC driver start time: $t0"
   echo "End time at this loop: $t1"
   duration=$SECONDS
   hours=$(($duration / 3600))
   minutes=$(($duration / 60 - 60 * $hours))
   minutes2=$(($duration / 60))
   seconds=$(($duration - 60 * minutes2))
   echo "total seconds = $SECONDS"
   echo "$hours hours, $minutes minutes and $seconds seconds elapsed."
done

t1=`date`
echo "MCMC driver start time: $t0"
echo "MCMC driver   end time: $t1"
duration=$SECONDS
hours=$(($duration / 3600))
minutes=$(($duration / 60 - 60 * $hours))
minutes2=$(($duration / 60))
seconds=$(($duration - 60 * minutes2))
echo "total seconds = $SECONDS"
echo "$hours hours, $minutes minutes and $seconds seconds elapsed."
echo "all done with MCMC simulations"

