import os, tarfile, tempfile, pathlib # System packages
import omni

import subprocess, sys # Alternative to os to run shell commands - dont know why it wasn't working before...


#################################################################
## Set Paths for Folders & Create Cases for Linux vs Windows OS
#################################################################

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
        "tmp"               : tmp,
        "share"             : f"{tmp}{sep}share",
        "usdTmp"            : f"{tmp}{sep}usd",
        "outTmpOpenMC"      : f"{tmp}{sep}outOpenMC",
        "workflowDest"      : "/" # In container
    }

# Allow choice between toil runner and cwltool - useful for testing
toil_runner = True
if toil_runner:
    runner = 'toil-cwl-runner'
else:
    runner = 'cwltool'

# Get operating system and set a prefix for the workflow commands
platform = sys.platform
if platform == 'linux':
    prefix_cmd = f'{runner}'
elif platform == 'win32':
    prefix_cmd = f'wsl.exe {runner}'
else:   # Unaccounted for OS
    print(f"I don't know what to do with operating system type: {platform}")


###################################
## Helper Functions
###################################

def t_f(string):
    """
    Convert string to bool with error handling

    Parameters
    ----------
    string: String
        String to be tested if True or False
    
    Returns
    -------
    bool: Default value of False
        True or False
    """

    if string == 'True':
        return True
    elif string == 'False':
        return False
    else:
        print("I don't know what this is, returning default of false")
        return False
    
def export_stage():
    """
    Exports the current USD stage to an output file
    """
    
    path = f"{paths['output_omni']}{sep}dagmc.usd"
    print(f"Exporting stage to: {path}")
    stage = omni.usd.get_context().get_stage()
    stage.Export(path)
    print("Successfully exported USD stage!")

def wsl_file_convert(win_path):
    """
    Converts a windows file path, ie C:\PhD\OmniFlow....
    to a wsl mount file path, ie /mnt/c/PhD/OmniFlow....

    Parameters
    ----------
    win_path: string
        file path in normal windows format
    
    Returns
    -------
    wsl_file: string
        file path in wsl format
    """
    step_in_path = win_path.split('\\')
    drive_letter = step_in_path[0].replace(':', '')
    wsl_file = f"/mnt/{drive_letter}"
    for step in step_in_path[1:]:
        wsl_file = f"{wsl_file}/{step}"

    return wsl_file


###################################
## Workflows
###################################

def toy_test():
    """ 
    Run a test module on a toy problem, validate base system is working
    Writes files into test output folder
    """

    print("Running Toy Test Workflow")

    # Handling of different operating systems 
    if platform == 'linux':
        out_dir = paths['output_test']
        cwl_loc = f"{paths['workflow']}{sep}tests{sep}toy{sep}openmc_tool_toy.cwl"
        yml_loc = f"{paths['workflow']}{sep}tests{sep}toy{sep}script_loc_toy.yml"
    elif platform == 'win32':
        out_dir = wsl_file_convert(paths['output_test'])
        cwl_loc = wsl_file_convert(f"{paths['workflow']}{sep}tests{sep}toy{sep}openmc_tool_toy.cwl")
        yml_loc = wsl_file_convert(f"{paths['workflow']}{sep}tests{sep}toy{sep}script_loc_toy.yml")
    else:
        print(f"Don't know how to handle platform: {platform} yet")

    # Run the workflow 
    cmd = f"{prefix_cmd} --outdir {out_dir} {cwl_loc} {yml_loc}"
    print(cmd)

    output = subprocess.run([i for i in cmd.split(' ')], capture_output=True, text=True)

    print(f'stdout:\n\n{output.stdout}\n\n')
    print(f'stderr:\n\n{output.stderr}\n\n')

    print(f"Toy Test Complete! Your files will be in: {paths['output_test']}")

