# Short python script to obtain materials from a list given by MOAB using mbsize command
import os

sep = os.sep
path_py = os.path.realpath(__file__)
list_path = ''

if "MScDIssertation" in path_py:
    cwl_folder = path_py.split(f"{sep}MScDIssertation", 1)[0]
elif "cwl" in path_py:
    cwl_folder = path_py.split(f"{sep}cwl", 1)[0]

for root, dirs, files in os.walk(cwl_folder):
    for file in files:
        if file.endswith("mat_list.txt"):
            list_path = os.path.join(root, file)


mats = []
check_str = 'NAME = mat:'

with open(list_path) as old, open('materials.txt', 'w') as new:
    for line in old: # Loop through lines in old txt
        if check_str in line: # check against check string
            if not any(material in line for material in mats): # check against existing materials
                new.write(line.replace('NAME = mat:', ''))


