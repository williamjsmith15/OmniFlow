__all__ = ["Window"]

import omni.ui as ui
from .functions import *
import numpy as np
import os

LABEL_WIDTH = 120
SPACING = 4


class Window(ui.Window):
    """The class that represents the window"""

    # Create dict to store variables
    settings_dict = {
        'sources'       : [],
        'materials'     : [],
        'batches'       : 0,
        'particles'     : 0,
        'run mode'      : 'fixed source'
    }

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

    def _run_workflow_button(self):
        self.generate()
        run_workflow()

    def _build_run(self):
        # Build the widgets of the Run group 
        with ui.VStack(height=0, spacing=SPACING):
            ui.Label("OpenMC Workflow Run and Settings")
            ui.Button("Run Workflow", clicked_fn=lambda: self._run_workflow_button())
            ui.Button("Refresh Screen", clicked_fn=lambda: self.frame.rebuild())
            with ui.CollapsableFrame("Test", collapsed = True):
                with ui.HStack():
                    ui.Button("Run Toy Test", clicked_fn=lambda: toy_test())
                    ui.Button("Run Simple CAD Test", clicked_fn=lambda: simple_CAD_test())

    def _build_materials(self):
        # Takes the material.txt file and reads all the material names into teh materails list
        def _get_materials_button():
            get_materials()
            self.frame.rebuild()

        mat_file_path = f"{paths['output_omni']}{paths['sep']}materials.txt"
        materials = []
        if os.path.exists(mat_file_path):
            with open(mat_file_path) as file:
                for line in file:
                    materials.append(line)

        # Build the widgets of the Materials
        with ui.CollapsableFrame("Materials", collapsed = True):
            with ui.VStack(height=0, spacing=SPACING):
                ui.Button("Get Materials", clicked_fn=lambda: _get_materials_button())
                # Uses the materials list to create a stack of materials to edit properties
                self.settings_dict['materials'] = []
                for material in materials:
                    tmp_array = [None] * 3
                    tmp_array[0] = material
                    with ui.HStack(spacing = SPACING):
                        ui.Label(material, width=self.label_width)
                        ui.Label("Element")
                        tmp_array[1] = ui.StringField().model
                        # ui.Label("Atom Percent", width=self.label_width)
                        # tmp_array[1] = ui.FloatField().model
                        ui.Label("Density (g/cm^3)")
                        tmp_array[2] = ui.FloatField().model
                    self.settings_dict['materials'].append(tmp_array)



    def _build_settings(self):
        # Build the widgets of the Settings group

        def _enter_button():
            settings_enter(self.num_sources_slider.as_int)
            self.frame.rebuild()

        with ui.CollapsableFrame("Settings"):
            with ui.VStack(height=0, spacing=SPACING):

                with ui.HStack():
                    ui.Label("Batches", width=self.label_width)
                    self.settings_dict['batches'] = ui.IntField().model

                with ui.HStack():
                    ui.Label("Particles", width=self.label_width)
                    self.settings_dict['particles'] = ui.IntField().model

                with ui.HStack():
                    ui.Label("Run Mode", width=self.label_width)
                    self.settings_dict['run mode'] = ui.StringField().model

                with ui.HStack():
                    ui.Label("Sources", width=self.label_width)
                    self.num_sources_slider = ui.IntField().model
                    ui.Button("Enter", clicked_fn=lambda: _enter_button())

                num_sources = 0

                if os.path.exists(f"{paths['output_omni']}{paths['sep']}num_sources.txt"):
                    with open(f"{paths['output_omni']}{paths['sep']}num_sources.txt") as file:
                        for line in file:
                            if "num_sources = " in line:
                                tmp = line.replace('num_sources = ', '')
                                num_sources = int(tmp)
                                self.num_sources_slider.set_value(num_sources)
                else:
                    print("Can't find num_sources.txt")

                with ui.CollapsableFrame("Sources", collapsed = True):
                    with ui.VStack(height=0, spacing=SPACING):
                        self.settings_dict['sources'] = []
                        for i in range(1, num_sources + 1):
                            tmp_array = [None] * 4
                            with ui.VStack(height=0, spacing=SPACING):
                                with ui.HStack(spacing=SPACING):
                                    ui.Label(f"Source {i}", width=self.label_width)
                                    ui.Label("Energy:", width=self.label_width)
                                    tmp_array[0] = ui.FloatField().model
                                    ui.Label("Location:", width=self.label_width)
                                    tmp_array[1] = ui.FloatField().model
                                    tmp_array[2] = ui.FloatField().model
                                    tmp_array[3] = ui.FloatField().model
                            self.settings_dict['sources'].append(tmp_array)

    def generate(self):
        #Something to convert settings and materials into a txt file for the general CAD py script to use

        print("Converting Materials and Settings")

        with open(f"{paths['output_omni']}{paths['sep']}settings.txt", 'w') as file:
            # Materials
            file.write('MATERIALS\n')
            for mat in self.settings_dict['materials']:
                file.write(f"{mat[0].replace(' ', '')[:-1]} {mat[1].get_value_as_string()} {mat[2].get_value_as_float()}\n")
            # Sources
            file.write('SOURCES\n')
            for src in self.settings_dict['sources']:
                file.write(f"{src[0].get_value_as_float()} {src[1].get_value_as_float()} {src[2].get_value_as_float()} {src[3].get_value_as_float()}\n")
            # Settings 
            file.write('SETTINGS\n')
            file.write(f"batches {self.settings_dict['batches'].get_value_as_int()}\n")
            file.write(f"particles {self.settings_dict['particles'].get_value_as_int()}\n")
            file.write(f"run_mode {self.settings_dict['run mode'].get_value_as_string()}\n")
        print("Finished Converting")

    def _build_generate(self):
        with ui.VStack(height=0, spacing=SPACING):
            ui.Button("Generate Files", clicked_fn=lambda: self.generate())

    def _build_export(self):
        with ui.VStack(height=0, spacing=SPACING):
            ui.Button("Export USD Stage", clicked_fn=lambda: export_stage())

    def _build_fn(self):
        """
        The method that is called to build all the UI once the window is
        visible.
        """
        with ui.ScrollingFrame():
            with ui.VStack(height=0):
                self._build_run()
                self._build_materials()
                self._build_settings()
                self._build_generate()
                self._build_export()

    
