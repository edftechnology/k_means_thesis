# functions/notdone.py

# -*- coding: utf-8 -*-

from tkinter.messagebox import showerror

def notdone(self):
    """
    Função que exibe uma mensagem de erro indicando que a funcionalidade ainda não foi implementada.

    :param self: Obrigatório. object.
        Instância da classe que está chamando a função. Permite acessar métodos e atributos da classe.
    
    :return None
    """
    
    showerror('Not implemented', 'Not yet available')
