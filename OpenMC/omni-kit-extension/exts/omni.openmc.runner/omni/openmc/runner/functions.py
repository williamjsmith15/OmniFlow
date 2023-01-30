import os, tarfile, tempfile, pathlib # System packages
import omni

import docker

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
        "general_CAD"       : f"{sep}paramak{sep}dagmc.h5m",
        "sep"               : sep,
        "tmp"               : tmp,
        "share"             : f"{tmp}{sep}share",
        "usdTmp"            : f"{tmp}{sep}usd",
        "outTmpOpenMC"      : f"{tmp}{sep}outOpenMC",
        "workflowDest"      : "/" # IN container
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

    new_sys = False # True to test docker system
    if new_sys:
        # Attach to toil docker container 
        client = docker.from_env()
        toilContainer = client.containers.get("omniflow-toil-1")

        # Send CWL files to container
        print('Sending Files')
        send_files(
            container = toilContainer,
            source = paths["workflow"],
            temp = f'{paths["share"]}{sep}cwlBundle.tar',
            destination = paths["workflowDest"]
        )

        # GET AND COPY USD FILE HERE

        # Run toil
        print('Running Workflow in Container') 
        var = toilContainer.exec_run(
            ["toil-cwl-runner",
            "--no-match-user",
            "--outdir", f"{paths['output_container']}/toy",
            "/tests/toy/openmc_tool_toy.cwl",
            "/tests/toy/script_loc_toy.yml"]
        )
        print(var)
        
        # Copy files back to output folder
        print('Retrieving Files')
        get_files(
            container = toilContainer,
            source = paths['output_container'],
            destination = paths['output_sim'],
            fname = 'toy_output'
        )
    else:
        print(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}tests{sep}toy{sep}openmc_tool_toy.cwl {paths['workflow']}{sep}tests{sep}toy{sep}script_loc_toy.yml")
        os.system(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}tests{sep}toy{sep}openmc_tool_toy.cwl {paths['workflow']}{sep}tests{sep}toy{sep}script_loc_toy.yml")

    print("Toy Test Completed")

def simple_CAD_test():
    #Test Simple CAD
    print("Running Simple CAD Test Workflow")

    print(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}tests{sep}simple{sep}simple_CAD_workflow.cwl {paths['workflow']}{sep}tests{sep}simple{sep}script_loc_simple_CAD.yml")
        
    os.system(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}tests{sep}simple{sep}simple_CAD_workflow.cwl {paths['workflow']}{sep}tests{sep}simple{sep}script_loc_simple_CAD.yml")

    print("DONE!")
    
def run_workflow():
    #Main OpenMC Workflow runner
    print('Running OpenMC Workflow')

    print("Exporting USD Stage")
    export_stage()

    print("Running Workflow")
    print(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}main{sep}openmc_workflow.cwl {paths['workflow']}{sep}main{sep}script_loc.yml")
    os.system(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}main{sep}openmc_workflow.cwl {paths['workflow']}{sep}main{sep}script_loc.yml")

    print(f"Done! Your files will be in: {paths['output_omni']}")


def get_materials():
    # Gets material names from the dagmc.h5m file (if its in the paramak folder)
    print("Getting Material Names")

    print(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.cwl {paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.yml")
        
    os.system(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.cwl {paths['workflow']}{sep}dagmc_material_name{sep}dagmc_materials.yml")

    print("DONE")


def settings_enter(num_source):
    #To remember the number of sources field
    with open(f"{paths['output_omni']}{sep}num_sources.txt", 'w') as file:
        file.write(f"num_sources = {num_source}")


def export_stage():
    print(f"Exporting stage to: {paths['output_omni']}/dagmc.usd")
    stage = omni.usd.get_context().get_stage()
    stage.Export(f"{paths['output_omni']}/dagmc.usd")
    print("Successfully exported USD stage!")
