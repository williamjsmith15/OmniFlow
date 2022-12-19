# MScDIssertation
Colleciton of Files and Scripts that contain the work performed for a MSc Strucutral Engineering dissertation

Extra Dependencies:
  pip install cwltool

For OpenMC Conda Env:
  conda create <env_name>              # Create the new conda environment to install into
  conda activate <env_name>            # Activate the environment
  conda install -c conda-forge mamba   # Install the package manager mamba
  mabma install openmc                 # Install OpenMC and all its dependencies through mamba

To run:
  cwltool, needs argument --no-pass-user when using the openMC docker container as this means the CWL tool can access the root user and not userID 1000:
    cwl-runner --no-match-user workflows/openmc_workflow.cwl workflows/script_loc.yml   # Can also use toil-cwl-runner insteaed 
  docker container normally: 
    docker run -it -v <parent_folder>/MScDIssertation/:/home/MScDissertation/ openmc/openmc:develop-dagmc-libmesh  # Links the git repo folder to folder /home/MScDissertation on the Docker container
  
To install extension into Omniverse:
  Launch app, go window > extensions > settings and add the <parent_folder>/omni-kit-extension/exts fiel to the filepaths
  Back onto teh extensions manager search fro OpenMC and it should be the only result
  Click on the toggle switch (and can select to autoload so next time it will already be loaded on lauch)
