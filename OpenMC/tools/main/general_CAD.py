# Steps for this workflow:
    # CAD through cubit and then into h5m format (throuigh mb convert)
    # Cubit adds materials etc etc 
    # Run send CAD file along with this script into the DOCKER container 

import openmc
import os
import math
import openmc_plasma_source as ops
import numpy as np

# Find the settings file
sep = os.sep
path_py = os.path.realpath(__file__)
settings_path = ''
geometry_path = ''

# Find parent folder path
if "MScDIssertation" in path_py:
    cwl_folder = path_py.split(f"{sep}MScDIssertation", 1)[0]
elif "cwl" in path_py:
    cwl_folder = path_py.split(f"{sep}cwl", 1)[0]

# Find settings and dagmc files
for root, dirs, files in os.walk(cwl_folder):
    for file in files:
        if file.endswith("settings.txt"):
            settings_path = os.path.join(root, file)
        if file.endswith("dagmc.h5m"):
            geometry_path = os.path.join(root, file)

# Get all settings out
materials_input = []
sources_input = []
settings_input = []
ex_settings = []
position = 0
with open(settings_path) as f:
    for line in f:
        if position == 0:
            if "MATERIALS" in line:
                position = 1
        elif position == 1:
            if "SOURCES" in line:
                position = 2
            else:
                materials_input.append(line.split())
        elif position == 2:
            if "SETTINGS" in line:
                position = 3
            else:
                sources_input.append(line.split())
        elif position == 3:
            if "EXT_SETTINGS" in line:
                position = 4
            else:
                settings_input.append(line.split())
        elif position == 4:
            ex_settings.append(line.split())
        

##################
# DEFINE MATERIALS
##################

tmp_material_array = []
# Temp for testing
# for material in materials_input:
#     tmp_material = openmc.Material(name = material[0])
#     tmp_material.add_element('Fe', 1, 'ao')
#     tmp_material.set_density("g/cm3", 7.7)
#     tmp_material_array.append(tmp_material)
for material in materials_input:
    tmp_material = openmc.Material(name = material[0])
    tmp_material.add_element(material[1], 1, "ao")
    tmp_material.set_density("g/cm3", float(material[2]))
    tmp_material_array.append(tmp_material)

materials = openmc.Materials(tmp_material_array)
materials.export_to_xml()

##################
# DEFINE GEOMETRY
##################
# Hack to handle the boundaires for the geometry (for now) - future look at how to handle this
# Took from the paramak examples https://github.com/fusion-energy/magnetic_fusion_openmc_dagmc_paramak_example/blob/main/2_run_openmc_dagmc_simulation.py
dagmc_univ = openmc.DAGMCUniverse(filename=geometry_path)
# geometry = openmc.Geometry(root=dagmc_univ)
# geometry.export_to_xml()

# creates an edge of universe boundary surface
vac_surf = openmc.Sphere(r=100000, surface_id=9999, boundary_type="vacuum")
# lead_surf = -openmc.Sphere(r=60000) & + openmc.Sphere(r=50000)
# lead = openmc.Material(name='lead')
# lead.set_density('g/cc', 11.4)
# lead.add_element('Pb', 1)
# lead_cell = openmc.Cell(fill=lead, region=lead_surf)
# adds reflective surface for the sector model at 0 degrees
reflective_1 = openmc.Plane(
    a=math.sin(0),
    b=-math.cos(0),
    c=0.0,
    d=0.0,
    surface_id=9991,
    boundary_type="reflective",
)
# adds reflective surface for the sector model at 90 degrees
reflective_2 = openmc.Plane(
    a=math.sin(math.radians(90)),
    b=-math.cos(math.radians(90)),
    c=0.0,
    d=0.0,
    surface_id=9990,
    boundary_type="reflective",
)
# specifies the region as below the universe boundary and inside the reflective surfaces
region = -vac_surf # & -reflective_1 & +reflective_2 DEBUGGING
# creates a cell from the region and fills the cell with the dagmc geometry
containing_cell = openmc.Cell(cell_id=9999, region=region, fill=dagmc_univ)

geometry = openmc.Geometry(root=[containing_cell])
geometry.export_to_xml()

##################
# DEFINE SETTINGS
##################

settings = openmc.Settings()

source_type = ''

for ex_setting in ex_settings:
    if ex_setting[0] == "source_type":
        source_type = " ".join(ex_setting[1:])
    else:
        print(f"Don't know what to do with {ex_setting}")

# Sources
sources = []
angle_conversion = (2*np.pi)/360
if source_type == 'Point Source': # If a point source
    for source in sources_input:
        source_pnt = openmc.stats.Point(xyz=(float(source[1]), float(source[2]), float(source[3])))
        source = openmc.Source(space=source_pnt, energy=openmc.stats.Discrete(x=[float(source[0]),], p=[1.0,]))
        sources.append(source)
    source_str = 1.0 / len(sources)
    for source in sources:
        source.strength = source_str
elif source_type == 'Fusion Point Source':
    for source in sources_input:
        source_single = ops.FusionPointSource(

        )
        sources.append(source_single)
elif source_type == 'Fusion Ring Source':
    for source in sources_input:
        source_single = ops.FusionRingSource(
            angles =        (float(source[2])*angle_conversion, float(source[3])*angle_conversion),
            radius =        float(source[0]),
            temperature =   float(source[4]),
            fuel =          str(source[1]),
            z_placement =   float(source[5])
        )
        sources.append(source_single)
elif source_type == 'Tokamak Source':
    for source in sources_input:
        source_single = ops.TokamakSource(

        ).make_openmc_sources()
        sources.append(source_single)
else:
    print(f'I dont know what to do with {source_type}')

settings.source = sources


# Settings
for setting in settings_input:
    try:
        if setting[0] == "batches":     # Apparently the version of python being used is not new enough for swtich statements... :(
            settings.batches = int(setting[1])
        elif setting[0] == "particles":
            settings.particles = int(setting[1])
        elif setting[0] == "run_mode":
            settings.run_mode = str(" ".join(setting[1:]))
        else:
            print(f"Setting: {setting} did not match one of the expected cases.")
    except:
        print(f"There was an error with setting {setting} somewhere...")

settings.export_to_xml()

openmc.run(tracks=True) # Run in tracking mode for visualisation of tracks through CAD
