import tulipUQ as uq
import tulipAC as ac
import sys
import os
import numpy as np
import time
import glob

#===============================================================================
#                            USER INPUTS HERE

INPUTS_FILE = 'sampledInputs.txt'
OUTPUTS_FILE = 'cylinderResults.txt'

#===============================================================================

if __name__ == '__main__':

  inputs = uq.uqSamples()

  # Create the Uncertainty Propagation Action Object
  mwBcs = ac.acActionUP_MWBCS()
  
  # Set Options
  mwBcs.opts.inputMode = ac.imTable
  mwBcs.opts.tableInputFileName = INPUTS_FILE
  mwBcs.opts.tableOutputFileName = OUTPUTS_FILE
  
  mwBcs.opts.addBoundaryPoints = False
  mwBcs.opts.boundaryPointOther = 30
  
  mwBcs.opts.numIniSamples = 0
  mwBcs.opts.doRefineSpace = True
  mwBcs.opts.doRefineSamples = False
  mwBcs.opts.maxMWOrder = 2
  mwBcs.opts.mwQuadOrder = 30
  mwBcs.opts.outputColumn = 0 # TODO: Change this to loop!
  mwBcs.opts.thresholdSize = 0.01
  mwBcs.opts.maxPartitionSizeRatio = 2.0
  mwBcs.opts.minSamplesInPartition = 10
  mwBcs.opts.maxMWVarianceRatio = 1e-4
  mwBcs.opts.forceRVMSolution = False
  mwBcs.opts.resToleranceRatio = 0.1
  
  # Set messaging options
  mwBcs.opts.printPartitionTree = True
  mwBcs.opts.printInputOutputSamples = True
  mwBcs.opts.printPartitionSamples = True
  mwBcs.opts.printAndEvalSurrogate = False
  mwBcs.opts.printPartitionMonitor = True
  mwBcs.opts.printOverallStats = True
  mwBcs.simulPrefix = 'cylinderUQ_'
  
  # Run the forward propagation
  mwBcs.go()
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
