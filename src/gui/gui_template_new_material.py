import os
import re
import tkinter as tk
from tkinter import Tk, Label, Entry, Button, messagebox, ttk, Frame
from datetime import datetime  # Adicionado para obter a data atual
from scipy.constants import pound, foot, psi, degree_Fahrenheit, convert_temperature
from scipy.constants import calorie, kilo  # Usaremos caloria para conversão de BTU

class MaterialForm:
    """
    Classe que cria uma interface gráfica para entrada de dados de propriedades de materiais
    utilizando a biblioteca tkinter.
    """
    def __init__(self, root, testing=False):
        """
        Inicializa a janela do formulário com campos de entrada para propriedades dos materiais.
        """
        self.root = root
        # Flag para controlar a exibição de mensagens de erro durante os testes:
        self.testing = testing
        self.root.title("Propulsion Library proplib - Material Properties Database")

        self.entries = {}
        self.generated_content = []  # Adiciona a variável para armazenar o conteúdo gerado
        fields = [
            'Material name',
            'Density',
            'Thermal conductivity',
            'Specific heat',
            'Melting point',
            'Coefficient of thermal expansion',
            'Ultimate tensile strength',
            'Tensile strength yield',
            'Modulus of elasticity',
            'Shear modulus',
            "Poisson's ratio"
        ]

        self.units = {
            'Density': ['kg/(m**3)', 'lb/(ft**3)'],
            'Thermal conductivity': ['W/(m*K)', 'BTU/(hr*ft*oF)'],
            'Specific heat': ['J/(kg*K)', 'BTU/(lb*oF)'],
            'Melting point': ['K', 'oC', 'oF'],
            'Coefficient of thermal expansion': ['1/K', '1/oC', '1/oF'],
            'Ultimate tensile strength': ['Pa', 'psi'],
            'Tensile strength yield': ['Pa', 'psi'],
            'Modulus of elasticity': ['Pa', 'psi'],
            'Shear modulus': ['Pa', 'psi']
        }

        self.numeric_fields = set(fields) - {'Material name'}

        for i, field in enumerate(fields):
            label = Label(root, text=field, anchor='w', width=30)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = Entry(root, validate='key',
                          validatecommand=(root.register(self.validate_entry), '%P', field))
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry

            if field in self.units:
                unit_combobox = ttk.Combobox(root,
                                             values=self.units[field], state="readonly", width=15)
                unit_combobox.set(self.units[field][0])
                unit_combobox.grid(row=i, column=2, padx=5, pady=5, sticky='w')
                self.entries[f"{field}_unit"] = unit_combobox

        # Criando um frame para o botão Submit e alinhando-o à direita
        button_frame = Frame(root)
        button_frame.grid(row=len(fields), column=0, columnspan=3, pady=10, padx=5, sticky='e')

        self.submit_button = Button(button_frame, text='Submit', command=self.process_form)
        self.submit_button.grid(row=0, column=0, padx=5, pady=10)
        self.submit_button.config(underline=0)  # Sublinha o caractere 'S' (índice 0) do botão

        # Define o atalho Alt+S para o botão Submit
        self.root.bind('<Alt-s>', lambda event: self.process_form())

    def validate_entry(self, value, field):
        """
        Valida a entrada do usuário. Garante que os campos numéricos contenham apenas números.
        """
        if field in self.numeric_fields:
            if value == "" or re.match(r'^-?\d*\.?\d*$', value):
                return True
            else:
                return False
        return True

    def convert_to_si(self, value, unit):
        """
        Converte valores em unidades inglesas para unidades do Sistema Internacional (SI)
        usando `scipy.constants`.
        """
        conversions = {
            'lb/(ft**3)': (pound / (foot**3), 'kg/(m**3)'),
            'BTU/(hr*ft*oF)': (1.730735, 'W/(m*K)'),  # Aproximado
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
        # Retorna o valor inalterado se nenhuma conversão for necessária:
        return value, unit

    def process_form(self):
        """
        Processa os dados inseridos no formulário, validando e criando um arquivo com as
        propriedades.
        """
        data = {}
        self.generated_content = []  # Limpa o conteúdo gerado
        for field, entry in self.entries.items():
            if "_unit" in field:
                continue
            value = entry.get().strip()
            if not value:
                if not self.testing:
                    messagebox.showerror("Missing Input", f"'{field}' cannot be empty.")
                return
            if field in self.numeric_fields:
                try:
                    value = float(value)
                except ValueError:
                    if not self.testing:
                        messagebox.showerror("Invalid Input",
                                             f"Enter a valid number for '{field}'.")
                    return
            unit = self.entries.get(f"{field}_unit")
            if unit:
                value, unit = self.convert_to_si(value, unit.get())
                value = f"{value} {unit}"
            data[field] = value
            self.generated_content.append(value)  # Armazena o valor
            # convertido em generated_content
        self.generate_file(data)

    def generate_file(self, data):
        """
        Gera um arquivo Python com definições de classe e métodos com
        base nas propriedades do material.
        """
        material_name = data.get('Material name', '').strip().replace(' ', '_')
        if not material_name:
            material_name = 'DefaultMaterial'
            file_name = '_default.py'
        else:
            file_name = f'_{material_name.lower()}.py'

        script_dir = os.path.dirname(__file__)  # Diretório do script atual
        file_path = os.path.join(script_dir, file_name)  # Caminho completo do arquivo

        if os.path.exists(file_path) and not self.testing:
            response = messagebox.askyesno("Existing File",
                                           f"The file '{file_name}' already exists. Do you want to replace it?")
            if not response:
                return

        # Adaptação para diferentes sistemas operacionais:
        user_name = os.getenv('USER') or os.getenv('USERNAME') or 'UnknownUser'
        # Obtendo a data atual no formato desejado:
        current_date = datetime.now().strftime('%a %b %d %H:%M:%S %Y')

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            f.write('"""\n')
            f.write(f'Created on {current_date}\n\n')  # Usando a data atual
            f.write(f'Contém base de dados para {material_name} (DEFAULT e variações)\n\n')
            f.write(f'@autor: {user_name}\n')
            f.write('"""\n\n')

            f.write('from proplib.util.properties.material_properties_database.material_base_class import MaterialDatabase\n\n')

            f.write(f'class {material_name}:\n')
            f.write('    def __init__(self):\n')
            f.write('        self._t = 293.15\n')
            f.write('        self._thickness = None\n')
            f.write('        self._k_material = 0\n')
            for field, value in data.items():
                if field != 'Material name':
                    safe_field_name = re.sub(r'[^a-zA-Z0-9_]', '_', field).lower()
                    f.write(f'    def set_{safe_field_name}(self, value):\n')
                    f.write(f'        """\n')
                    f.write(f'        Carrega {field}.\n\n')
                    f.write(f'        :param value: Required. {field} value to set.\n')
                    f.write(f'        """\n')
                    f.write(f'        self.{safe_field_name} = value\n\n')

            # Exemplo de uso no fim do arquivo
            f.write('if __name__ == "__main__":\n')
            f.write(f'    # Example usage:\n')
            f.write(f'    material = {material_name}()\n')
            for field, value in data.items():
                if field != 'Material name':
                    safe_field_name = re.sub(r'[^a-zA-Z0-9_]', '_', field).lower()
                    f.write(f'    material.set_{safe_field_name}({value})\n')
            f.write('    # Continue implementation here\n')

        # Mensagem de sucesso se não estiver em modo de teste
        if not self.testing:
            messagebox.showinfo("Success", "Material created successfully.")

if __name__ == "__main__":
    root = Tk()
    form = MaterialForm(root)
    root.mainloop()
