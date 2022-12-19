#From https://nbviewer.org/github/openmc-dev/openmc-notebooks/blob/main/cad-based-geometry.ipynb

import urllib.request
from IPython.display import Image
import openmc
from matplotlib import pyplot as plt


        


##################
# DEFINE MATERIALS
##################

water = openmc.Material(name="water")
water.add_nuclide('H1', 2.0, 'ao')
water.add_nuclide('O16', 1.0, 'ao')
water.set_density('g/cc', 1.0)
water.add_s_alpha_beta('c_H_in_H2O')
water.id = 41

iron = openmc.Material(name="iron")
iron.add_nuclide("Fe54", 0.0564555822608)
iron.add_nuclide("Fe56", 0.919015287728)
iron.add_nuclide("Fe57", 0.0216036861685)
iron.add_nuclide("Fe58", 0.00292544384231)
iron.set_density("g/cm3", 7.874)
mats = openmc.Materials([iron, water])
mats.export_to_xml()

##################
# DEFINE GEOMETRY
##################

teapot_url = 'https://tinyurl.com/y4mcmc3u' # 29 MB

def download(url):
    """
    Helper function for retrieving dagmc models
    """
    u = urllib.request.urlopen(url)
    
    if u.status != 200:
        raise RuntimeError("Failed to download file.")
    
    # save file as dagmc.h5m
    with open("dagmc.h5m", 'wb') as f:
        f.write(u.read())

download(teapot_url)

dagmc_univ = openmc.DAGMCUniverse(filename="dagmc.h5m")
geometry = openmc.Geometry(root=dagmc_univ)
geometry.export_to_xml()

##################
# DEFINE SETTINGS
##################

settings = openmc.Settings()
settings.batches = 10
settings.particles = 5000
settings.run_mode = "fixed source"

src_locations = ((-4.0, 0.0, -2.0),
                 ( 4.0, 0.0, -2.0),
                 ( 4.0, 0.0, -6.0),
                 (-4.0, 0.0, -6.0),
                 (10.0, 0.0, -4.0),
                 (-8.0, 0.0, -4.0))

# we'll use the same energy for each source
src_e = openmc.stats.Discrete(x=[12.0,], p=[1.0,])

# create source for each location
sources = []
for loc in src_locations:
    src_pnt = openmc.stats.Point(xyz=loc)
    src = openmc.Source(space=src_pnt, energy=src_e)
    sources.append(src)

src_str = 1.0 / len(sources)
for source in sources:
    source.strength = src_str

settings.source = sources
settings.export_to_xml()



mesh = openmc.RegularMesh()
mesh.dimension = (120, 1, 40)
mesh.lower_left = (-20.0, 0.0, -10.0)
mesh.upper_right = (20.0, 1.0, 4.0)

mesh_filter = openmc.MeshFilter(mesh)

pot_filter = openmc.CellFilter([1])
pot_tally = openmc.Tally()
pot_tally.filters = [mesh_filter, pot_filter]
pot_tally.scores = ['flux']

water_filter = openmc.CellFilter([5])
water_tally = openmc.Tally()
water_tally.filters = [mesh_filter, water_filter]
water_tally.scores = ['flux']


tallies = openmc.Tallies([pot_tally, water_tally])
tallies.export_to_xml()

openmc.run(tracks=True) # Run in tracking mode for visualisation of tracks through CAD



##################
# PLOTTING
##################


sp = openmc.StatePoint("statepoint.10.h5")

water_tally = sp.get_tally(scores=['flux'], id=water_tally.id)
water_flux = water_tally.mean
water_flux.shape = (40, 120)
water_flux = water_flux[::-1, :]

pot_tally = sp.get_tally(scores=['flux'], id=pot_tally.id)
pot_flux = pot_tally.mean
pot_flux.shape = (40, 120)
pot_flux = pot_flux[::-1, :]

del sp


p = openmc.Plot()
p.basis = 'xz'
p.origin = (0.0, 0.0, 0.0)
p.width = (30.0, 20.0)
p.pixels = (450, 300)
p.color_by = 'material'
p.colors = {iron: 'gray', water: 'blue'}
openmc.plot_inline(p)

plt.savefig('Plot_1.png')
plt.clf()

fig = plt.figure(figsize=(18, 16))

sub_plot1 = plt.subplot(121, title="Kettle Flux")
sub_plot1.imshow(pot_flux)



sub_plot2 = plt.subplot(122, title="Water Flux")
sub_plot2.imshow(water_flux)

plt.savefig('Flux.png')
plt.clf()

















