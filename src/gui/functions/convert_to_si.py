# functions/convert_to_si.py

# -*- coding: utf-8 -*-

def convert_to_si(self, value, unit):
    """
    Esta função é útil para conversões de unidade e pode ser usada em diversos contextos.

    :param self: Opcional. object.
        Instância da classe.
    :param value: Obrigatório. float.
        Valor.
    :param unit: Obrigatório. str.
        Unidade.
    """
    
    conversions = {
        'lb/(ft**3)': (pound / (foot**3), 'kg/(m**3)'),
        'BTU/(hr*ft*oF)': (1.730735, 'W/(m*K)'),
        'BTU/(lb*oF)': (4184 / (pound * degree_Fahrenheit), 'J/(kg*K)'),
        'oF': (lambda x: convert_temperature(x, 'F', 'K'), 'K'),
        'psi': (psi, 'Pa'),
        '1/oF': (1.8, '1/K')
    }
    if unit in conversions:
        factor, si_unit = conversions[unit]
        if callable(factor):
            return factor(value), si_unit
        else:
            return value * factor, si_unit
    return value, unit
