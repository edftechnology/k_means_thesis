# -*- coding: utf-8 -*-

from tkinter import Menu

def make_menu(main_form_instance, root):
    """
    Cria a barra de menu para a aplicação tkinter, adicionando opções de arquivo como Novo, Abrir, Salvar, 
    Salvar Como e Sair.

    :param main_form_instance: Obrigatório. object.
        Instância da classe MainForm.
    :param root: Obrigatório. tkinter.Tk.
        A janela principal da aplicação tkinter.
    :return: Menu.
        A barra de menu criada.
    """
    
    menubar = Menu(root)
    root.config(menu=menubar)

    filemenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New...", command=main_form_instance.new_file)
    filemenu.add_command(label="Open...", command=main_form_instance.open_file)
    filemenu.add_command(label="Save", command=main_form_instance.save_file)
    filemenu.add_command(label="Save As...", command=main_form_instance.save_as_file)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=main_form_instance.quit_app)

    return menubar
