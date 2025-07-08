# functions/save_file.py

# -*- coding: utf-8 -*-

import json
from tkinter import messagebox

def save_file(self):
    """
    Função que salva os dados do formulário em um arquivo JSON.

    :param self: Obrigatório. object.
        Instância da classe que está chamando a função. Permite acessar métodos e atributos da classe.
    
    :return None
    """

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
