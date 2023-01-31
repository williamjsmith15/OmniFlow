#!/usr/bin/env cwl-runner
# A command line tool to run the basic openMC docker container

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
hints:
  DockerRequirement:
    dockerPull: williamjsmith15/omniflow-openmc:latest
inputs:
  script:
    type: File
    inputBinding:
      position: 1
  dagmc_CAD:
    type: File
  settings:
    type: File
    
outputs:
  example_out:
    type: stdout
  tracks_out:
    type: File
    outputBinding:
      glob: tracks.h5
stdout: output.txt