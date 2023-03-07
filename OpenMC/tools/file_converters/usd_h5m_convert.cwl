#!/usr/bin/env cwl-runner
# A command line tool to run usd to h5m converer

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python3
hints:
  DockerRequirement:
    dockerPull: williamjsmith15/omniflow-openmc:latest
inputs:
  usd_h5m_script:
    type: File
    inputBinding:
      position: 1
  usd_CAD:
    type: File
  settings:
    type: File
    
outputs:
  dagmc_CAD:
    type: File
    outputBinding:
      glob: dagmc.h5m
      # glob: Test_4_DonutOnCube.h5m # Test case
#   example_out:
#     type: stdout
# stdout: output.txt