# functions/clear_form.py

# -*- coding: utf-8 -*-

from tkinter import ttk

def clear_form(self):
    """
    Limpa todos os campos do formulário, redefinindo os valores de entrada e comboboxes.

    :param self: Obrigatório. object.
        Instância da classe.
    
    :rertun None
    """
    
    for field, entry in self.entries.items():
        if isinstance(entry, StringVar):
            entry.set("")
        elif isinstance(entry, ttk.Combobox):
            continue  # Skip clearing comboboxes
