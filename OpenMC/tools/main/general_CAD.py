# Steps for this workflow:
    # CAD through cubit and then into h5m format (throuigh mb convert)
    # Cubit adds materials etc etc 
    # Run send CAD file along with this script into the DOCKER container 

import openmc
import os
import math

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
mats = []
srcs = []
sets = []
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
                mats.append(line.split())
        elif position == 2:
            if "SETTINGS" in line:
                position = 3
            else:
                srcs.append(line.split())
        elif position == 3:
            sets.append(line.split())
        

##################
# DEFINE MATERIALS
##################

tmp_mat_array = []
for mat in mats:
    tmp_mat = openmc.Material(name = mat[0])
    tmp_mat.add_element(mat[1], 1, "ao")
    tmp_mat.set_density("g/cm3", float(mat[2]))
    tmp_mat_array.append(tmp_mat)

materials = openmc.Materials(tmp_mat_array)
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
vac_surf = openmc.Sphere(r=10000, surface_id=9999, boundary_type="vacuum")
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

# Sources
sources = []
for src in srcs:
    src_pnt = openmc.stats.Point(xyz=(float(src[1]), float(src[2]), float(src[3])))
    src = openmc.Source(space=src_pnt, energy=openmc.stats.Discrete(x=[float(src[0]),], p=[1.0,]))
    sources.append(src)
src_str = 1.0 / len(sources)
for source in sources:
    source.strength = src_str
settings.source = sources

# Settings
settings.batches = 10
settings.particles = 5000
settings.run_mode = "fixed source"

settings.export_to_xml()

openmc.run(tracks=True) # Run in tracking mode for visualisation of tracks through CAD