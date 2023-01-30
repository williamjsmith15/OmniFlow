#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    extract_script:
        type: File
    usd_CAD:
        type: File
    usd_h5m_script:
        type: File


steps:
    usd_h5m:
        run: ../file_converters/usd_h5m_convert.cwl
        in:
            usd_h5m_script: usd_h5m_script
            usd_CAD: usd_CAD
        out:
            [dagmc_CAD]

    list_mats:
        run: list_mats.cwl
        in:
            h5m_CAD_in: usd_h5m/dagmc_CAD
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