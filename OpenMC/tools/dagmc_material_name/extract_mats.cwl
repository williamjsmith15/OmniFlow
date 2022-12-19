#!/usr/bin/env cwl-runner
# A command line tool to return the materials from a dagmc .h5m file

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
hints:
  DockerRequirement:
    dockerPull: williamjsmith15/omniflow_openmc-env:latest
inputs:
  extract_script:
    type: File
    inputBinding:
        position: 2
  mat_list_in:
    type: File
    inputBinding:
        position: 3

outputs:
  extracted_mats:
    type: File
    outputBinding:
        glob: materials.txt