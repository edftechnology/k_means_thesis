# functions/create_numeric_entry.py

# functions/create_numeric_entry.py

# -*- coding: utf-8 -*-

from tkinter import ttk, StringVar

def create_numeric_entry(parent, title, row, default_value="", units=None, entries=None):
    """
    Cria uma entrada numérica com um rótulo e uma unidade opcional.

    :param parent: Obrigatório. object.
        Frame pai onde a entrada será adicionada.
    :param title: Obrigatório. str.
        O título da entrada.
    :param row: Obrigatório. int.
        A linha onde a entrada será posicionada no frame.
    :param default_value: Opcional. str.
        O valor padrão da entrada.
    :param units: Opcional. list.
        Lista de unidades para a combobox de unidades.
    :param entries: Opcional. dict.
        Dicionário onde a variável StringVar será armazenada.
    :return: StringVar.
        A variável associada à entrada.
    """
    
    label = ttk.Label(parent, text=title, anchor='w')
    label.grid(row=row, column=0, padx=5, pady=2, sticky='w')
    
    var = StringVar(value=default_value)
    entry = ttk.Entry(parent, textvariable=var, justify="right")
    entry.grid(row=row, column=1, padx=5, pady=2, sticky='ew')
    
    if entries is not None:
        entries[title] = var
    
    if units:
        unit_combobox = ttk.Combobox(parent, values=units, state="readonly", width=10, justify='left')
        unit_combobox.set(units[0])
        unit_combobox.grid(row=row, column=2, padx=5, pady=2, sticky='ew')
        if entries is not None:
            entries[f"{title}_unit"] = unit_combobox
    
    return var
