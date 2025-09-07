# functions/create_numeric_entry.py

# -*- coding: utf-8 -*-

from tkinter import ttk

def clear_form(self):
    """
    Limpa todos os campos do formulário, redefinindo os valores de entrada e comboboxes.

    :param self: Obrigatório. object.
        Instância da classe.

    :return None
    """
    
    for entry in self.entries.values():
        if isinstance(entry, StringVar):
            entry.set("")  # Limpa o conteúdo do campo de entrada
        elif isinstance(entry, ttk.Combobox):
            entry.set(entry["values"][0])  # Redefine o combobox para o primeiro valor da lista