def simple_CAD_test():
    """ 
    Run a test module on a simple CAD problem, validate CAD system is working
    Writes files into test output folder
    """

    print("Running Simple CAD Test Workflow")

    # Handling of different operating systems 
    if platform == 'linux':
        out_dir = paths['output_test']
        cwl_loc = f"{paths['workflow']}{sep}tests{sep}simple{sep}simple_CAD_workflow.cwl"
        yml_loc = f"{paths['workflow']}{sep}tests{sep}simple{sep}script_loc_simple_CAD.yml"
    elif platform == 'win32':
        out_dir = wsl_file_convert(paths['output_test'])
        cwl_loc = wsl_file_convert(f"{paths['workflow']}{sep}tests{sep}simple{sep}simple_CAD_workflow.cwl")
        yml_loc = wsl_file_convert(f"{paths['workflow']}{sep}tests{sep}simple{sep}script_loc_simple_CAD.yml")
    else:
        print(f"Don't know how to handle platform: {platform} yet")

    # Run the workflow
    cmd = f"{prefix_cmd} --outdir {out_dir} {cwl_loc} {yml_loc}"
    print(cmd)

    output = subprocess.run([i for i in cmd.split(' ')], capture_output=True, text=True)

    print(f'stdout:\n\n{output.stdout}\n\n')
    print(f'stderr:\n\n{output.stderr}\n\n')

    print(f"Simple CAD Test Complete! Your files will be in: {paths['output_test']}")
    
def run_workflow():
    """ 
    Main OpenMC Workflow runner
    Runs workflow with the settings file written to in the extension
    Writes files to simulation folder
    """
     
    print('Running OpenMC Workflow')

    print("Exporting USD Stage")
    export_stage()

    print("Running Workflow")

    # Handling of different operating systems 
    if platform == 'linux':
        out_dir = paths['output_sim']
        cwl_loc = f"{paths['workflow']}{sep}main{sep}openmc_workflow.cwl"
        yml_loc = f"{paths['workflow']}{sep}main{sep}script_loc.yml"
    elif platform == 'win32':
        out_dir = wsl_file_convert(paths['output_sim'])
        cwl_loc = wsl_file_convert(f"{paths['workflow']}{sep}main{sep}openmc_workflow.cwl")
        yml_loc = wsl_file_convert(f"{paths['workflow']}{sep}main{sep}script_loc.yml")
    else:
        print(f"Don't know how to handle platform: {platform} yet")

    # Run the workflow
    cmd = f"{prefix_cmd} --outdir {out_dir} {cwl_loc} {yml_loc}"
    print(cmd)

    output = subprocess.run([i for i in cmd.split(' ')], capture_output=True, text=True)

    print(f'stdout:\n\n{output.stdout}\n\n')
    print(f'stderr:\n\n{output.stderr}\n\n')

    print(f"Done! Your files will be in: {paths['output_sim']}")

def get_materials():
    """ 
    Gets material names from the USD file in the current stage

    Returns
    -------
    materials: 1D String Array
        All material names present in the stage
    """

    print("Getting Material Names")

    print('Exporting File')
    export_stage()

    print(ext_path)

    print('Running materials getter')

    # Handling of different operating systems 
    if platform == 'linux':
        out_dir = paths['output_omni']
        cwl_loc = f"{paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.cwl"
        yml_loc = f"{paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.yml"
    elif platform == 'win32':
        out_dir = wsl_file_convert(paths['output_omni'])
        cwl_loc = wsl_file_convert(f"{paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.cwl")
        yml_loc = wsl_file_convert(f"{paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.yml")
    else:
        print(f"Don't know how to handle platform: {platform} yet")

    # Run the workflow 
    cmd = f"{prefix_cmd} --outdir {out_dir} {cwl_loc} {yml_loc}"
    print(cmd)

    output = subprocess.run([i for i in cmd.split(' ')], capture_output=True, text=True)

    print(f'stdout:\n\n{output.stdout}\n\n')
    print(f'stderr:\n\n{output.stderr}\n\n')

    mat_file_path = f"{paths['output_omni']}{sep}materials.txt"
    materials = []
    if os.path.exists(mat_file_path):
        with open(mat_file_path) as file:
            for line in file:
                materials.append(line)

    print("Materials Getter Finished")

    return materials