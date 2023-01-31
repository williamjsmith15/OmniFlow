#!/usr/bin/env cwl-runner
# A command line tool to convert from h5m to vtk fro visualisation of CAD in paraview

cwlVersion: v1.0
class: CommandLineTool
baseCommand: mbconvert
hints:
  DockerRequirement:
    dockerPull: williamjsmith15/omniflow-openmc:latest
inputs:
  CAD_in:
    type: File
    inputBinding:
      position: 1
  str:
    type: string
    inputBinding:
      position: 50
outputs:
  CAD_out:
    type: File
    outputBinding:
      glob: dagmc.vtk