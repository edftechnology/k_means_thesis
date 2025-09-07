# functions/save_as_file.py

# -*- coding: utf-8 -*-

from tkinter.filedialog import asksaveasfilename

def save_as_file(self):
    """
    Função para abrir uma caixa de diálogo "Salvar Como" para salvar os dados do formulário em um arquivo JSON.

    :param self: Obrigatório. object.
        Instância da classe que está chamando a função. Permite acessar métodos e atributos da classe.
    
    :return None
    """

    file_path = asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        self.file_path = file_path
        self.save_file()
