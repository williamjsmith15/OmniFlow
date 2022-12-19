# Script to run the final test for OpenMC 
import openmc
import math
import os

##################
# DEFINE MATERIALS
##################

mat_pf_coil_1 = openmc.Material(name="pf_coil_1")
mat_pf_coil_1.add_element("Cu", 1, "ao")
mat_pf_coil_1.set_density("g/cm3", 8.96)

mat_pf_coil_2 = openmc.Material(name="pf_coil_2")
mat_pf_coil_2.add_element("Cu", 1, "ao")
mat_pf_coil_2.set_density("g/cm3", 8.96)

mat_pf_coil_3 = openmc.Material(name="pf_coil_3")
mat_pf_coil_3.add_element("Cu", 1, "ao")
mat_pf_coil_3.set_density("g/cm3", 8.96)

mat_pf_coil_4 = openmc.Material(name="pf_coil_4")
mat_pf_coil_4.add_element("Cu", 1, "ao")
mat_pf_coil_4.set_density("g/cm3", 8.96)

mat_pf_coil_5 = openmc.Material(name="pf_coil_5")
mat_pf_coil_5.add_element("Cu", 1, "ao")
mat_pf_coil_5.set_density("g/cm3", 8.96)

mat_pf_coil_6 = openmc.Material(name="pf_coil_6")
mat_pf_coil_6.add_element("Cu", 1, "ao")
mat_pf_coil_6.set_density("g/cm3", 8.96)

mat_outboard_pf_coils_1 = openmc.Material(name="outboard_pf_coils_1")
mat_outboard_pf_coils_1.add_element("Fe", 1, "ao")
mat_outboard_pf_coils_1.set_density("g/cm3", 8.96)

mat_outboard_pf_coils_2 = openmc.Material(name="outboard_pf_coils_2")
mat_outboard_pf_coils_2.add_element("Fe", 1, "ao")
mat_outboard_pf_coils_2.set_density("g/cm3", 8.96)

mat_outboard_pf_coils_3 = openmc.Material(name="outboard_pf_coils_3")
mat_outboard_pf_coils_3.add_element("Fe", 1, "ao")
mat_outboard_pf_coils_3.set_density("g/cm3", 8.96)

mat_outboard_pf_coils_4 = openmc.Material(name="outboard_pf_coils_4")
mat_outboard_pf_coils_4.add_element("Fe", 1, "ao")
mat_outboard_pf_coils_4.set_density("g/cm3", 8.96)

mat_outboard_pf_coils_5 = openmc.Material(name="outboard_pf_coils_5")
mat_outboard_pf_coils_5.add_element("Fe", 1, "ao")
mat_outboard_pf_coils_5.set_density("g/cm3", 8.96)

mat_outboard_pf_coils_6 = openmc.Material(name="outboard_pf_coils_6")
mat_outboard_pf_coils_6.add_element("Fe", 1, "ao")
mat_outboard_pf_coils_6.set_density("g/cm3", 8.96)

mat_plasma = openmc.Material(name="plasma")
mat_plasma.add_element("H", 1, "ao")
mat_plasma.set_density("g/cm3", 0.00001)

mat_blanket = openmc.Material(name="blanket")
mat_blanket.add_element("Pb", 1, "ao")
mat_blanket.set_density("g/cm3", 19)

mat_divertor = openmc.Material(name="divertor")
mat_divertor.add_element("W", 1, "ao")
mat_divertor.set_density("g/cm3", 19.3)

mat_supports = openmc.Material(name="supports")
mat_supports.add_element("Fe", 1, "ao")
mat_supports.set_density("g/cm3", 7.7)

mat_vessel_inner = openmc.Material(name="vessel_inner")
mat_vessel_inner.add_element("Fe", 1, "ao")
mat_vessel_inner.set_density("g/cm3", 7.7)

mat_tf_coils = openmc.Material(name="tf_coils")
mat_tf_coils.add_element("Cu", 1, "ao")
mat_tf_coils.set_density("g/cm3", 8.96)

materials = openmc.Materials(
    [
        mat_pf_coil_1,
        mat_pf_coil_2,
        mat_pf_coil_3,
        mat_pf_coil_4,
        mat_pf_coil_5,
        mat_pf_coil_6,
        mat_outboard_pf_coils_1,
        mat_outboard_pf_coils_2,
        mat_outboard_pf_coils_3,
        mat_outboard_pf_coils_4,
        mat_outboard_pf_coils_5,
        mat_outboard_pf_coils_6,
        mat_plasma,
        mat_blanket,
        mat_divertor,
        mat_supports,
        mat_vessel_inner,
        mat_tf_coils,
    ]
)

materials.export_to_xml()

##################
# DEFINE GEOMETRY
##################

dagmc_univ = openmc.DAGMCUniverse(filename='dagmc.h5m')

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
region = -vac_surf & -reflective_1 & +reflective_2
# creates a cell from the region and fills the cell with the dagmc geometry
containing_cell = openmc.Cell(cell_id=9999, region=region, fill=dagmc_univ)

geometry = openmc.Geometry(root=[containing_cell])
geometry.export_to_xml()

##################
# DEFINE SETTINGS
##################

settings = openmc.Settings()

# Sources
src_pnt = openmc.stats.Point(xyz=(500, 500, 0))
src = openmc.Source(space=src_pnt, energy=openmc.stats.Discrete(x=[12.0,], p=[1.0,]))
src.strength = 1
settings.source = src

# Settings
settings.batches = 10
settings.particles = 5000
settings.run_mode = "fixed source"

settings.export_to_xml()

openmc.run(tracks=True) # Run in tracking mode for visualisation of tracks through CAD
