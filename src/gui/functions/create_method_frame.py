# -*- coding: utf-8 -*-

from tkinter import Frame, Label, StringVar, ttk

def create_method_frame(self, parent, title, list_values, row, col=0):
    """
    Esta função é bastante específica, mas pode ser reutilizada em outros formulários que necessitem
    de comboboxes.

    :param self: Obrigatório. object.
        Instância da classe.
    :param parent: Obrigatório. Frame.
        O frame pai no qual o novo frame será criado.
    :param title: Obrigatório. str.
        O título do frame que será exibido como um label.
    :param list_values: Obrigatório. list.
        Uma lista de valores que será utilizada para preencher o combobox.
    :param row: Obrigatório. int.
        A linha onde o frame será posicionado no layout de grade do parent.
    :param col: Opcional. int. Default=0.
        A coluna onde o frame será posicionado no layout de grade do parent.
        
    :return: tuple
        Retorna uma tupla contendo a variável StringVar associada ao combobox e o frame criado.
    """

    frame = Frame(parent, borderwidth=0, relief="flat")
    frame.grid(row=row, column=col, pady=2, padx=2, sticky="ew")

    frame_title = Label(frame, text=title, anchor='w')
    frame_title.grid(row=0, column=0, padx=5, pady=(0, 2))

    var = StringVar()
    combobox = ttk.Combobox(frame, textvariable=var, values=list_values, state="readonly", style="TCombobox", justify='left')
    combobox.grid(row=0, column=1, padx=5, pady=(0, 2), sticky="ew")
    
    self.adjust_combobox_width(combobox, list_values)

    self.entries[title] = var
    return var, frame
