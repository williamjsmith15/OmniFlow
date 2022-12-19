#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    extract_script:
        type: File
    h5m_CAD_in:
        type: File


steps:
    list_mats:
        run: list_mats.cwl
        in:
            h5m_CAD_in: h5m_CAD_in
        out:
            [mat_list_out]
    extract_mats:
        run: extract_mats.cwl
        in:
            extract_script: extract_script
            mat_list_in: list_mats/mat_list_out
        out:
            [extracted_mats]

outputs:
    extracted_mats:
        type: File
        outputSource: extract_mats/extracted_mats