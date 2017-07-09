import sys
import os
import numpy as np
import time
import glob
from math import factorial
import matplotlib.pyplot as plt

# ==============================================================================
#                             USER INPUTS HERE

N_SAMPLES = 500
FLOW_MEAN = -100
FLOW_STD = 10
RES_MEAN = 1200
RES_STD = 240

MESHCOMPLETE_PATH = '../../mesh-complete'
SVPRE_PATH = '/home/marsden/Desktop/2_17_15_simvascular/svSolver/BuildWithMake/Bin/svpre.exe'

# ==============================================================================

def generateFlowFile(flow_val):
  
  flow_file = open('cylinder_flow.flow', 'w')
  
  write_string = '0.0 ' + str(flow_val) + '\n'
  flow_file.write(write_string)
  write_string = '1.0 ' + str(flow_val) + '\n'
  flow_file.write(write_string)
  
  flow_file.close()

# ==============================================================================

def generateSvpre():
  svpre_file = open('cylinder_sim.svpre', 'w')
  
  # Read in the mesh files
  write_string = 'mesh_and_adjncy_vtu ' + MESHCOMPLETE_PATH + '/mesh-complete.mesh.vtu\n\n'
  svpre_file.write(write_string)
  
  # Set surface IDs
  write_string = 'set_surface_id_vtp ' + MESHCOMPLETE_PATH + '/mesh-complete.exterior.vtp 1\n'
  svpre_file.write(write_string)
  write_string = 'set_surface_id_vtp ' + MESHCOMPLETE_PATH + '/mesh-surfaces/cap_cylinder_group.vtp 2\n'
  svpre_file.write(write_string)
  write_string = 'set_surface_id_vtp ' + MESHCOMPLETE_PATH + '/mesh-surfaces/cap_cylinder_group_2.vtp 3\n\n'
  svpre_file.write(write_string)
  
  # Set properties for a plug inflow with the flow value
  write_string = 'fluid_density 1.06\n'
  svpre_file.write(write_string)
  write_string = 'fluid_viscosity 0.04\n'
  svpre_file.write(write_string)
  write_string = 'initial_pressure 0\n'
  svpre_file.write(write_string)
  write_string = 'prescribed_velocities_vtp ' + MESHCOMPLETE_PATH + '/mesh-surfaces/cap_cylinder_group.vtp\n'
  svpre_file.write(write_string)
  write_string = 'bct_analytical_shape plug\n'
  svpre_file.write(write_string)
  write_string = 'bct_period 1.0\n'
  svpre_file.write(write_string)
  write_string = 'bct_point_number 201\n'
  svpre_file.write(write_string)
  write_string = 'bct_fourier_mode_number 10\n'
  svpre_file.write(write_string)
  write_string = 'bct_create ' + MESHCOMPLETE_PATH + '/mesh-surfaces/cap_cylinder_group.vtp cylinder_flow.flow\n'
  svpre_file.write(write_string)
  write_string = 'bct_write_dat bct.dat\n'
  svpre_file.write(write_string)
  write_string = 'bct_write_vtp bct.vtp\n\n'
  svpre_file.write(write_string)
  
  # Assign Neumann outlet boundary condition
  write_string = 'pressure_vtp ' + MESHCOMPLETE_PATH + '/mesh-surfaces/cap_cylinder_group_2.vtp 0\n\n'
  svpre_file.write(write_string)
  
  # Assign no slip to the walls
  write_string = 'noslip_vtp ' + MESHCOMPLETE_PATH + '/walls_combined.vtp\n\n'
  svpre_file.write(write_string)
  
  # Write out the solver files
  write_string = 'write_geombc geombc.dat.1\n'
  svpre_file.write(write_string)
  write_string = 'write_restart restart.0.1\n'
  svpre_file.write(write_string)
  
  svpre_file.close()
  
# ==============================================================================

