import os

sep = os.sep    # System separator
ext_path = os.path.realpath(__file__)   # File path of ext
parent_folder = ext_path.split(f"{sep}omni-kit", 1)[0]  # File path of parent folder to extension

paths = {
        "workflow"          : f"{parent_folder}{sep}workflows",
        "output_toy"        : f"{parent_folder}{sep}output{sep}toy",
        "output_simple"     : f"{parent_folder}{sep}output{sep}simpleCAD",
        "output_omni"       : f"{parent_folder}{sep}output{sep}omni",
        "general_CAD"       : f"{parent_folder}{sep}paramak{sep}dagmc.h5m",
        "sep"               : sep
    }

def toy_test():
    #Test Toy
    print("Running Toy Test Workflow")

    print(f"cwltool --outdir {paths['output_toy']} --no-match-user {paths['workflow']}{sep}openmc_tool_toy.cwl {paths['workflow']}{sep}script_loc_toy.yml")
        
    os.system(f"cwltool --outdir {paths['output_toy']} --no-match-user {paths['workflow']}{sep}openmc_tool_toy.cwl {paths['workflow']}{sep}script_loc_toy.yml")
    
    print("DONE!")

def simple_CAD_test():
    #Test Simple CAD
    print("Running Simple CAD Test Workflow")

    print(f"cwltool --outdir {paths['output_simple']} --no-match-user {paths['workflow']}{sep}simple_CAD_workflow.cwl {paths['workflow']}{sep}script_loc_simple_CAD.yml")
        
    os.system(f"cwltool --outdir {paths['output_simple']} --no-match-user {paths['workflow']}{sep}simple_CAD_workflow.cwl {paths['workflow']}{sep}script_loc_simple_CAD.yml")

    print("DONE!")
    
def run_workflow():
    #Main OpenMC Workflow runner
    print('Running OpenMC Workflow')

    print("Generating Files")

    print(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}openmc_workflow.cwl {paths['workflow']}{sep}script_loc.yml")
        
    os.system(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}openmc_workflow.cwl {paths['workflow']}{sep}script_loc.yml")

    print(f"Done! Your files will be in: {paths['output_omni']}")


def get_materials():
    # Gets material names from the dagmc.h5m file (if its in the paramak folder)
    print("Getting Material Names")

    print(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}dagmc_materials.cwl {paths['workflow']}{sep}dagmc_materials.yml")
        
    os.system(f"cwltool --outdir {paths['output_omni']} --no-match-user {paths['workflow']}{sep}dagmc_materials.cwl {paths['workflow']}{sep}dagmc_materials.yml")

    print("DONE")


def settings_enter(num_source):
    #To remember the number of sources field
    with open(f"{paths['output_omni']}{sep}num_sources.txt", 'w') as file:
        file.write(f"num_sources = {num_source}")
