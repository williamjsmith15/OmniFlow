# OmniFlow
NVIDIA Omniverse Simulation Integration System


To start the docker container:
    First time only to build   - docker compose -f "docker-compose-toil.yml" build
    Every time after to launch - docker compose -f "docker-compose-toil.yml" up

Set the paths to the individual extensions in Omniverse, for example in the case of OpenMC:
    Launch the Omniverse app, go window > extensions > settings and add the <installation-folder>/OmniFlow/OpenMC/omni-kit-extension/exts/ folder to the filepaths
    Back onto the extensions manager search for the extension name (or there is a button to filter for just 3rd Party Exts) and find the extension
    Click on the toggle switch to launch the extenion (and can select to autoload so next time it will already be loaded on lauch)
To Install:

pip install docker
pip install cwltool
pip install toil
sudo apt install git
sudo apt install python3-pip
sudo apt install libfuse2 	# For omni - needs it

git clone https://github.com/williamjsmith15/OmniFlow
	should point omni to ext path
	get onto correct branch (feature branch)