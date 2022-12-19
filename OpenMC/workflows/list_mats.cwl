#!/usr/bin/env cwl-runner
# A command line tool to return the materials from a dagmc .h5m file

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['mbsize', '-ll']
hints:
  DockerRequirement:
    dockerPull: williamjsmith15/omniflow_openmc-env:latest
inputs:
  h5m_CAD_in:
    type: File
    inputBinding:
        position: 3

outputs:
  mat_list_out:
    type: stdout
stdout: mat_list.txt

