import sys
import os
import numpy as np
import time
import glob
from math import factorial
import matplotlib.pyplot as plt

# ==============================================================================
#                             USER INPUTS HERE

N_CORES = 6
SVSOLVER_PATH = '~/Desktop/2_17_15_simvascular/svSolver/BuildWithMake/Bin/svsolver-nompi.exe'

# ==============================================================================

if __name__ == '__main__':

  # Change into the trials folder
  command_string = 'cd cylinder_sim_trials'
  print(command_string)
  os.chdir('cylinder_sim_trials')
  
  # Get the number of trials that we have to run
  trial_list = glob.glob('trial_*')
  num_trials = len(trial_list)
  
  to_do_list = range(0, num_trials)
  running_list = []
  completed_list = []
  
  while(len(to_do_list) > 0):
  
    # Start new jobs
    while(len(running_list) < N_CORES):
    
      run_index = to_do_list.pop(0)
      running_list.append(run_index)
      
      command_string = 'cd trial_' + str(run_index)
      print(command_string)
      os.chdir('trial_' + str(run_index))
      
      # Start the flowsolver
      command_string = SVSOLVER_PATH + ' & > solver_out.txt'
      print(command_string)
      os.system(command_string)
      
      # Move out of this folder
      command_string = 'cd ../'
      print(command_string)
      os.chdir('../')
    
    # Check status of running jobs
    to_remove = []
    count = 0
    for i_run in running_list:
    
      command_string = 'cd trial_' + str(i_run)
      print(command_string)
      os.chdir('trial_' + str(i_run))
      
      # Check the numstart.dat file to check job status
      numstart = open('numstart.dat', 'r')
      last_step = int(numstart.readline())
      if(last_step == 50):
        to_remove.append(count)
      numstart.close()
      
      count = count+1
      
      command_string = 'cd ../'
      print(command_string)
      os.chdir('../')
      
    # Remove completed jobs from the running list
    for i_remove in reversed(to_remove):
      completed_index = running_list.pop(i_remove)
      completed_list.append(completed_index)
      
    # Sleep for a minute
    time.sleep(60)









































































