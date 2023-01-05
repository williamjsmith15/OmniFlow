#!/usr/bin/env cwl-runner
# A command line tool to run usd to h5m converer

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
hints:
  DockerRequirement:
    dockerPull: williamjsmith15/omniflow_openmc-env:latest
inputs:
  usd_h5m_script:
    type: File
    inputBinding:
      position: 1
  usd_CAD:
    type: File
    
outputs:
  h5m_out:
    type: File
    outputBinding:
      glob: dagmc.h5m
      # glob: Test_4_DonutOnCube.h5m # Test case
#   example_out:
#     type: stdout
# stdout: output.txt