def generateSolverInp(res_val):
  solver_file = open('solver.inp', 'w')
  
  write_string = 'Density: 1.06\n'
  solver_file.write(write_string)
  write_string = 'Viscosity: 0.04\n\n'
  solver_file.write(write_string)
  
  write_string = 'Number of Timesteps: 50\n'
  solver_file.write(write_string)
  write_string = 'Time Step Size: 0.01\n\n'
  solver_file.write(write_string)
  
  write_string = 'Number of Timesteps between Restarts: 50\n'
  solver_file.write(write_string)
  write_string = 'Number of Force Surfaces: 1\n'
  solver_file.write(write_string)
  write_string = "Surface ID's for Force Calculation: 1\n"
  solver_file.write(write_string)
  write_string = 'Force Calculation Method: Velocity Based\n'
  solver_file.write(write_string)
  write_string = 'Print Average Solution: True\n'
  solver_file.write(write_string)
  write_string = 'Print Error Indicators: False\n\n'
  solver_file.write(write_string)
  
  write_string = 'Time Varying Boundary Conditions From File: True\n\n'
  solver_file.write(write_string)
  
  write_string = 'Step Construction: 0 1 0 1 0 1 0 1 0 1\n\n'
  solver_file.write(write_string)
  
  write_string = 'Number of Resistance Surfaces: 1\n'
  solver_file.write(write_string)
  write_string = 'List of Resistance Surfaces: 3\n'
  solver_file.write(write_string)
  write_string = 'Resistance Values: ' + str(res_val) + '\n\n'
  solver_file.write(write_string)
  
  write_string = 'Pressure Coupling: Implicit\n'
  solver_file.write(write_string)
  write_string = 'Number of Coupled Surfaces: 1\n\n'
  solver_file.write(write_string)
  
  write_string = 'Backflow Stabilization Coefficient: 0.2\n'
  solver_file.write(write_string)
  write_string = 'Residual Control: True\n'
  solver_file.write(write_string)
  write_string = 'Residual Criteria: 0.01\n'
  solver_file.write(write_string)
  write_string = 'Minimum Required Iterations: 3\n'
  solver_file.write(write_string)
  write_string = 'svLS Type: NS\n'
  solver_file.write(write_string)
  write_string = 'Number of Krylov Vectors per GMRES Sweep: 100\n'
  solver_file.write(write_string)
  write_string = 'Number of Solves per Left-hand-side Formation: 1\n'
  solver_file.write(write_string)
  write_string = 'Tolerance on Momentum Equations: 0.05\n'
  solver_file.write(write_string)
  write_string = 'Tolerance on Continuity Equations: 0.05\n'
  solver_file.write(write_string)
  write_string = 'Tolerance on svLS NS Solver: 0.05\n'
  solver_file.write(write_string)
  write_string = 'Maximum Number of Iterations for svLS NS Solver: 10\n'
  solver_file.write(write_string)
  write_string = 'Maximum Number of Iterations for svLS Momentum Loop: 2\n'
  solver_file.write(write_string)
  write_string = 'Maximum Number of Iterations for svLS Continuity Loop: 400\n'
  solver_file.write(write_string)
  write_string = 'Time Integration Rule: Second Order\n'
  solver_file.write(write_string)
  write_string = 'Time Integration Rho Infinity: 0.5\n'
  solver_file.write(write_string)
  write_string = 'Flow Advection Form: Convective\n'
  solver_file.write(write_string)
  write_string = 'Quadrature Rule on Interior: 2\n'
  solver_file.write(write_string)
  write_string = 'Quadrature Rule on Boundary: 3\n'
  solver_file.write(write_string)
  
  solver_file.close()
  
# ==============================================================================

if __name__ == "__main__":
  
  # Make a separate folder to hold the UQ trials
  command_string = 'mkdir -p cylinder_sim_trials'
  print(command_string)
  os.system(command_string)
  command_string = 'cd cylinder_sim_trials'
  print(command_string)
  os.chdir('cylinder_sim_trials')
  
  flow_vals = np.zeros(N_SAMPLES)
  res_vals = np.zeros(N_SAMPLES)
  
  for i_trial in xrange(0, N_SAMPLES):
  
    # Make a directory for each of the cylinder simulations we will run
    command_string = 'mkdir -p trial_' + str(i_trial)
    print(command_string)
    os.system(command_string)
    command_string = 'cd trial_' + str(i_trial)
    print(command_string)
    os.chdir('trial_' + str(i_trial))
    
    # Sample the inflow value and outlet pressure from Gaussian distributions
    sampled_flow = FLOW_STD*np.random.randn() + FLOW_MEAN
    sampled_res = RES_STD*np.random.randn() + RES_MEAN
    
    # We only want negative values of flow and positive values of resistance
    while(sampled_flow > 0):
      sampled_flow = FLOW_STD*np.random.rand() + FLOW_MEAN
    while(sampled_res < 0):
      sampled_res = RES_STD*np.random.randn() + RES_MEAN
  
    # Save the sampled flow and resistance
    flow_vals[i_trial] = sampled_flow
    res_vals[i_trial] = sampled_res
    
    # Create the pre-solver files needed for the pre-solver
    generateFlowFile(sampled_flow)
    generateSvpre()
    generateSolverInp(sampled_res)
    
    # Run pre-solver
    command_string = SVPRE_PATH + ' cylinder_sim.svpre'
    print(command_string)
    os.system(command_string)
    
    # Create numstart.dat
    numstart_file = open('numstart.dat', 'w')
    numstart_file.write('0')
    numstart_file.close()
    
    # Done with this trial, move back up one
    command_string = 'cd ../'
    print(command_string)
    os.chdir('../')
    
  # Save the sampled inputs to file
  command_string = 'cd ../'
  print(command_string)
  os.chdir('../')
  
  inputs_file = open('sampledInputs.txt', 'w')
  
  for i_input in xrange(0, N_SAMPLES):
    write_string = str(flow_vals[i_input]) + ' ' + str(res_vals[i_input]) + '\n'
    inputs_file.write(write_string)
  
  inputs_file.close()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
# ==============================================================================
