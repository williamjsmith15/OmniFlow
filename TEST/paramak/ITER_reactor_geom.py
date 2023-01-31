import paramak

reactor = paramak.IterFrom2020PaperDiagram(rotation_angle = 90.0)

reactor.export_dagmc_h5m(filename="dagmc.h5m", min_mesh_size=5, max_mesh_size=20)