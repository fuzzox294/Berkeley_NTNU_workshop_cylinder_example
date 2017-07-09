import sys
import os
import numpy as np
import time
import glob
import vtk

# ==============================================================================
#                             USER INPUTS

SVPOST_PATH = '/home/marsden/Desktop/2_17_15_simvascular/svSolver/BuildWithMake/Bin/svpost.exe'
MESHCOMPLETE_PATH = '../../mesh-complete'

# ==============================================================================

if __name__ == '__main__':

  # Change into the trials folder
  command_string = 'cd cylinder_sim_trials'
  print(command_string)
  os.chdir('cylinder_sim_trials')
  
  # Get the list of trial folders and the number of trials
  trial_list = glob.glob('trial_*')
  num_trials = len(trial_list)

  # The quantities of interest we will consider in this example are:
  #  1. Average pressure across the outlet face
  #  2. Maximum velocity at the outlet face
  average_outlet_pressure = np.zeros(num_trials)
  maximum_outlet_velocity = np.zeros(num_trials)
  
  # Change into each run directory and call the SimVascular postsolver to
  # generate VTK files for the results
  for i_trial in xrange(0, num_trials):
  
    trial_folder = 'trial_' + str(i_trial)
    command_string = 'cd ' + trial_folder
    print(command_string)
    os.chdir(trial_folder)
    
    command_string = SVPOST_PATH + ' -sn 50 -vtu all_results.vtu -vtp all_results.vtp ' \
                                   + '-vtkcombo -all'
    print(command_string)
    os.system(command_string)
    
    # Now that we have the all_results file, we can process it to find out
    # output quantities of interest. We want to find quantities on the outlet
    # face, so let's first isolate this part of the model by finding the
    # nodes that belong on this face:
    all_results_reader = vtk.vtkXMLPolyDataReader()
    all_results_reader.SetFileName('all_results.vtp')
    all_results_reader.Update()
    all_results_model = vtk.vtkPolyData()
    all_results_model = all_results_reader.GetOutput()
    all_results_numPts = all_results_model.GetNumberOfPoints()
    all_results_nodeID = all_results_model.GetPointData().GetArray("GlobalNodeID")
    
    # Get the velocity and pressure arrays from the all_results
    pressure_result = vtk.vtkDoubleArray()
    pressure_result = all_results_model.GetPointData().GetArray('pressure_00050')
    velocity_result = vtk.vtkDoubleArray()
    velocity_result = all_results_model.GetPointData().GetArray('velocity_00050')
    
    # Since we are looking at quantities on the outlet face, load up the .vtp
    # file defining the outlet face from the mesh files and store the GlobalNodeID
    # of all the nodes on this outlet face
    outlet_face_path = MESHCOMPLETE_PATH + '/mesh-surfaces/cap_cylinder_group_2.vtp'
    outlet_reader = vtk.vtkXMLPolyDataReader()
    outlet_reader.SetFileName(outlet_face_path)
    outlet_reader.Update()
    outlet_face = vtk.vtkPolyData()
    outlet_face = outlet_reader.GetOutput()
    outlet_numPts = outlet_face.GetNumberOfPoints()
    outlet_nodeID = outlet_face.GetPointData().GetArray('GlobalNodeID')
  
    # We want to save out velocity and pressure on the outlet face of this
    # cylinder simulation. Allocate space for them here
    pressure_out = vtk.vtkDoubleArray()
    pressure_out.SetNumberOfComponents(1)
    pressure_out.Allocate(outlet_numPts,10000)
    pressure_out.SetNumberOfTuples(outlet_numPts)
    pressure_out.SetName('pressure')
  
    velocity_out = vtk.vtkDoubleArray()
    velocity_out.SetNumberOfComponents(3)
    velocity_out.Allocate(outlet_numPts,10000)
    velocity_out.SetNumberOfTuples(outlet_numPts)
    velocity_out.SetName('velocity')
    
    # Loop over the points on the outlet face and find the matching nodes
    # on the all_results
    for i_out in xrange(0, outlet_numPts):
      tempID = outlet_nodeID.GetTuple1(i_out)
      for i_result in xrange(0, all_results_numPts):
        if(not(tempID == all_results_nodeID.GetTuple1(i_result))):
          continue
        temp_pressure = pressure_result.GetTuple1(i_result)
        temp_velocity = velocity_result.GetTuple3(i_result)
        
        pressure_out.SetTuple1(i_out, temp_pressure)
        velocity_out.SetTuple3(i_out, temp_velocity[0], temp_velocity[1], temp_velocity[2])
        
    # Add these arrays to the outlet face, and write out the model
    outlet_face.GetPointData().AddArray(pressure_out)
    outlet_face.GetPointData().AddArray(velocity_out)
    outlet_writer = vtk.vtkXMLPolyDataWriter()
    outlet_writer.SetInputData(outlet_face)
    outlet_writer.SetFileName('outlet_results.vtp')
    outlet_writer.Write()
    
    # Now that we have the velocities and pressures on the outlet face, perform
    # additional post processing to get the values that we want
    
    # Integrate the pressures over the area of the outlet face, then divide by
    # the total area to get the average pressure
    numCells = outlet_face.GetNumberOfCells()
    pressure_avg = 0.0
    total_area = 0.0
    for i_cell in xrange(0, numCells):
      # Extract a cell from this outlet face
      temp_cell = outlet_face.GetCell(i_cell)
      pts_cell = temp_cell.GetPointIds()
      
      # First, get the area of this cell
      vtkpt = temp_cell.GetPoints()
      p0 = vtkpt.GetPoint(0)
      p1 = vtkpt.GetPoint(1)
      p2 = vtkpt.GetPoint(2)
      temp_area = temp_cell.TriangleArea(p0, p1, p2)
      total_area = total_area + temp_area
      
      # Now sum up the pressures at the cell vertices
      temp_press = 0.0
      for ipt in xrange(0, pts_cell.GetNumberOfIds()):
        iid = pts_cell.GetId(ipt)
        temp_press = temp_press + float(pressure_out.GetTuple(iid)[0])
        
      # To complete the trapezoidal rule integration, multiply the summed pressures
      # by the area of the cell then divide by the number of vertices
      pressure_avg = pressure_avg + temp_press*temp_area/3.0
    
    average_outlet_pressure[i_trial] = pressure_avg/total_area
    
    # Find the maximum velocity magnitude on this outlet face
    max_vel_mag = 0.0
    for i_node in xrange(0, outlet_numPts):
      temp_vel = velocity_out.GetTuple3(i_node)
      temp_mag = np.sqrt(temp_vel[0]*temp_vel[0] + \
                         temp_vel[1]*temp_vel[1] + \
                         temp_vel[2]*temp_vel[2])
      max_vel_mag = max(max_vel_mag, temp_mag)
    
    maximum_outlet_velocity[i_trial] = max_vel_mag
    
    # Exit this trial directory
    command_string = 'cd ../'
    print(command_string)
    os.chdir('../')
    
  # Return to the top directory
  command_string = 'cd ../'
  print(command_string)
  os.chdir('../')
    
  # Write out the results to file
  output_file = open('cylinderResults.txt', 'w')
  
  for i_trial in xrange(0, num_trials):
    write_string = str(average_outlet_pressure[i_trial]) + ' ' + str(maximum_outlet_velocity[i_trial]) + '\n'
    output_file.write(write_string)
  
  output_file.close()
    
  
# ==============================================================================




















































