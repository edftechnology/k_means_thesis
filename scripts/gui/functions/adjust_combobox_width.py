# functions/new_file.py

# -*- coding: utf-8 -*-

def adjust_combobox_width(self, combobox, values, max_width=50):
    """
    Ajusta a largura de um combobox com base na largura do texto de seus valores.

    :param self: Obrigatório. object.
        Instância da classe. 
    :param combobox: Obrigatório. ttk.Combobox.
        O combobox cujo tamanho será ajustado. 
    :param values: Obrigatório. list.
        Uma lista de valores que serão exibidos no combobox.
    :param max_width: Opcional. int. Default=50.
        A largura máxima permitida para o combobox. O valor padrão é 50 caracteres.
    
    :return None
    """
    
    font = tkFont.Font(font=combobox['font'])
    max_text_width = max([font.measure(value) for value in values])
    char_width = font.measure('0')
    adjusted_width = min(max_text_width // char_width + 1, max_width)
    combobox.config(width=adjusted_width)
