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


VS Code
Discord
Zoom

pip install docker
pip install cwltool
pip install toil
sudo apt install git
sudo apt install python3-pip
sudo apt install libfuse2 	# For omni - needs it

pip install 

pip install whatsdesk
pip install kazam
pip install paraview


git clone https://github.com/williamjsmith15/OmniFlow
	should point omni to ext path
	get onto correct branch (feature branch)

Omniverse (apps and connectors)
mendeley ref manager
Teams



Firefox:
	motion
	mendeley



Driver using:
	+-----------------------------------------------------------------------------+
	| NVIDIA-SMI 515.86.01    Driver Version: 515.86.01    CUDA Version: 11.7     |
	|-------------------------------+----------------------+----------------------+
	| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
	| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
	|                               |                      |               MIG M. |
	|===============================+======================+======================|
	|   0  NVIDIA GeForce ...  Off  | 00000000:01:00.0 Off |                  N/A |
	| N/A   45C    P0    N/A /  N/A |      5MiB / 16384MiB |      0%      Default |
	|                               |                      |                  N/A |
	+-------------------------------+----------------------+----------------------+
		                                                                       
	+-----------------------------------------------------------------------------+
	| Processes:                                                                  |
	|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
	|        ID   ID                                                   Usage      |
	|=============================================================================|
	|    0   N/A  N/A      1583      G   /usr/lib/xorg/Xorg                  4MiB |
	+-----------------------------------------------------------------------------+
