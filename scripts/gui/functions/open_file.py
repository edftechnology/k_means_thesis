# functions/open_file.py

# -*- coding: utf-8 -*-

from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import json

def open_file(self):
    """
    Função para abrir um arquivo JSON e carregar os dados no formulário.

    :param self: Obrigatório. object.
        Instância da classe que está chamando a função. Permite acessar métodos e atributos da classe.

    :return None
    """

    file_path = askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.form_data.data = json.load(file)
            self.file_path = file_path
            self.populate_form()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")

