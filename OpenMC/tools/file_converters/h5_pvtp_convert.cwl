#!/usr/bin/env cwl-runner
# A command line tool to convert from h5 to pvtp fro visualisation of tracks in paraview

cwlVersion: v1.0
class: CommandLineTool
baseCommand: openmc-track-to-vtk
hints:
  DockerRequirement:
    dockerPull: williamjsmith15/omniflow_openmc-env:latest
inputs:
  tracks_in:
    type: File
    inputBinding:
      position: 1
outputs:
  tracks_out_loc:
    type: File
    outputBinding:
      glob: tracks.pvtp
  tracks_out_data:
    type: File
    outputBinding:
      glob: tracks_0.vtp