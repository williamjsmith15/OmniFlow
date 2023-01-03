#!/usr/bin/env cwl-runner
# A command line tool to run the basic openMC docker container

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
hints:
  DockerRequirement:
    dockerPull: ghcr.io/fusion-energy/neutronics-workshop
    # dockerImageId: williamjsmith15/omniflow_openmc-env:latest
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
stdout: output.txt