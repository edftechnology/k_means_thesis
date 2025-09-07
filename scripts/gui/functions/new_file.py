# functions/new_file.py

# -*- coding: utf-8 -*-

from tkinter import messagebox

def new_file(self):
    """
    Função que lida com a criação de um novo arquivo, perguntando ao usuário se deseja limpar todos os campos
    do formulário atual. Se o usuário confirmar, todos os campos do formulário são limpos. Caso contrário,
    uma mensagem informando que os dados não foram alterados é exibida.

    :param self: Obrigatório. object.
        Instância da classe que contém os métodos e atributos necessários, como `form_data` e `clear_form`.
    """
    if messagebox.askyesno("Clear Form", "Do you want to clear all fields?"):
        self.form_data.data = {}
        self.clear_form()
    else:
        messagebox.showinfo("Info", "Data not changed.")
