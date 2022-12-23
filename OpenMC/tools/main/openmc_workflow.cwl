#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
inputs:
    script:
        type: File
    str:
        type: string
    dagmc_CAD:
        type: File
    settings:
        type: File


steps:
    openmc:
        run: openmc_tool.cwl
        in:
            script: script
            dagmc_CAD: dagmc_CAD
            settings: settings
        out:
            [example_out, tracks_out]
    h5m-vtk:
        run: ../file_converters/h5m_vtk_convert.cwl
        in:
            CAD_in: dagmc_CAD
            str: str
        out:
            [CAD_out]
    h5-pvtp:
        run: ../file_converters/h5_pvtp_convert.cwl
        in:
            tracks_in: openmc/tracks_out
        out:
            [tracks_out_loc, tracks_out_data]

outputs:
    # example_out:
    #     type: stdout
    #     outputSource: openmc/example_out
    CAD_out:
        type: File
        outputSource: h5m-vtk/CAD_out
    tracks_out_loc:
        type: File
        outputSource: h5-pvtp/tracks_out_loc
    tracks_out_data:
        type: File
        outputSource: h5-pvtp/tracks_out_data
