import os, tarfile, tempfile, pathlib # System packages
import omni

import subprocess, sys # Alternative to os to run shell commands - dont know why it wasn't working before...


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

pathlib.Path(paths["share"]).mkdir(parents=True, exist_ok=True)
pathlib.Path(paths["usdTmp"]).mkdir(parents=True, exist_ok=True)
pathlib.Path(paths["outTmpOpenMC"]).mkdir(parents=True, exist_ok=True)

###################################
## Helper Functions
###################################

def make_tarfile(source_dir, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        print(f"{source_dir} contains: {os.listdir(source_dir)}")
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    return tar


def send_files(container, source, temp, destination):
    make_tarfile(source, temp)
    with open(temp, 'rb') as bundle:
        ok = container.put_archive(path=destination, data=bundle)
        if not ok:
            raise Exception(f'Put {source} to {destination} failed')
        else:
            print(f'Uploaded {source} ({os.path.getsize(temp)} B) to {destination} successfully')

def get_files(container, source, destination, fname):
    
    f = open(f"{destination}{sep}{fname}.tar", 'wb')
    bits, stat = container.get_archive(path = source)
    for chunck in bits:
        f.write(chunck)
    f.close()
    

###################################
## Workflows
###################################

def toy_test():
    #Test Toy
    print("Running Toy Test Workflow")

    cmd = f"toil-cwl-runner --outdir {paths['output_test']} {paths['workflow']}{sep}tests{sep}toy{sep}openmc_tool_toy.cwl {paths['workflow']}{sep}tests{sep}toy{sep}script_loc_toy.yml"
    print(cmd)

    output = subprocess.run([i for i in cmd.split(' ')], capture_output=True, text=True)

    print(f'stdout:\n\n{output.stdout}\n\n')
    print(f'stderr:\n\n{output.stderr}\n\n')

    # print(f"cwltool --outdir {paths['output_test']} {paths['workflow']}{sep}tests{sep}toy{sep}openmc_tool_toy.cwl {paths['workflow']}{sep}tests{sep}toy{sep}script_loc_toy.yml")
    # os.system(f"cwltool --outdir {paths['output_test']} {paths['workflow']}{sep}tests{sep}toy{sep}openmc_tool_toy.cwl {paths['workflow']}{sep}tests{sep}toy{sep}script_loc_toy.yml")

    print(f"Toy Test Complete! Your files will be in: {paths['output_test']}")

def simple_CAD_test():
    #Test Simple CAD
    print("Running Simple CAD Test Workflow")

    cmd = f"toil-cwl-runner --outdir {paths['output_test']} {paths['workflow']}{sep}tests{sep}simple{sep}simple_CAD_workflow.cwl {paths['workflow']}{sep}tests{sep}simple{sep}script_loc_simple_CAD.yml"
    print(cmd)

    output = subprocess.run([i for i in cmd.split(' ')], capture_output=True, text=True)

    print(f'stdout:\n\n{output.stdout}\n\n')
    print(f'stderr:\n\n{output.stderr}\n\n')

    # print(f"cwltool --outdir {paths['output_test']} {paths['workflow']}{sep}tests{sep}simple{sep}simple_CAD_workflow.cwl {paths['workflow']}{sep}tests{sep}simple{sep}script_loc_simple_CAD.yml")  
    # os.system(f"cwltool --outdir {paths['output_test']} {paths['workflow']}{sep}tests{sep}simple{sep}simple_CAD_workflow.cwl {paths['workflow']}{sep}tests{sep}simple{sep}script_loc_simple_CAD.yml")

    print(f"Simple CAD Test Complete! Your files will be in: {paths['output_test']}")
    
def run_workflow():
    #Main OpenMC Workflow runner
    print('Running OpenMC Workflow')

    print("Exporting USD Stage")
    export_stage()

    print("Running Workflow")

    cmd = f"toil-cwl-runner --outdir {paths['output_sim']} {paths['workflow']}{sep}main{sep}openmc_workflow.cwl {paths['workflow']}{sep}main{sep}script_loc.yml"
    print(cmd)

    output = subprocess.run([i for i in cmd.split(' ')], capture_output=True, text=True)

    print(f'stdout:\n\n{output.stdout}\n\n')
    print(f'stderr:\n\n{output.stderr}\n\n')

    # print(f"cwltool --outdir {paths['output_sim']} {paths['workflow']}{sep}main{sep}openmc_workflow.cwl {paths['workflow']}{sep}main{sep}script_loc.yml")
    # os.system(f"cwltool --outdir {paths['output_sim']} {paths['workflow']}{sep}main{sep}openmc_workflow.cwl {paths['workflow']}{sep}main{sep}script_loc.yml")

    print(f"Done! Your files will be in: {paths['output_sim']}")


def get_materials():
    # Gets material names from the usd file outputted by the omniverse extension
    print("Getting Material Names")

    print('Exporting File')
    export_stage()

    print(ext_path)

    print('Running materials getter')

    cmd = f"toil-cwl-runner --outdir {paths['output_omni']} {paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.cwl {paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.yml"
    print(cmd)

    output = subprocess.run([i for i in cmd.split(' ')], capture_output=True, text=True)

    print(f'stdout:\n\n{output.stdout}\n\n')
    print(f'stderr:\n\n{output.stderr}\n\n')

    # output = subprocess.run(["toil-cwl-runner", "--outdir", paths['output_omni'], f"{paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.cwl", f"{paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.yml"], capture_output=True, text=True)

    # print(f'stdout:\n\n{output.stdout}\n\n')
    # print(f'stderr:\n\n{output.stderr}\n\n')

    # output = subprocess.run(["cwltool", "/home/williamjsmith15/PhD/OmniFlow/test.txt"], capture_output=True, text=True)

    # print(f'stdout:\n\n{output.stdout}\n\n')
    # print(f'stderr:\n\n{output.stderr}\n\n')

    mat_file_path = f"{paths['output_omni']}{paths['sep']}materials.txt"
    materials = []
    if os.path.exists(mat_file_path):
        with open(mat_file_path) as file:
            for line in file:
                materials.append(line)

    print("Materials Getter Finished")

    return materials

def export_stage():
    print(f"Exporting stage to: {paths['output_omni']}/dagmc.usd")
    stage = omni.usd.get_context().get_stage()
    stage.Export(f"{paths['output_omni']}/dagmc.usd")
    print("Successfully exported USD stage!")


def t_f(string):
    # Quick helper function to convert string to bool
    if string == 'True':
        return True
    elif string == 'False':
        return False
    else:
        print('I dont know what this is, returning default of false')
        return False