__all__ = ["Window"]

import omni.ui as ui
from .functions import *
from .ui_helpers import *
import numpy as np
import os

LABEL_WIDTH = 120
SPACING = 4

default_dict = {
    'sources'       : [],
    'materials'     : [],

    # Run settings
    'batches'       : 0,
    'particles'     : 0,
    'run_mode'      : 'fixed source',

    # All system / extension settings
    'num_sources'   : 1,
    'source_type'   : 'Point Source', # 0=point, 1=plasma
    'up_axis'       : 'Z', # 0=X 1=Y 2=Z
    'test_dropdown' : False,
    'mats_dropdown' : False,
    'sets_dropdown' : True,
    'srcs_dropdown' : False
}
class Window(ui.Window):
    """The class that represents the window"""

    # Create dict to store variables
    settings_dict = default_dict
    previous_settings = default_dict

    # Options for dropdowns
    run_type_options = np.array(['fixed source','eigenvalue','volume','plot','particle restart'])
    source_type_options = np.array(['Point Source', 'Fusion Point Source', 'Fusion Ring Source', 'Tokamak Source'])
    up_axis_choice = np.array(['X','Y','Z'])

    def __init__(self, title: str, delegate=None, **kwargs):
        self.__label_width = LABEL_WIDTH

        super().__init__(title, **kwargs)

        # Set the function that is called to build widgets when the window is
        # visible
        self.frame.set_build_fn(self._build_fn)

    def destroy(self):
        # It will destroy all the children
        super().destroy()

    @property
    def label_width(self):
        """The width of the attribute label"""
        return self.__label_width

    @label_width.setter
    def label_width(self, value):
        """The width of the attribute label"""
        self.__label_width = value
        self.frame.rebuild()

    ##########################
    # --- BUILD FRAMES ---
    ##########################

    def _build_run(self):
        # Build the widgets of the Run group 
        with ui.VStack(height=0, spacing=SPACING):
            ui.Label("OpenMC Workflow Run and Settings")
            ui.Button("Run Workflow", clicked_fn=lambda: self._run_workflow_button())
            ui.Button("Save State", clicked_fn=lambda: self._save_state_button())

            self.settings_dict['test_dropdown'] = ui.CollapsableFrame("Test", collapsed = t_f(self.previous_settings['test_dropdown']))
            with self.settings_dict['test_dropdown']:

                with ui.HStack():
                    ui.Button("Run Toy Test", clicked_fn=lambda: toy_test())
                    ui.Button("Run Simple CAD Test", clicked_fn=lambda: simple_CAD_test())

    def _build_materials(self):
        # Takes the material.txt file and reads all the material names into teh materails list

        mat_file_path = f"{paths['output_omni']}{sep}materials.txt"
        materials = []
        if os.path.exists(mat_file_path):
            with open(mat_file_path) as file:
                for line in file:
                    materials.append(line)

        # Build the widgets of the Materials
        self.settings_dict['mats_dropdown'] = ui.CollapsableFrame("Materials", collapsed = t_f(self.previous_settings['mats_dropdown']))
        with self.settings_dict['mats_dropdown']:

            with ui.VStack(height=0, spacing=SPACING):
                ui.Button("Get Materials", clicked_fn=lambda: self._save_state_button(get_mats=True))
                # Uses the materials list to create a stack of materials to edit properties
                self.settings_dict['materials'] = []

                for i in range(len(self.previous_settings['materials'])):
                    self.settings_dict['materials'].append([None]*3)
                    self.settings_dict['materials'][i][0] = self.previous_settings['materials'][i][0]
                    with ui.HStack(spacing = SPACING):
                        ui.Label(self.previous_settings['materials'][i][0], width=self.label_width)

                        ui.Label("Element")
                        self.settings_dict['materials'][i][1] = ui.StringField().model
                        if str(self.previous_settings['materials'][i][1]) != 'None':
                            self.settings_dict['materials'][i][1].set_value(str(self.previous_settings['materials'][i][1]))

                        # ui.Label("Atom Percent", width=self.label_width)
                        # tmp_array[1] = ui.FloatField().model

                        ui.Label("Density (g/cm^3)")
                        self.settings_dict['materials'][i][2] = ui.FloatField().model
                        self.settings_dict['materials'][i][2].set_value(str(self.previous_settings['materials'][i][2]))

    def _build_sources(self):
        self.settings_dict['srcs_dropdown'] = ui.CollapsableFrame("Sources", collapsed = t_f(self.previous_settings['srcs_dropdown']))
        with self.settings_dict['srcs_dropdown']:
            with ui.VStack(height=0, spacing=SPACING):

                with ui.HStack():
                    ui.Label("Source Type", width=self.label_width)
                    self.settings_dict['source_type'] = MinimalModel(items=self.source_type_options, value=int(np.where(self.source_type_options==str(self.previous_settings['source_type']))[0]))
                    ui.ComboBox(self.settings_dict['source_type'])
                    ui.Button("Enter", clicked_fn=lambda: self._save_state_button())

                with ui.HStack():
                    ui.Label("Number of Sources", width=self.label_width)
                    self.settings_dict['num_sources'] = ui.IntField().model
                    self.settings_dict['num_sources'].set_value(int(self.previous_settings['num_sources']))
                    ui.Button("Enter", clicked_fn=lambda: self._save_state_button())

                # Point source case
                if self.settings_dict['source_type'].get_item_value_model(None, 1).get_value_as_int() == 0: 
                    self.settings_dict['sources'] = []
                    for i in range(int(self.previous_settings['num_sources'])):
                        self.settings_dict['sources'].append([None]*4)
                        
                        with ui.VStack(height=0, spacing=SPACING):
                            with ui.HStack(spacing=SPACING):

                                ui.Label(f"Source {i+1}", width=self.label_width)
                                ui.Label("Energy:", width=self.label_width)
                                self.settings_dict['sources'][i][0] = ui.FloatField().model
                                ui.Label("Location:", width=self.label_width)
                                self.settings_dict['sources'][i][1] = ui.FloatField().model
                                self.settings_dict['sources'][i][2] = ui.FloatField().model
                                self.settings_dict['sources'][i][3] = ui.FloatField().model
                                
                                try:
                                    self.settings_dict['sources'][i][0].set_value(float(self.previous_settings['sources'][i][0]))
                                    self.settings_dict['sources'][i][1].set_value(float(self.previous_settings['sources'][i][1]))
                                    self.settings_dict['sources'][i][2].set_value(float(self.previous_settings['sources'][i][2]))
                                    self.settings_dict['sources'][i][3].set_value(float(self.previous_settings['sources'][i][3]))
                                except: # Handling of sources that don't have data
                                    print(f"No source data found for source {i+1}")

                # Fusion Point Source Case
                elif self.settings_dict['source_type'].get_item_value_model(None, 1).get_value_as_int() == 1: 
                    self.settings_dict['sources'] = []
                    for i in range(int(self.previous_settings['num_sources'])):
                        self.settings_dict['sources'].append([None]*5)
                        with ui.HStack(spacing=SPACING):
                            ui.Label(f"Source {i+1}", width=self.label_width)

                        with ui.HStack(spacing=SPACING):
                            ui.Label("Fuel Type (DT, DD)", width=self.label_width)
                            self.settings_dict['sources'][i][4] = ui.StringField().model
                            ui.Label("Temoerature (eV)", width=self.label_width)
                            self.settings_dict['sources'][i][3] = ui.FloatField().model

                        with ui.HStack(spacing=SPACING):
                            ui.Label("Coordinate:")
                            ui.Label("x")
                            self.settings_dict['sources'][i][0] = ui.FloatField().model
                            ui.Label("y")
                            self.settings_dict['sources'][i][1] = ui.FloatField().model
                            ui.Label("z")
                            self.settings_dict['sources'][i][2] = ui.FloatField().model

                        for j in range(5):
                            try:
                                if j == 4:
                                    self.settings_dict['sources'][i][j].set_value(str(self.previous_settings['sources'][i][j]))
                                else:
                                    self.settings_dict['sources'][i][j].set_value(float(self.previous_settings['sources'][i][j]))
                            except: # Handling of sources that don't have data
                                print(f"No float data found for source {i+1}")

                
                # Fusion Ring Source Case
                elif self.settings_dict['source_type'].get_item_value_model(None, 1).get_value_as_int() == 2: 
                    self.settings_dict['sources'] = []
                    for i in range(int(self.previous_settings['num_sources'])):
                        self.settings_dict['sources'].append([None]*6)
                        with ui.HStack(spacing=SPACING):
                            ui.Label(f"Source {i+1}", width=self.label_width)
                            ui.Label("Radius (inside, cm)", width=self.label_width)
                            self.settings_dict['sources'][i][0] = ui.FloatField().model
                            

                        with ui.HStack(spacing=SPACING):
                            ui.Label("Angle (deg) start:", width=self.label_width)
                            self.settings_dict['sources'][i][2] = ui.FloatField().model
                            ui.Label("end:")
                            self.settings_dict['sources'][i][3] = ui.FloatField().model
                            ui.Label("Temp (eV)")
                            self.settings_dict['sources'][i][4] = ui.FloatField().model

                        with ui.HStack(spacing=SPACING):
                            ui.Label("Fuel Type (DT, DD)")
                            self.settings_dict['sources'][i][1] = ui.StringField().model
                            ui.Label("Vert Offset")
                            self.settings_dict['sources'][i][5] = ui.FloatField().model

                        for j in range(6):
                            try:
                                if j == 1:
                                    self.settings_dict['sources'][i][j].set_value(str(self.previous_settings['sources'][i][j]))
                                else:
                                    self.settings_dict['sources'][i][j].set_value(float(self.previous_settings['sources'][i][j]))
                            except: # Handling of sources that don't have data
                                print(f"No float data found for source {i+1}")


                # Tokamak Source Case
                elif self.settings_dict['source_type'].get_item_value_model(None, 1).get_value_as_int() == 3: 
                    self.settings_dict['sources'] = []
                    for i in range(int(self.previous_settings['num_sources'])):
                        self.settings_dict['sources'].append([None]*19) # TODO: Check 18 is the correct number
                        with ui.HStack(spacing=SPACING):
                            ui.Label(f"Source {i+1}", width=self.label_width)
                            ui.Label("Major Radius (m)", width=self.label_width)
                            self.settings_dict['sources'][i][0] = ui.FloatField().model
                            ui.Label("Minor Radius (m)", width=self.label_width)
                            self.settings_dict['sources'][i][1] = ui.FloatField().model
                            

                        with ui.HStack(spacing=SPACING):
                            ui.Label("Elongation", width=self.label_width)
                            self.settings_dict['sources'][i][2] = ui.FloatField().model
                            ui.Label("Triangularity")
                            self.settings_dict['sources'][i][3] = ui.FloatField().model
                            ui.Label("Confinement Mode (L,H,A)")
                            self.settings_dict['sources'][i][4] = ui.StringField().model

                        with ui.HStack(spacing=SPACING):
                            ui.Label("Ion Density (m^-3) at:")
                            ui.Label("Ion Density Peaking Factor")
                            self.settings_dict['sources'][i][6] = ui.FloatField().model
                        
                        with ui.HStack(spacing=SPACING):
                            ui.Label("Centre", width=self.label_width)
                            self.settings_dict['sources'][i][5] = ui.FloatField().model
                            ui.Label("Pedestal")
                            self.settings_dict['sources'][i][7] = ui.FloatField().model
                            ui.Label("Seperatrix")
                            self.settings_dict['sources'][i][8] = ui.FloatField().model

                        with ui.HStack(spacing=SPACING):
                            ui.Label("Ion Temperature (KeV) at:")
                            ui.Label("Peaking Factor")
                            self.settings_dict['sources'][i][10] = ui.FloatField().model
                            ui.Label("Beta")
                            self.settings_dict['sources'][i][11] = ui.FloatField().model
                        
                        with ui.HStack(spacing=SPACING):
                            ui.Label("Centre", width=self.label_width)
                            self.settings_dict['sources'][i][9] = ui.FloatField().model
                            ui.Label("Pedestal")
                            self.settings_dict['sources'][i][12] = ui.FloatField().model
                            ui.Label("Seperatrix")
                            self.settings_dict['sources'][i][13] = ui.FloatField().model

                        with ui.HStack(spacing=SPACING):
                            ui.Label("Pedestal Raduis (m)", width=self.label_width)
                            self.settings_dict['sources'][i][14] = ui.FloatField().model
                            ui.Label("Shafranov Factor")
                            self.settings_dict['sources'][i][15] = ui.FloatField().model
                            ui.Label("Sample Size")
                            self.settings_dict['sources'][i][18] = ui.FloatField().model

                        with ui.HStack(spacing=SPACING):
                            ui.Label("Angle (deg) start:", width=self.label_width)
                            self.settings_dict['sources'][i][16] = ui.FloatField().model
                            ui.Label("end:")
                            self.settings_dict['sources'][i][17] = ui.FloatField().model

                        for j in range(19):
                            try:
                                if j == 4:
                                    self.settings_dict['sources'][i][j].set_value(str(self.previous_settings['sources'][i][j]))
                                else:
                                    self.settings_dict['sources'][i][j].set_value(float(self.previous_settings['sources'][i][j]))
                            except: # Handling of sources that don't have data
                                print(f"No float data found for source {i+1}")
                        
                else:
                    print('There was an error, unknown source type detected')


    def _build_settings(self):
        # Build the widgets of the Settings group
        self.settings_dict['sets_dropdown'] = ui.CollapsableFrame("Settings", collapsed = t_f(self.previous_settings['sets_dropdown']))

        with self.settings_dict['sets_dropdown']:

            with ui.VStack(height=0, spacing=SPACING):

                with ui.HStack():
                    ui.Label("Batches", width=self.label_width)
                    self.settings_dict['batches'] = ui.IntField().model
                    self.settings_dict['batches'].set_value(int(self.previous_settings['batches']))

                with ui.HStack():
                    ui.Label("Particles", width=self.label_width)
                    self.settings_dict['particles'] = ui.IntField().model
                    self.settings_dict['particles'].set_value(int(self.previous_settings['particles']))

                with ui.HStack():
                    ui.Label("Run Mode", width=self.label_width)
                    self.settings_dict['run_mode'] = MinimalModel(items=self.run_type_options, value=int(np.where(self.run_type_options == self.previous_settings['run_mode'])[0]))
                    ui.ComboBox(self.settings_dict['run_mode'])

                with ui.HStack():
                    ui.Label("Up Axis", width=self.label_width)
                    self.settings_dict['up_axis'] = MinimalModel(items=self.up_axis_choice, value=int(np.where(self.up_axis_choice == self.previous_settings['up_axis'])[0]))
                    ui.ComboBox(self.settings_dict['up_axis'])


    def _build_export(self):
        with ui.VStack(height=0, spacing=SPACING):
            ui.Button("Export USD Stage", clicked_fn=lambda: export_stage())

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is
        visible.
        """
        self.load_state()

        with ui.ScrollingFrame():
            with ui.VStack(height=0):
                self._build_run()
                self._build_materials()
                self._build_sources()
                self._build_settings()
                self._build_export()


    ##########################
    # --- BUTTONS ---
    ##########################

    def _run_workflow_button(self):
        self.generate()
        run_workflow()

    def _save_state_button(self, get_mats=False):
        # Saves the state of the extension
        self.generate(get_mats)

        print('Refreshing screen')
        self.frame.rebuild()

    ##########################
    # --- EXTRA FUNCTIONS ---
    ##########################

    def generate(self, get_mats=False):
    # Converts settings and materials into a txt file for the general CAD py script to use
        print("Saving Materials and Settings")

        already_used_materials = []

        if get_mats:
            materials = get_materials()

        with open(f"{paths['output_omni']}{sep}settings.txt", 'w') as file:
            # Materials
            file.write('MATERIALS\n')
            # count = 0     # DEBUGGING
            if get_mats: # Just write the materials to the settings file, no element or density
                for mat in materials:
                    if mat in already_used_materials:
                        pass
                    else:
                        file.write(f"{mat}")
                        already_used_materials.append(mat)
            else:        # Write the material settings set in omni
                for mat in self.settings_dict['materials']:
                    # count += 1
                    # file.write(f"mesh_{count} Fe 7.7\n")
                    if 'Irangon' in mat[0]:
                        file.write(f"{mat[0].replace(' ', '')} Fe 7.7\n")
                    else:
                        file.write(f"{mat[0].replace(' ', '')} {mat[1].get_value_as_string()} {mat[2].get_value_as_float()}\n")
            
            # Sources
            file.write('SOURCES\n')
            for src in self.settings_dict['sources']:
                tmp_src = []
                for field in src:
                    try: # Basically handles any float or string coming out of the data fields and joins them with a space inbetween each
                        tmp_field = field.get_value_as_float()
                    except:
                        pass
                    try:
                        tmp_field = field.get_value_as_string()
                    except:
                        pass
                    tmp_src.append(str(tmp_field))
                file.write(f"{' '.join(tmp_src)}\n")

            # Settings 
            file.write('SETTINGS\n')
            file.write(f"batches {self.settings_dict['batches'].get_value_as_int()}\n")
            file.write(f"particles {self.settings_dict['particles'].get_value_as_int()}\n")
            file.write(f"run_mode {self.run_type_options[self.settings_dict['run_mode'].get_item_value_model(None, 1).get_value_as_int()]}\n")

            file.write('EXT_SETTINGS\n')
            file.write(f"source_type {self.source_type_options[self.settings_dict['source_type'].get_item_value_model(None, 1).get_value_as_int()]}\n")
            file.write(f"num_sources {self.settings_dict['num_sources'].get_value_as_int()}\n")
            file.write(f"up_axis {self.up_axis_choice[self.settings_dict['up_axis'].get_item_value_model(None, 1).get_value_as_int()]}\n")
            file.write(f"test_dropdown {self.settings_dict['test_dropdown'].collapsed}\n")
            file.write(f"mats_dropdown {self.settings_dict['mats_dropdown'].collapsed}\n")
            file.write(f"sets_dropdown {self.settings_dict['sets_dropdown'].collapsed}\n")
            file.write(f"srcs_dropdown {self.settings_dict['srcs_dropdown'].collapsed}\n")
            

        print("Finished Converting")

    def load_state(self):
        position = 0
        self.previous_settings = {}

        with open(f"{paths['output_omni']}{sep}settings.txt", 'r') as file:
            for line in file:
                split_line = line.split()
                if position == 0:
                    if "MATERIALS" in line:
                        position = 1
                        self.previous_settings['materials'] = []
                elif position == 1:
                    if "SOURCES" in line:
                        position = 2
                        self.previous_settings['sources'] = []
                    else:
                        if len(split_line) == 3:
                            self.previous_settings['materials'].append(split_line)
                        else:
                            self.previous_settings['materials'].append([split_line[0], None, 0.0])
                elif position == 2:
                    if "SETTINGS" in line:
                        position = 3
                    else:
                        self.previous_settings['sources'].append(split_line)
                elif position == 3:
                    if "EXT_SETTINGS" in line:
                        position = 4
                    else:
                        self.previous_settings[split_line[0]] = ' '.join(split_line[1:])
                elif position == 4:
                    self.previous_settings[split_line[0]] = ' '.join(split_line[1:])
                else:
                    print(f'I dont know what position {position} is')
