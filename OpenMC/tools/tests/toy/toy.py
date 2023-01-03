# From https://nbviewer.org/github/openmc-dev/openmc-notebooks/blob/main/pincell.ipynb
# An OpenMC python script that runs a toy problem example 


import openmc
import matplotlib.pyplot as plt         # Extra to save plots produced in the process
import openmc_data_downloader as odd    # Removes need to have the --no-match-user in the CWL call, this downloads the data files needed for the neutronics code automatically
import os

# #Set cross sections XML path
# os.environ["OPENMC_CROSS_SECTIONS"] = str('/home/nndc_hdf5/cross_sections.xml')

####################
# DEFINING MATERIALS
####################

# Uranium Dioxide Fuel
uo2 = openmc.Material(name="uo2") # Create material variable with name uo2
uo2.add_nuclide('U235', 0.03)	# Add nuclides to material 
uo2.add_nuclide('U238', 0.97)
uo2.add_nuclide('O16', 2.0)
uo2.set_density('g/cm3', 10.0)	# Set density of material

# Zirchonium Casing
zirconium = openmc.Material(name="zirconium")
zirconium.add_element('Zr', 1.0) # Use of add element as elemental material
zirconium.set_density('g/cm3', 6.6)

# Water Coolant
water = openmc.Material(name="h2o") # Same process as uo2
water.add_nuclide('H1', 2.0)
water.add_nuclide('O16', 1.0)
water.set_density('g/cm3', 1.0)
# water.add_s_alpha_beta('c_H_in_H2O') # So bound-atom cross section is used as thermal energies rather than free-atom

mats = openmc.Materials([uo2, zirconium, water]) # Add all materials to a group of materials

# odd.just_in_time_library_generator(
#     libraries = 'ENDFB-7.1-NNDC',
#     materials = mats
# )

# os.environ["OPENMC_CROSS_SECTIONS"] = str('/home/nndc_hdf5/cross_sections.xml')

mats.export_to_xml() # Export the material data to a .xml file that the solver will use later on

os.system('cat materials.xml')

####################
# DEFINING GEOMETRY
####################

# Set cylinders to define regions and then define regions from those cylinders
fuel_outer_radius = openmc.ZCylinder(r=0.39)
clad_inner_radius = openmc.ZCylinder(r=0.40)
clad_outer_radius = openmc.ZCylinder(r=0.46)
fuel_region = -fuel_outer_radius
gap_region = +fuel_outer_radius & -clad_inner_radius
clad_region = +clad_inner_radius & -clad_outer_radius

# Assign matreials and regions to cells
fuel = openmc.Cell(name='fuel')
fuel.fill = uo2
fuel.region = fuel_region

gap = openmc.Cell(name='air gap')
gap.region = gap_region

clad = openmc.Cell(name='clad')
clad.fill = zirconium
clad.region = clad_region

# Create a box around the cylinders and fill with water as coolant
pitch = 1.26
box = openmc.rectangular_prism(width=pitch, height=pitch, boundary_type='reflective')
water_region = box & +clad_outer_radius

moderator = openmc.Cell(name='moderator')
moderator.fill = water
moderator.region = water_region

# Add all cells to the overall universe and again push to .xml for use by the solver
root_universe = openmc.Universe(cells=(fuel, gap, clad, moderator))
geometry = openmc.Geometry(root_universe)
geometry.export_to_xml()



####################
# DEFINING SETTINGS
####################

# Create a point source
point = openmc.stats.Point((0, 0, 0))
source = openmc.Source(space=point)

# Set settings
settings = openmc.Settings()
settings.source = source
settings.batches = 100
settings.inactive = 10
settings.particles = 1000

# Push settings to .xml for solver
settings.export_to_xml()



####################
# DEFINING TALLIES
####################

cell_filter = openmc.CellFilter(fuel) # What space the tallies take place in

tally = openmc.Tally(1)
tally.filters = [cell_filter]

# Tell tally what to collect info on
tally.nuclides = ['U235']
tally.scores = ['total', 'fission', 'absorption', '(n,gamma)']

# Export to .xml for solver
tallies = openmc.Tallies([tally])
tallies.export_to_xml()


####################
# RUN
####################

openmc.run(tracks=True) # Run in tracking mode for visualisation of tracks through CAD


# Plot geometries
plot = openmc.Plot()
plot.filename = 'pinplot'
plot.width = (pitch, pitch)
plot.pixels = (200, 200)
plot.color_by = 'material'
plot.colors = {uo2: 'yellow', water: 'blue'}
plots = openmc.Plots([plot])
plots.export_to_xml()


openmc.plot_geometry()



