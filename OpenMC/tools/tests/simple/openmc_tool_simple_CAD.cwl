#!/usr/bin/env cwl-runner
# A command line tool to run the basic openMC docker container

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python3
hints:
  DockerRequirement:
    dockerPull: williamjsmith15/omniflow-openmc:latest
    # dockerPull: williamjsmith15/omniflow_openmc-env:latest
inputs:
  script:
    type: File
    inputBinding:
      position: 1
outputs:
  example_out:
    type: stdout
  tallies_out:
    type: File
    outputBinding:
      glob: tallies.out
  tracks_out:
    type: File
    outputBinding:
      glob: tracks.h5
  CAD_out:
    type: File
    outputBinding:
      glob: dagmc.h5m
stdout: output.txt