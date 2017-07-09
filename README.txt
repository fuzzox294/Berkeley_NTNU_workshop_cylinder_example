This document will explain how to run a simple uncertainty quantification
analysis on a cylinder geometry using SimVascular to run the simulations
and tulip to perform the forward propagation. The idea behind this tutorial
is to give you an example on how to interface UQ tools with an existing solver
to perform uncertainty quantification analysis.

Pre-requisites for running this tutorial:
  1. SimVascular flowsolver
  2. Python VTK (for post-processing)
  3. tulip UQ library (for forward propagation)

We simulate just steady flow through a cylinder with a resistance outlet.
Our uncertain inputs are therefore the inflow value and the value of the
outlet resistance. These will be sampled with Gaussin distributions. We will
then propagate these uncertainties forward to compute the statistics on
two quantities of interest that are relevant for cardiovascular simulations:
the average pressure at the outlet face and the maximum velocity at the outlet
face.

We have already generated the computational mesh for you in the "mesh-complete" 
folder. This is typically what you will get when you create a computational 
model in SimVascular. With this mesh, we now have to execute the SimVascular
pre-solver to generate the files that the flowsolver will need. This process
has been automated for you in the script "cylinder_presolve.py" script. If you
open this file, you will notice that there is a block for inputs at the top.
You will need to specify:

1. N_SAMPLES - Number of samples to run for the UQ analysis
2. FLOW_MEAN - Mean value of the inflow
3. FLOW_STD - Standard deviation of the inflow value
4. RES_MEAN - Mean value of the outlet resistance
5. RES_STD - Standard deviation of the outlet resistance

The default values for these parameters have been chosen to mimic typically
conditions in the descending aorta.

The next thing you will have to set is the path for the SimVascular pre-solver:

SVPRE_PATH

This will depend on where you have SimVascular installed on your system. If you
make minimal modifications to the file structure, you will not have to change the
MESHCOMPELTE_PATH.

Once you have set all the inputs, save and close the "cylinder_presolve.py" file
and run this command from the terminal:

python cylinder_presolve.py

This will generate inflow values and outlet resistances for all of the samples
that we will consider, and run the SimVascular pre-solver on all the cases.
The simulation files will be saved in the folder: "cylinder_sim_trials"

Once the pre-solve is done, you will now need to run the simulations. We have
provided a script called "launch_sim_jobs.py" that will do this automatically
for you. If you open this file, you will notice there are 2 inputs you must
specify:

1. N_CORES - Number of cores you want to use to run simulations. It is
             recommended you specify a number of cores close to the amount
             of cores you have on your computer, but leave a couple leftover
             so you can still do stuff.
2. SVSOLVER_PATH - Path to the SimVascular flowsolver

Once these are set, save and close the script and run it in the terminal using:

python launch_sim_jobs.py

This will launch the simulation jobs on your computer. It will take a while to
run all these jobs depending on your workstation, so now would be a good time
to take a break and do chores! For reference, with 6 cores it took me ~4 hours
to complete 500 simulations.

NOTE: This example was designed to run on typical lab computers. On more realstic
cases with a larger mesh, it is highly recommended to run these simulations
on a large computer cluster. If you are doing so, then you will need to modify
this script to automatically launch the simulation jobs on your cluster

Once the simulations are done, we need to post-process the jobs to generate
the results we need. This involves calling the SimVascular postsolver to
generate VTK format output files and performing additional postprocessing
with VTK routines to get the quantities of interest we are looking for.

These steps have been automated for you in the script "cylinder_postsolve.py".
You will need to open this file and set the path for the SimVascular postsolver,
but besides that the script should be ready to go. Once you have set that path,
run it in the terminal using:

python cylinder_postsolve.py

This will generate a file called "cylinderResults.txt" that has the average
outlet pressure and maximum outlet velocity for all the trials that you ran.

Now that we have generated our results, we need to propagate them forward.
In this tutorial, we use the tulip library to do this. We have prepared a script
which calls the relevant functions in tulip to perform this task. More information
on the various options in tulip can be found in the official documentation.
The only line you will have to pay attention to is line 37, where you specify
the index of the output we want to examine. Set this to 0 to compute the 
uncertainties on the outlet pressure, and 1 to compute the uncertainties on
the maximum velocity. Once you have set this, run it in the terminal using:

python forwardPropagationTable.py

Once you do that, you should see the following output to the terminal:

             IT      Partitions   AVG Var Ratio    Max Residual             AVG             STD          Volume
              1               1    6.835058e+00    1.262466e+00    5.570783e+01    9.032501e+00    5.141830e+06
              2               2    4.037284e+00    1.074678e+00    5.570807e+01    9.030613e+00    5.141852e+06
              3               4    7.335096e+00    9.657351e-01    5.575031e+01    9.008701e+00    5.145751e+06
              4               7    4.159422e+00    7.227291e-01    5.576919e+01    8.953019e+00    5.147493e+06
              5              12    2.216632e+00    5.285087e-01    5.578102e+01    8.947123e+00    5.148585e+06
              6              18    2.855945e-01    4.079830e-01    5.575821e+01    8.936750e+00    5.146480e+06
              7              28    1.326548e-01    4.079830e-01    5.577478e+01    8.910934e+00    5.148009e+06
              8              29    7.950334e-02    4.079830e-01    5.577496e+01    8.910789e+00    5.148026e+06
              
Where the AVG and STD columns show the mean and standard deviation. You will
want to look at the last row in these columns to find the converged values for 
these quantities.



















































