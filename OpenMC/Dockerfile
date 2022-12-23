FROM openmc/openmc:develop-dagmc-libmesh

# Currently not working
# # Move the cross section files to an accessbile folder and change the path (circumvents the issue with UserID not being root)
# RUN cp -r ~/nndc_hdf5/ /home
# ENV OPENMC_CROSS_SECTIONS=/home/nndc_hdf5/cross_sections.xml

RUN cp -r ~/nndc_hdf5/ /home

RUN pip install vtk
RUN pip install vertices_to_h5m
RUN pip install usd-core
RUN pip install openmc_data_downloader


WORKDIR /
# CMD echo 'Test launch of container'