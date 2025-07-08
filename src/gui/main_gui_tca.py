# -*- coding: utf-8 -*-

import os
import re
import json
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.font as tkFont
from datetime import datetime

# Verifica a variável de ambiente DEBUG_MODE
debug_mode = os.getenv("DEBUG_MODE") == "True"

if debug_mode:
    from functions.clear_form import clear_form
    from functions.notdone import notdone
    from functions.open_file import open_file
    from functions.quit_app import quit_app
    from functions.save_as_file import save_as_file
    from functions.save_file import save_file
    from functions.write_param_file import write_param_file
    from functions.validate_entry import validate_entry
    from functions.convert_to_si import convert_to_si
else:
    from gui.functions.clear_form import clear_form
    from gui.functions.notdone import notdone
    from gui.functions.open_file import open_file
    from gui.functions.quit_app import quit_app
    from gui.functions.save_as_file import save_as_file
    from gui.functions.save_file import save_file
    from gui.functions.write_param_file import write_param_file
    from gui.functions.validate_entry import validate_entry
    from gui.functions.convert_to_si import convert_to_si


class FormData:
    def __init__(self):
        self.data = {}

class MainForm:
    """
    Classe que cria uma interface gráfica para entrada de dados de propriedades do
    Conjunto da Câmara de Empuxo (Thrust Chamber Assemble, TCA)
    utilizando a biblioteca tkinter.
    """

    def notdone(self):
        showerror('Not implemented', 'Not yet available')

    def makemenu(self, root):
        menubar = Menu(root)
        root.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu, underline=0)
        filemenu.add_command(label="New...", command=self.new_file, underline=0, accelerator="Ctrl+N")
        filemenu.add_command(label="Open...", command=self.open_file, underline=0, accelerator="Ctrl+O")
        filemenu.add_command(label="Save", command=self.save_file, underline=0, accelerator="Ctrl+S")
        filemenu.add_command(label="Save As...", command=self.save_as_file, underline=5)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.quit_app, underline=0, accelerator="Ctrl+Q")

        root.bind_all("<Control-n>", lambda event: self.new_file())
        root.bind_all("<Control-o>", lambda event: self.open_file())
        root.bind_all("<Control-s>", lambda event: self.save_file())
        root.bind_all("<Control-q>", lambda event: self.quit_app())

        return menubar

    def new_file(self):
        if messagebox.askyesno("New File", "Do you want to clear all fields?"):
            self.form_data.data = {}
            self.clear_form()
        else:
            messagebox.showinfo("Info", "Data not changed")

    def quit_app(self):
        if messagebox.askyesno("Quit", "Do you want to exit the application?"):
            self.root.quit()

    def open_file(self):
        file_path = askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.form_data.data = json.load(file)
                self.file_path = file_path
                self.populate_form()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        if hasattr(self, 'file_path') and self.file_path:
            try:
                self.process_form(save_only=True)
                with open(self.file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.form_data.data, file, ensure_ascii=False, indent=4)
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            self.file_path = file_path
            self.save_file()

    def clear_form(self):
        for field, entry in self.entries.items():
            if isinstance(entry, StringVar):
                entry.set("")
            elif isinstance(entry, ttk.Combobox):
                if '_unit' not in field and entry.cget('state') != 'readonly':
                    entry.set("")

        # Definir valores padrão para os comboboxes específicos
        self.entries['Nozzle shape'].set('Profiled')
        self.entries['Cooling channel shape'].set('Rectangle')
        self.entries['Combustion chamber shape'].set('Cylindrical')

    def populate_form(self):
        for field, value in self.form_data.data.items():
            entry = self.entries.get(field)
            if entry:
                entry.set(value)
        # Preenche os campos de unidade também, se necessário
        for field, unit in self.entries.items():
            if field.endswith('_unit'):
                main_field = field.replace('_unit', '')
                if main_field in self.form_data.data:
                    unit.set(self.form_data.data.get(f"{main_field}_unit", unit.get()))

    def __init__(self, root, testing=False):
        self.root = root
        self.testing = testing
        self.file_path = None
        self.root.title("Propulsion Library proplib - Thrust Chamber Assembly (TCA) Cooling")
        self.form_data = FormData()  # Instancia a classe FormData

        # Criação do menu
        self.makemenu(root)

        self.entries = {}
        self.numeric_fields = {
            'Oxidizer inlet temperature in the thrust chamber',
            'Initial guess for ethanol inlet temperature in injectors',
            'Design vacuum thrust',
            'Design chamber pressure',
            'Pressure ratio at the nozzle exit to chamber',
            'Global mixture ratio (O/F)',
            'Wall layer mixture ratio (O/F in outer layer injectors)',
            'Fraction of total flow injected in the wall layer',
            'Fraction of total flow directed to fuel film',
            'Minimum specific impulse at sea level',
            'Minimum specific impulse in vacuum',
            'Estimated expansion efficiency',
            'Estimated combustion efficiency (c*)',
            'Maximum exit diameter',
            'Diameter of the cylindrical section of the combustion chamber',
            'Gas residence time in the combustion chamber',
            'Characteristic length',
            'Maximum characteristic length - Dobrovolskiy',
            'Minimum characteristic length - Dobrovolskiy',
            'Compression ratio (cylindrical/throat)',
            'Inclination angle of the conical profile, if any',
            'Ratio between the radius of smoothing of the divergent and the radius of the cylindrical part',
            'Maximum thrust chamber length',
            'Number of coordinates (x, r) of the contour',
            'Ratio between the radius of the low pressure convergent and the throat diameter',
            'Ratio between the radius of the high pressure convergent and the diameter of the cylindrical part',
            'Tolerance for convergence of the initial slope of the nozzle (beta_m)',
            'Tolerance for convergence of the slope of the nozzle (beta)'
        }

        self.units_general = {
            'Oxidizer inlet temperature in the thrust chamber': ['K', '°C', '°F'],
            'Initial guess for ethanol inlet temperature in injectors': ['K', '°C', '°F'],
            'Design vacuum thrust': ['N', 'lbf'],
            'Design chamber pressure': ['Pa', 'psi'],
            'Pressure ratio at the nozzle exit to chamber': [],
            'Global mixture ratio (O/F)': [],
            'Wall layer mixture ratio (O/F in outer layer injectors)': [],
            'Fraction of total flow injected in the wall layer': [],
            'Fraction of total flow directed to fuel film': [],
            'Minimum specific impulse at sea level': ['s'],
            'Minimum specific impulse in vacuum': ['s'],
            'Estimated expansion efficiency': [],
            'Estimated combustion efficiency (c*)': []
        }

        self.units_geometric = {
            'Maximum exit diameter': ['m', 'in'],
            'Diameter of the cylindrical section of the combustion chamber': ['m', 'in'],
            'Gas residence time in the combustion chamber': ['s'],
            'Characteristic length': ['m', 'ft'],
            'Maximum characteristic length - Dobrovolskiy': ['m', 'ft'],
            'Minimum characteristic length - Dobrovolskiy': ['m', 'ft'],
            'Compression ratio (cylindrical/throat)': [],
            'Inclination angle of the conical profile, if any': ['rad', 'deg'],
            'Ratio between the radius of smoothing of the divergent and the radius of the cylindrical part': [],
            'Maximum thrust chamber length': ['m', 'ft'],
            'Number of coordinates (x, r) of the contour': [],
            'Ratio between the radius of the low pressure convergent and the throat diameter': [],
            'Ratio between the radius of the high pressure convergent and the diameter of the cylindrical part': [],
            'Tolerance for convergence of the initial slope of the nozzle (beta_m)': [],
            'Tolerance for convergence of the slope of the nozzle (beta)': ['m', 'ft']
        }

        self.units_mesh = {
            'Number of mesh elements in the cylindrical section before the flame front': [],
            'Number of mesh elements in the cylindrical section after the flame front': [],
            'Number of mesh elements in the divergent jacket': [],
            'Number of mesh elements in the divergent not covered by the jacket': []
        }

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox", fieldbackground="white", background="white", justify="left")

        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.page_general = Frame(self.notebook)
        self.page_geometric = Frame(self.notebook)
        self.page_injectors = Frame(self.notebook)
        self.page_jacket = Frame(self.notebook)
        self.page_mesh = Frame(self.notebook)
        self.page_plot = Frame(self.notebook)

        self.notebook.add(self.page_general, text="General parameters")
        self.notebook.add(self.page_geometric, text="Geometric parameters")
        self.notebook.add(self.page_injectors, text="Injectors data")
        self.notebook.add(self.page_jacket, text="TCA Cooling")
        self.notebook.add(self.page_mesh, text="Mesh refinement")
        self.notebook.add(self.page_plot, text="Plot settings")

        self.create_form()

        # Adicionando expansão para preencher a janela maximizada
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.notebook.grid(row=0, column=0, sticky='nsew')

    def create_method_frame(self, parent, title, list_values, row, col=0):
        frame = Frame(parent, borderwidth=0, relief="flat")
        frame.grid(row=row, column=col, pady=2, padx=2, sticky="w")

        frame_title = Label(frame, text=title, anchor='w')
        frame_title.grid(row=0, column=0, padx=5, pady=(0, 2))

        var = StringVar()
        combobox = ttk.Combobox(frame, textvariable=var, values=list_values, state="readonly", style="TCombobox", justify='left')
        combobox.grid(row=0, column=1, padx=5, pady=(0, 2), sticky="w")
        
        self.adjust_combobox_width(combobox, list_values)

        self.entries[title] = var
        return var, frame

    def create_numeric_entry(self, parent, title, row, default_value="", col=0, units=None):
        label = Label(parent, text=title, anchor='w')
        label.grid(row=row, column=col, padx=5, pady=2, sticky='w')
        var = StringVar(value=default_value)
        entry = Entry(parent, textvariable=var, validate='key', validatecommand=(self.root.register(self.validate_entry), '%P', title), justify="right")
        entry.grid(row=row, column=col+1, padx=5, pady=2, sticky='ew')
        self.entries[title] = var
        if units:
            unit_combobox = ttk.Combobox(parent, values=units, state="readonly", width=10, justify='left')
            unit_combobox.set(units[0])
            unit_combobox.grid(row=row, column=col+2, padx=5, pady=2, sticky='w')
            self.entries[f"{title}_unit"] = unit_combobox
        return var

    def create_form(self):
        # Criar os componentes do formulário aqui
        frame_engine_file_name = Frame(self.page_general, borderwidth=2, relief="groove")
        frame_engine_file_name.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        frame_engine_file_name_title = Label(frame_engine_file_name, text="Engine/File name", anchor='w')
        frame_engine_file_name_title.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

        self.var_engine_file_name = self.create_numeric_entry(frame_engine_file_name, "Engine/File name", row=1, default_value="")
        self.var_description = self.create_numeric_entry(frame_engine_file_name, "Description", row=2, default_value="")

        frame_mixture = Frame(self.page_general, borderwidth=2, relief="groove")
        frame_mixture.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        frame_mixture_title = Label(frame_mixture, text="Mixture", anchor='w')
        frame_mixture_title.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

        self.var_oxidant, frame_oxidant = self.create_method_frame(frame_mixture, "Oxidant", [
            'Nitric acid',
            'Liquid oxygen (LOx)'
        ], row=1)

        self.var_fuel, frame_fuel = self.create_method_frame(frame_mixture, "Fuel", [
            'Tonka 250',
            'Ethanol'
        ], row=2)

        frame_combustion_nozzle = Frame(self.page_general, borderwidth=2, relief="groove")
        frame_combustion_nozzle.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        frame_combustion_nozzle_title = Label(frame_combustion_nozzle, text="Combustion chamber shape", anchor='w')
        frame_combustion_nozzle_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="w")

        Label(frame_combustion_nozzle, text="Combustion chamber shape:", anchor='w').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.var_combustion_chamber_shape, frame_combustion = self.create_method_frame(frame_combustion_nozzle, "", [
            'Cylindrical',
            'Semithermal',
            'Spherical',
            'Conical',
            'Annular'
        ], row=1, col=1)
        self.var_combustion_chamber_shape.set('Cylindrical')

        combustion_chamber_image = Label(frame_combustion_nozzle, text="Combustion chamber shape image here", anchor='w', relief="solid", width=30, height=5)
        combustion_chamber_image.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        frame_nozzle = Frame(self.page_general, borderwidth=2, relief="groove")
        frame_nozzle.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        frame_nozzle_title = Label(frame_nozzle, text="Nozzle shape", anchor='w')
        frame_nozzle_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="w")

        Label(frame_nozzle, text="Nozzle shape:", anchor='w').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.var_nozzle_shape, frame_nozzle_inner = self.create_method_frame(frame_nozzle, "", [
            'Conical',
            'Profiled',
            'With angular entrance',
            'Annular',
            'Full full external expansion',
            'With partial internal expansion',
            'Plate with free internal expansion'
        ], row=1, col=1)
        self.var_nozzle_shape.set('Profiled')

        nozzle_shape_image = Label(frame_nozzle, text="Nozzle shape image here", anchor='w', relief="solid", width=30, height=5)
        nozzle_shape_image.grid(row=1, column=2, padx=5, pady=5, sticky='w')

        frame_variables_geometric = Frame(self.page_geometric, borderwidth=2, relief="groove")
        frame_variables_geometric.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        frame_variables_geometric_title = Label(frame_variables_geometric, text="Variables", anchor='w')
        frame_variables_geometric_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="w")

        self.var_max_diameter = self.create_numeric_entry(frame_variables_geometric, "Maximum exit diameter", row=1, default_value="", units=self.units_geometric['Maximum exit diameter'])
        self.var_cylinder_diameter = self.create_numeric_entry(frame_variables_geometric, "Diameter of the cylindrical section of the combustion chamber", row=2, default_value="", units=self.units_geometric['Diameter of the cylindrical section of the combustion chamber'])
        self.var_residence_time = self.create_numeric_entry(frame_variables_geometric, "Gas residence time in the combustion chamber", row=3, default_value="", units=self.units_geometric['Gas residence time in the combustion chamber'])
        self.var_characteristic_length = self.create_numeric_entry(frame_variables_geometric, "Characteristic length", row=4, default_value="", units=self.units_geometric['Characteristic length'])
        self.var_max_characteristic_length = self.create_numeric_entry(frame_variables_geometric, "Maximum characteristic length - Dobrovolskiy", row=5, default_value="", units=self.units_geometric['Maximum characteristic length - Dobrovolskiy'])
        self.var_min_characteristic_length = self.create_numeric_entry(frame_variables_geometric, "Minimum characteristic length - Dobrovolskiy", row=6, default_value="", units=self.units_geometric['Minimum characteristic length - Dobrovolskiy'])
        self.var_compression_ratio = self.create_numeric_entry(frame_variables_geometric, "Compression ratio (cylindrical/throat)", row=7, default_value="")
        self.var_conical_profile_angle = self.create_numeric_entry(frame_variables_geometric, "Inclination angle of the conical profile, if any", row=8, default_value="", units=self.units_geometric['Inclination angle of the conical profile, if any'])
        self.var_smoothing_radius_ratio = self.create_numeric_entry(frame_variables_geometric, "Ratio between the radius of smoothing of the divergent and the radius of the cylindrical part", row=9, default_value="")
        self.var_max_chamber_length = self.create_numeric_entry(frame_variables_geometric, "Maximum thrust chamber length", row=10, default_value="", units=self.units_geometric['Maximum thrust chamber length'])
        self.var_num_coordinates = self.create_numeric_entry(frame_variables_geometric, "Number of coordinates (x, r) of the contour", row=11, default_value="")
        self.var_low_pressure_convergent_ratio = self.create_numeric_entry(frame_variables_geometric, "Ratio between the radius of the low pressure convergent and the throat diameter", row=12, default_value="")
        self.var_high_pressure_convergent_ratio = self.create_numeric_entry(frame_variables_geometric, "Ratio between the radius of the high pressure convergent and the diameter of the cylindrical part", row=13, default_value="")
        self.var_tolerance_initial_slope = self.create_numeric_entry(frame_variables_geometric, "Tolerance for convergence of the initial slope of the nozzle (beta_m)", row=14, default_value="")
        self.var_tolerance_slope = self.create_numeric_entry(frame_variables_geometric, "Tolerance for convergence of the slope of the nozzle (beta)", row=15, default_value="", units=self.units_geometric['Tolerance for convergence of the slope of the nozzle (beta)'])

        self.var_temp_ox = self.create_numeric_entry(frame_variables_geometric, "Oxidizer inlet temperature in the thrust chamber", row=16, default_value="", units=self.units_general['Oxidizer inlet temperature in the thrust chamber'])
        self.var_temp_fuel = self.create_numeric_entry(frame_variables_geometric, "Initial guess for ethanol inlet temperature in injectors", row=17, default_value="", units=self.units_general['Initial guess for ethanol inlet temperature in injectors'])
        self.var_thrust = self.create_numeric_entry(frame_variables_geometric, "Design vacuum thrust", row=18, default_value="", units=self.units_general['Design vacuum thrust'])
        self.var_chamber_pressure = self.create_numeric_entry(frame_variables_geometric, "Design chamber pressure", row=19, default_value="", units=self.units_general['Design chamber pressure'])
        self.var_pressure_ratio = self.create_numeric_entry(frame_variables_geometric, "Pressure ratio at the nozzle exit to chamber", row=20, default_value="")
        self.var_km_global = self.create_numeric_entry(frame_variables_geometric, "Global mixture ratio (O/F)", row=21, default_value="")
        self.var_km_wall_layer = self.create_numeric_entry(frame_variables_geometric, "Wall layer mixture ratio (O/F in outer layer injectors)", row=22, default_value="")
        self.var_flow_fraction_wall_layer = self.create_numeric_entry(frame_variables_geometric, "Fraction of total flow injected in the wall layer", row=23, default_value="")
        self.var_flow_fraction_fuel_film = self.create_numeric_entry(frame_variables_geometric, "Fraction of total flow directed to fuel film", row=24, default_value="")
        self.var_specific_impulse_at_sea_level = self.create_numeric_entry(frame_variables_geometric, "Minimum specific impulse at sea level", row=25, default_value="", units=self.units_general['Minimum specific impulse at sea level'])
        self.var_specific_impulse_in_vacuum = self.create_numeric_entry(frame_variables_geometric, "Minimum specific impulse in vacuum", row=26, default_value="", units=self.units_general['Minimum specific impulse in vacuum'])
        self.var_expansion_efficiency = self.create_numeric_entry(frame_variables_geometric, "Estimated expansion efficiency", row=27, default_value="")
        self.var_combustion_efficiency = self.create_numeric_entry(frame_variables_geometric, "Estimated combustion efficiency (c*)", row=28, default_value="")

        frame_variables_injectors = Frame(self.page_injectors, borderwidth=2, relief="groove")
        frame_variables_injectors.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        frame_variables_injectors_title = Label(frame_variables_injectors, text="Variables", anchor='w')
        frame_variables_injectors_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="w")

        self.var_num_fuel_injectors = self.create_numeric_entry(frame_variables_injectors, "Number of fuel injectors", row=1, default_value="")
        self.var_num_oxidizer_injectors = self.create_numeric_entry(frame_variables_injectors, "Number of oxidizer injectors", row=2, default_value="")

        frame_sections = Frame(self.page_jacket, borderwidth=2, relief="groove")
        frame_sections.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        frame_sections_title = Label(frame_sections, text="Combustion chamber and nozzle sections", anchor='w')
        frame_sections_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="w")

        self.var_chamber_sections = self.create_numeric_entry(frame_sections, "Combustion chamber sections", row=1, default_value="")
        self.var_nozzle_sections = self.create_numeric_entry(frame_sections, "Nozzle sections", row=2, default_value="")

        frame_method = Frame(self.page_jacket, borderwidth=2, relief="groove")
        frame_method.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        frame_method_title = Label(frame_method, text="Method", anchor='w')
        frame_method_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="w")

        self.var_convective_heat_desired_method, frame_convective_heat = self.create_method_frame(frame_method, "Convective heat desired method", [
            'A. P. Vasiliev and V. M. Kudryavtsev (1993)',
            'A. R. Poliaskiy',
            'M. V. Dobrovolskiy (1968)',
            'M. V. Dobrovolskiy (1968) (s1)',
            'M. V. Dobrovolskiy (1968) (s2)',
            'M. V. Dobrovolskiy (1968) (2)',
            'J. V. Kessaev (1997)',
            'Kudryavtsev',
            'Bartz'
        ], row=1)

        self.var_radiative_heat_desired_method, frame_radiative_heat = self.create_method_frame(frame_method, "Radiative heat desired method", [
            'A. P. Vasiliev and V. M. Kudryavtsev (1993)',
            'A. R. Poliaskiy',
            'M. V. Dobrovolskiy (1968)',
            'M. V. Dobrovolskiy (1968) (s1)',
            'M. V. Dobrovolskiy (1968) (s2)',
            'M. V. Dobrovolskiy (1968) (2)',
            'J. V. Kessaev (1997)',
            'Kudryavtsev',
            'Bartz'
        ], row=2)

        self.var_case, frame_case = self.create_method_frame(frame_method, "Case", [
            'Without film, no external radioactive',
            'Without film, with external radioactive',
            'With film (with or without external radioactive)'
        ], row=3)

        frame_cooling_channel = Frame(self.page_jacket, borderwidth=2, relief="groove")
        frame_cooling_channel.grid(row=2, column=0, pady=10, padx=10, sticky="w")

        frame_cooling_channel_title = Label(frame_cooling_channel, text="Cooling channel shape", anchor='w')
        frame_cooling_channel_title.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="w")

        cooling_channel_var = StringVar()
        cooling_channel_combobox = ttk.Combobox(frame_cooling_channel, textvariable=cooling_channel_var, values=sorted([
            'Obround (or racetrack shape)',
            'Ovoid',
            'Circular crown',
            'Parallelogram',
            'Circumference',
            'Rectangle',
            'Hexagon',
            'Square',
            'Ellipse',
            'Diamond',
            'Rectangle triangle',
            'Circular_sector',
            'Trapezium',
            'Equilateral triangle',
            'Circular crown arch'
        ]), state="readonly", style="TCombobox", justify='left')
        cooling_channel_combobox.grid(row=0, column=1, padx=5, pady=(0, 5), sticky="w")
        self.adjust_combobox_width(cooling_channel_combobox, cooling_channel_combobox['values'])
        self.entries["Cooling channel shape"] = cooling_channel_var
        cooling_channel_var.set('Rectangle')  # Definindo o valor-padrão

        cooling_channel_image = Label(frame_cooling_channel, text="Cooling channel shape image here", anchor='w', relief="solid", width=30, height=5)
        cooling_channel_image.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        frame_variables = Frame(self.page_jacket, borderwidth=2, relief="groove")
        frame_variables.grid(row=3, column=0, pady=10, padx=10, sticky="w")

        frame_variables_title = Label(frame_variables, text="Variables", anchor='w')
        frame_variables_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="w")

        variables = [
            'Fuel injector pressure loss',  # 5e5
            'Wall thickness vector',  # Vetor (lista), 1e-3
            'Outer wall thickness vector',  # Vetor (lista), 1e-3
            'Gas side effective temperature',  # 1000.
            'Convective heat flux base',  # Vector (lista)
            'Gas side wall temperature',  # Vetor
            'Gas pressure',  # Vector
            'Gas pressure threshold for sea level test',  # Vetor (lista)
            'Temperature of the wall gas (t_wall_gas) vector',  #,
            'Thermo complex base',
            'Thermo complex auxiliary parameter',
            'Radiative nozzle wall material',
            'Radiative nozzle wall material details',
            'Dissociated gas temperature',
            'Dissociated gas viscosity',
            'Non-dissociated gas constant',
            'Radiative heat flux',
            'Radiative nozzle outer wall temperature',
            'Radiative nozzle wall thickness'
        ]

        variables_values = {
            'Fuel injector pressure loss': '500000',
            'Wall thickness vector': '0.001',
            'Outer wall thickness vector': '0.001',
            'Gas side effective temperature': '1000',
            'Convective heat flux base': '1000',
            'Gas side wall temperature': '800',
            'Gas pressure': '101325',
            'Gas pressure threshold for sea level test': '101325',
            'Temperature of the wall gas (t_wall_gas) vector': '700',
            'Thermo complex base': '',
            'Thermo complex auxiliary parameter': '1',
            'Radiative nozzle wall material': '',
            'Radiative nozzle wall material details': '',
            'Dissociated gas temperature': '',
            'Dissociated gas viscosity': '',
            'Non-dissociated gas constant': '',
            'Radiative heat flux': '',
            'Radiative nozzle outer wall temperature': '',
            'Radiative nozzle wall thickness': '0'
        }

        units = {
            'Fuel injector pressure loss': ['Pa', 'psi'],
            'Wall thickness vector': ['m', 'in'],
            'Outer wall thickness vector': ['m', 'in'],
            'Gas side effective temperature': ['K', '°C', '°F'],
            'Convective heat flux base': ['W/(m**2)', 'BTU/(h*ft**2)'],
            'Gas side wall temperature': ['K', '°C', '°F'],
            'Gas pressure': ['Pa', 'psi'],
            'Gas pressure threshold for sea level test': ['Pa', 'psi'],
            'Temperature of the wall gas (t_wall_gas) vector': ['K', '°C', '°F'],
            'Dissociated gas temperature': ['K', '°C', '°F'],
            'Dissociated gas viscosity': ['Pa*s', 'cP'],
            'Non-dissociated gas constant': ['J/(kg*K)', 'BTU/(lb*°F)'],
            'Radiative heat flux': ['W/(m**2)', 'BTU/(h*ft**2)'],
            'Radiative nozzle outer wall temperature': ['K', '°C', '°F'],
            'Radiative nozzle wall thickness': ['m', 'in']
        }

        for i, var_name in enumerate(variables):
            label = Label(frame_variables, text=var_name, anchor='w')
            label.grid(row=i+4, column=0, padx=5, pady=2, sticky='w')
            var = StringVar(value=variables_values[var_name])
            entry = Entry(frame_variables, textvariable=var, validate='key', validatecommand=(self.root.register(self.validate_entry), '%P', var_name), justify="right")
            entry.grid(row=i+4, column=1, padx=5, pady=2, sticky='ew')
            self.entries[var_name] = var
            
            if var_name in units and units[var_name]:
                unit_combobox = ttk.Combobox(frame_variables, values=units[var_name], state="readonly", width=10, justify='left')
                unit_combobox.set(units[var_name][0])
                unit_combobox.grid(row=i+4, column=2, padx=5, pady=2, sticky='w')
                self.entries[f"{var_name}_unit"] = unit_combobox

        frame_variables_mesh = Frame(self.page_mesh, borderwidth=2, relief="groove")
        frame_variables_mesh.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        frame_variables_mesh_title = Label(frame_variables_mesh, text="Variables", anchor='w')
        frame_variables_mesh_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="w")

        self.var_mesh_elements_cylindrical_before_flame = self.create_numeric_entry(frame_variables_mesh, "Number of mesh elements in the cylindrical section before the flame front", row=1, default_value="50")
        self.var_mesh_elements_cylindrical_after_flame = self.create_numeric_entry(frame_variables_mesh, "Number of mesh elements in the cylindrical section after the flame front", row=2, default_value="50")
        self.var_mesh_elements_divergent_jacket = self.create_numeric_entry(frame_variables_mesh, "Number of mesh elements in the divergent jacket", row=3, default_value="50")
        self.var_mesh_elements_divergent_no_jacket = self.create_numeric_entry(frame_variables_mesh, "Number of mesh elements in the divergent not covered by the jacket", row=4, default_value="50")

        frame_variables_plot = Frame(self.page_plot, borderwidth=2, relief="groove")
        frame_variables_plot.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        frame_variables_plot_title = Label(frame_variables_plot, text="Variables", anchor='w')
        frame_variables_plot_title.grid(row=0, column=0, columnspan=3, padx=5, pady=(0, 5), sticky="w")

        variables_plot = [
            'Show geometry plot',
            'Show mixture ratio',
            'Show heat flux',
            'Show wall temperature',
            'Show jacket temperature',
            'Show jacket heat transfer coefficient',
            'Show jacket geometry',
            'Show coolant properties',
            'Show copper thermal conductivity',
            'Show jacket pressure',
            'Show jacket flow velocity'
        ]

        variables_plot_values = {var: 'True' for var in variables_plot}

        for i, var_name in enumerate(variables_plot):
            label = Label(frame_variables_plot, text=var_name, anchor='w')
            label.grid(row=i+1, column=0, padx=5, pady=2, sticky='w')
            var = StringVar(value=variables_plot_values[var_name])
            combobox = ttk.Combobox(frame_variables_plot, textvariable=var, values=['True', 'False'], state="readonly", justify='left')
            combobox.grid(row=i+1, column=1, padx=5, pady=2, sticky='ew')
            
            self.adjust_combobox_width(combobox, ['True', 'False'])
            
            self.entries[var_name] = var

        frame_booleans = Frame(self.page_jacket, borderwidth=2, relief="groove")
        frame_booleans.grid(row=4, column=0, pady=10, padx=10, sticky="w")

        frame6_title = Label(frame_booleans, text="Boolean variables", anchor='w')
        frame6_title.grid(row=0, column=0, sticky='w', padx=5, pady=(0, 5))

        frame_variables2 = Frame(frame_booleans)
        frame_variables2.grid(row=1, column=0)

        variables2 = [
            'First iteration convective',
            'Convective heat inner variables'
        ]

        variables2_values = {
            'First iteration convective': 'True',
            'Convective heat inner variables': 'True'
        }

        for i, var_name in enumerate(variables2):
            label = Label(frame_variables2, text=var_name, anchor='w')
            label.grid(row=i, column=0, padx=5, pady=2, sticky='w')
            var = StringVar(value=variables2_values[var_name])
            combobox = ttk.Combobox(frame_variables2, textvariable=var, values=['True', 'False'], state="readonly", justify='left')
            combobox.grid(row=i, column=1, padx=5, pady=2, sticky='ew')
            
            self.adjust_combobox_width(combobox, ['True', 'False'])
            
            self.entries[var_name] = var

        submit_button = Button(self.root, text='Submit', command=self.process_form)
        submit_button.grid(row=1, column=0, pady=10, sticky='e')

    def validate_entry(self, new_value, field):
        if field in self.numeric_fields:
            if new_value == "" or re.match(r'^-?\d*\.?\d*$', new_value):
                return True
            else:
                return False
        return True

    def process_form(self, save_only=False):
        for field, entry in self.entries.items():
            if "_unit" in field:
                continue
            value = entry.get().strip()
            if not value:
                value = "1"  # Preencher campos vazios com valor 1
            if field in self.numeric_fields:
                try:
                    value = re.sub(r'[^\d.-]', '', value)
                    value = float(value)
                except ValueError:
                    messagebox.showerror("Invalid Input", f"Enter a valid number for '{field}'.")
                    return
            unit = self.entries.get(f"{field}_unit")
            if unit:
                value, unit = self.convert_to_si(value, unit.get())
            self.form_data.data[field] = value

        if not save_only:
            messagebox.showinfo("Success", "Data submitted successfully!")
            write_param_file(self.form_data.data, self.testing)  # Chamando a função importada aqui
        print(self.form_data.data)

    def adjust_combobox_width(self, combobox, values, max_width=50):
        font = tkFont.Font(font=combobox['font'])
        max_text_width = max([font.measure(value) for value in values])
        char_width = font.measure('0')
        adjusted_width = min(max_text_width // char_width + 1, max_width)
        combobox.config(width=adjusted_width)

    def convert_to_si(self, value, unit):
        conversions = {
            'lb/(ft**3)': (pound / (foot**3), 'kg/(m**3)'),
            'BTU/(hr*ft*oF)': (1.730735, 'W/(m*K)'),
            'BTU/(lb*oF)': (4184 / (pound * degree_Fahrenheit), 'J/(kg*K)'),
            'oF': (lambda x: convert_temperature(x, 'F', 'K'), 'K'),
            'psi': (psi, 'Pa'),
            '1/oF': (1.8, '1/K')
        }
        if unit in conversions:
            factor, si_unit = conversions[unit]
            if callable(factor):
                return factor(value), si_unit
            else:
                return value * factor, si_unit
        return value, unit

def open_main_gui_tca():
    root = Tk()
    app = MainForm(root)
    root.state('normal')  # Use 'normal' para abrir a janela em estado normal
    root.attributes('-zoomed', True)  # Maximizar a janela (Linux)
    root.mainloop()

if __name__ == "__main__":
    open_main_gui_tca()
