# functions/validate_entry.py

# -*- coding: utf-8 -*-

def validate_entry(self, new_value, field):
    """
    Esta função pode ser útil para qualquer formulário que precise validar entradas numéricas.

    :param self: Opcional. object.
        Instância da classe.
    
    :return bool.
        Valor booleano.
    """
    
    if field in self.numeric_fields:
        if new_value == "" or re.match(r'^-?\d*\.?\d*$', new_value):
            return True
        else:
            return False
    return True
