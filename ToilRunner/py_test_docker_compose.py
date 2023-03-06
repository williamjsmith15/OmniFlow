import docker

import os

import tempfile, pathlib, tarfile

###################################
## Set Paths & Get Temp Folders
###################################

sep = os.sep    # System separator
ext_path = os.path.realpath(__file__)   # File path of ext
parent_folder = ext_path.split(f"{sep}OmniFlow", 1)[0]  # File path of parent folder to extension
parent_folder = f"{parent_folder}{sep}OmniFlow{sep}OpenMC"
tmp       = tempfile.gettempdir()

paths = {
        "workflow"          : f"{parent_folder}{sep}tools",
        "output_container"  : f"{sep}output",  # IN container
        "output_omni"       : f"{parent_folder}{sep}output{sep}omni",
        "output_sim"        : f"{parent_folder}{sep}output{sep}simulation",
        "output_test"       : f"{parent_folder}{sep}output{sep}test",
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

print(f"{paths['workflow']}{sep}tests{sep}toy{sep}openmc_tool_toy.cwl")

runner = 'cwltool'            # Testing
# runner = 'toil-cwl-runner'    # Testing
container = ' '
# container = ' --no-container '

# os.system(f"wsl.exe {runner}{container}--debug --outdir /mnt/d/PhD/OmniFlow/OpenMC/output/tests /mnt/d/PhD/OmniFlow/OpenMC/tools/tests/toy/openmc_tool_toy.cwl /mnt/d/PhD/OmniFlow/OpenMC/tools/tests/toy/script_loc_toy.yml")
os.system(f"wsl.exe {runner}{container}--debug --outdir /mnt/d/PhD/OmniFlow/OpenMC/output/tests /mnt/d/PhD/OmniFlow/OpenMC/tools/tests/simple/simple_CAD_workflow.cwl /mnt/d/PhD/OmniFlow/OpenMC/tools/tests/simple/script_loc_simple_CAD.yml")



# client = docker.from_env()
# toilContainer = client.containers.get("omniflow-toil-1")

# # var = toilContainer.exec_run(["ls", "OmniFlow/OpenMC/tools/tests/toy"])
# var = toilContainer.exec_run(["toil-cwl-runner", "--debug", "--outdir", "OmniFlow/OpenMC/output/tests", "OmniFlow/OpenMC/tools/tests/toy/openmc_tool_toy.cwl", "OmniFlow/OpenMC/tools/tests/toy/script_loc_toy.yml"])

# for msg in str(var[1]).split("\\n"):
#     for i in msg.split("\\x1b"):
#         print(i)




# To look at:

# https://cwl.discourse.group/t/working-offline-with-singularity/246