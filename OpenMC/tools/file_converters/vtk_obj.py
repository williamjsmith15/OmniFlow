# Convert vtk to obj file format
# Credit: https://github.com/lodeguns/VTK-OBJ/blob/master/vtk_to_obj_converter.py

import pyvista as pv
import os 
from pyvista import examples

# System separator
sep = os.sep
this_path = os.path.realpath(__file__)
parent_folder = this_path.split(f"{sep}file_convertors", 1)[0]

paths = {
    "input" : f"{parent_folder}{sep}test_output",
    "output"   : f"{parent_folder}{sep}test_output"
}

def convert(indir, outdir) :
    files = os.listdir(indir)
    files = [ os.path.join(indir,f) for f in files if f.endswith('.vtk') ]

    for f in files:
        mesh = pv.read(f)
        basename = os.path.basename(f)
        print("Copying file:", basename)
        basename = os.path.splitext(basename)[0]
        print("File name:", basename)
        othermesh = examples.load_uniform()
        legend_entries = []
        legend_entries.append(['Liver converted', 'w'])
        legend_entries.append(['External marker', 'k'])
        plotter = pv.Plotter()
        _ = plotter.add_mesh(mesh)
        _ = plotter.add_mesh(othermesh, 'k')
        _ = plotter.add_legend(legend_entries)
        _ = plotter.export_obj(outdir+"conv_"+basename+".obj")
        plotter.export_obj(f"{basename}.obj")


convert(paths['input'], paths['output'])