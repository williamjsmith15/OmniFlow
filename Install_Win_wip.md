
# Setup

## Environment Setup

Download and install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and follow all the instructions given by microsoft. The default installation options here are fine (system tested running with an Ubuntu distro install)

Download and install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/), follow the instalation steps and set up docker with the WSL 2 install in the previous step.

Can verify the version and installation of both of these running these commands in PowerShell or the Command Prompt:
``
wsl -l -v
docker version
``

Next, on wsl, install cwltool and the toil-cwl-runner, fist update the installer:
```
sudo apt-get update
```
followed by
```
sudo apt-get install cwltool
sudo apt-get install python3-pip
pip install toil[cwl]
```
both of the workflow runners can be tested later when the repository is cloned on the test OpenMC cases.


To save time later when running the Monte Carlo solver, the Docker image for this can be downloaded now by running
```
docker run -it williamjsmith15/omniflow-openmc:latest
```
and then when the image is installed and running, in the command line run
```
python
import openmc
```
if this throws no errors then the container has been downloaded and the packages inside set up correctly. This can now be exited by running:
```
exit()
exit
```

For visualisation, ParaView is the viewer of choice and comes with a connector that can be installed to allow operation with Omniverse. Paraview can be downloaded from [here](paraview.org/download/). ParaView versions 5.9, 5.10 and 5.11 are all currently supported by Omniverse.

Finally, download and install [NVIDIA Omniverse](https://www.nvidia.com/en-sg/omniverse/download/). The extension should work in most apps but to start, Omniverse create is reccommended.

## Extension Download & Testing

Clone the repository with
```
git clone https://github.com/williamjsmith15/OmniFlow
```

After cloning test that all the environments are working so far, this can be done from the main OmniFlow directory with the following commands:
```
python test/cwltool_test.py [CREATE THESE TEST MODULES]
python test/toil_test.py
```
verify that there are no errors in the terminal output and see that the output files are correctly saved in the folders /test/cwltool/toy/ /test/cwltool/simple/ /test/toil/toy/ /test/toil/simple/ and the vtk files in the simple tests can both be opened in ParaView to visually test and to check correct install of ParaView [SCREENSHOTS]


## Connect Extension to Omniverse

Open -> Extension Manager -> blah balh blah

TODO:
    Screenshots for everything
    Create test modules
    Create a win and linux file to autoinstall most things