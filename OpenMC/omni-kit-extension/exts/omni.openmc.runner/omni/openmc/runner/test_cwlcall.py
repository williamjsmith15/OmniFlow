import os
import subprocess, sys # Alternative to os to run shell commands - dont know why it wasn't working before...
import tempfile

###################################
## Set Paths & Get Temp Folders
###################################

sep = os.sep    # System separator
ext_path = os.path.realpath(__file__)   # File path of ext
parent_folder = ext_path.split(f"{sep}omni-kit", 1)[0]  # File path of parent folder to extension
tmp       = tempfile.gettempdir()

paths = {
        "workflow"          : f"{parent_folder}{sep}tools",
        "output_container"  : f"{sep}output",  # IN container
        "output_omni"       : f"{parent_folder}{sep}output{sep}omni",
        "output_sim"        : f"{parent_folder}{sep}output{sep}simulation",
        "output_test"       : f"{parent_folder}{sep}output{sep}test",
        "general_CAD"       : f"{sep}paramak{sep}dagmc.h5m",
        "sep"               : sep,
        "tmp"               : tmp,
        "share"             : f"{tmp}{sep}share",
        "usdTmp"            : f"{tmp}{sep}usd",
        "outTmpOpenMC"      : f"{tmp}{sep}outOpenMC",
        "workflowDest"      : "/" # In container
    }

cmd = f"toil-cwl-runner --outdir {paths['output_omni']} {paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.cwl {paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.yml"

# output = subprocess.run(["toil-cwl-runner", "--outdir", paths['output_omni'], f"{paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.cwl", f"{paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.yml"], capture_output=True, text=True)

output = subprocess.run([i for i in cmd.split(' ')], capture_output=True, text=True)

print(f'stdout:\n\n{output.stdout}\n\n')
print(f'stderr:\n\n{output.stderr}\n\n')