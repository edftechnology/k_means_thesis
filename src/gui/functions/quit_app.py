# functions/quit_app.py

# -*- coding: utf-8 -*-

from tkinter import messagebox

def quit_app(self):
    """
    Função para perguntar ao usuário se ele deseja sair da aplicação e, em caso afirmativo, fechar a aplicação.

    :param self: Obrigatório. object.
        Instância da classe que está chamando a função. Permite acessar métodos e atributos da classe.
    :return None
    """

    if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
        self.root.quit()
