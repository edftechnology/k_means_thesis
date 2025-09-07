# functions/write_param_file.py

# -*- coding: utf-8 -*-
import os
from datetime import datetime
import numpy as np

def write_param_file(self):
    """
    Função para escrever/gerar o arquivo `input.py` para execução.

    :param self: Opcional. Object.
        Instância da classe.

    :return
        Gera o arquivo de input `.py`. 
    """

    # Especifica o diretório alvo
    target_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'inputs')
    # Cria o diretório se ele não existir
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Obtém o nome do arquivo do motor
    engine_file_name = self.form_data.data.get('Engine/File name', '').strip().replace(' ', '_')
    if not engine_file_name:
        engine_file_name = 'DefaultEngineFileName'
    # Remove o prefixo de sublinhado
    file_name = f'{engine_file_name.lower()}.py'

    # Constrói o caminho do arquivo
    file_path = os.path.join(target_dir, file_name)

    if os.path.exists(file_path) and not self.testing:
        response = messagebox.askyesno("Existing File", f"The file '{file_name}' already exists. Do you want to replace it?")
        if not response:
            return

    user_name = os.getenv('USER') or os.getenv('USERNAME') or 'UnknownUser'  # Adaptação para diferentes sistemas operacionais
    current_date = datetime.now().strftime('%a %b %d %H:%M:%S %Y')  # Obtendo a data atual no formato desejado

    description = self.form_data.data.get('Description', 'Arquivo de `input` (entrada) para o comando `TCA_main` com escolha de parâmetros do Conjunto da Câmara de Empuxo (Thrust Chamber Assembly, TCA) Motor Foguete a Propelente Líquido (MFPL).')

    param_file_content = f"""# -*- coding: utf-8 -*-

\"\"\"
Created on {current_date}

Descrição: {description}

@autor: {user_name}

alterado por último: {current_date}
\"\"\"

import numpy as np

class ParaFile:
\"\"\"
Classe para manipulação de arquivos de parâmetros,
ou seja, Parameters File (ParaFile).
\"\"\"

def __init__(self):
    \"\"\"
    Classe para manipulação de arquivos de parâmetros,
    ou seja, Parameters File (ParaFile)..

    :param self: object.
        Instância da classe.
    \"\"\"

    self.procedure = 'TCA_analysis'

    # ---
    # DADO(S)/PARÂMETRO(S) GERAL(IS) DO CONJUNTO DA CÂMARA DE EMPUXO
    # (THRUST CHAMBER ASSEMBLY, TCA):
    
    # oxidizer: Oxidante
    self.oxidizer = '{self.form_data.data.get('Oxidizer', 'oxygen')}'
    # fuel: Combustível
    self.fuel = '{self.form_data.data.get('Fuel', 'ethanol')}'
    # oxid_temp: Temperatura de entrada do oxidante na câmara de empuxo [K]
    self.oxid_temp = {self.form_data.data.get('Oxidizer inlet temperature in the thrust chamber', 4.0)}  # [K]
    # fuel_inj_temp: Palpite inicial da temperatura de entrada nos injetores [K]
    self.fuel_inj_temp = {self.form_data.data.get('Initial guess for ethanol inlet temperature in injectors', 90.0)}  # [K]
    # thrust: Empuxo de projeto no vácuo [N]
    self.thrust = {self.form_data.data.get('Design vacuum thrust', 25e3)}  # [N]
    # chamber_pres: Pressão de câmara de projeto [Pa]
    self.chamber_pres = {self.form_data.data.get('Design chamber pressure', 60e6)}  # [Pa]
    # pres_expansion_rt: Razão entre as pressões na saída do divergente e
    # da câmara de empuxo
    self.pres_expansion_rt = {self.form_data.data.get('Pressure ratio at the nozzle exit to chamber', 20.0)}
    # mix_rt_global: km global (O/F) [-]
    self.mix_rt_global = {self.form_data.data.get('Global mixture ratio (O/F)', 1.48)}
    # mix_rt_wall: km do "wall layer" (O/F na camada externa de injetores)
    self.mix_rt_wall = {self.form_data.data.get('Wall layer mixture ratio (O/F in outer layer injectors)', 3.2)}
    # wall_frac: Fração da vazão total que será injetada na "wall layer"
    # (valor 'dummy' até o momento, ainda não utilizado no cálculo)
    self.wall_frac = {self.form_data.data.get('Fraction of total flow injected in the wall layer', 48/122)}
    # film_frac: Fração da vazão total que será direcionada para o filme de
    # combustível
    self.film_frac = {self.form_data.data.get('Fraction of total flow directed to fuel film', 0.0)}

    # AVISO: o código calculará o `km` do core em função dos 4 valores acima.

    # isp_min: Impulso específico no vácuo mínimo [s]
    self.isp_min = {self.form_data.data.get('Minimum specific impulse at sea level', 321.8)}  # [s]
    # exp_eff: eficiência de expansão estimada
    self.exp_eff = {self.form_data.data.get('Estimated expansion efficiency', 0.97)}
    # comb_eff: eficiência de combustão (c*) estimada
    self.comb_eff = {self.form_data.data.get('Estimated combustion efficiency (c*)', 0.98)}

    # ---
    # DADO(S)/PARÂMETRO(S) GEOMÉTRICO(S):

    # exhaust_diam_max: Diâmetro de saída máximo [m]
    self.exhaust_diam_max = {self.form_data.data.get('Maximum exit diameter', 1.4*0.2)}  # [m]
    # chb_diameter: Diâmetro da seção cilíndrica da câmara de combustão [m]
    self.chb_diameter = {self.form_data.data.get('Diameter of the cylindrical section of the combustion chamber', 0.1)}  # [m]
    # res_time: Tempo de residência dos gases na câmara de combustão [s]
    self.res_time = {self.form_data.data.get('Gas residence time in the combustion chamber', 2.9e-3)}  # [s]
    # charac_length: Comprimento característico [m]. Se o tempo de residência for
    # fornecido, este valor será ignorado.
    self.charac_length = {self.form_data.data.get('Characteristic length', None)}
    # charac_length_upper_bound: Máximo comprimento característico - Dobrovolskiy [m]
    self.charac_length_upper_bound = {self.form_data.data.get('Maximum characteristic length - Dobrovolskiy', 0.5)}  # [m]
    # charac_length_lower_bound: Mínimo comprimento característico - Dobrovolskiy[m]
    self.charac_length_lower_bound = {self.form_data.data.get('Minimum characteristic length - Dobrovolskiy', 1.3)}  # [m]
    # chamber_area_rt: Razão de compressão (cilíndrico/garganta) - Gurtovoi recomenda entre
    # 2 e 6.
    self.chamber_area_rt = {self.form_data.data.get('Compression ratio (cylindrical/throat)', None)}
    # conic: 'True' se existe perfil cônico no convergente
    self.conic = {self.form_data.data.get('Inclination angle of the conical profile, if any', False)}
    # conic_angle: Ângulo de inclinação do perfil cônico, se houver (rad)
    self.conic_angle = {self.form_data.data.get('Inclination angle of the conical profile, if any', None)}
    # smooth_rad_rt: Razão entre raio de suavização do divergente e raio da parte
    # cilíndrica. Kessaev: 0.10...0.20, L5: 0.191
    self.smooth_rad_rt = {self.form_data.data.get('Ratio between the radius of smoothing of the divergent and the radius of the cylindrical part', 0.191)}
    # max_length: Comprimento máximo da câmara de empuxo
    self.max_length = {self.form_data.data.get('Maximum thrust chamber length', None)}
    # chb_num_of_elem: Número de coordenadas (x, r) do contorno
    self.chb_num_of_elem = {self.form_data.data.get('Number of coordinates (x, r) of the contour', 10)}
    # low_pres_conv_rad_rt: Razão entre raio do convergente de baixa pressão e diâmetro da
    # garganta. Kessaev recomenda 1.
    self.low_pres_conv_rad_rt = {self.form_data.data.get('Ratio between the radius of the low pressure convergent and the throat diameter', 1.0)}
    # high_pres_conv_rad_rt: Razão entre raio do convergente de alta pressão e diâmetro da
    # parte cilíndrica
    self.high_pres_conv_rad_rt = {self.form_data.data.get('Ratio between the radius of the high pressure convergent and the diameter of the cylindrical part', None)}
    # beta_m_tol: Tolerância para convergência da inclinação inicial da tubeira
    # (beta_m) usando fmin (referente ao diâmetro relativo adimensional)
    self.beta_m_tol = {self.form_data.data.get('Tolerance for convergence of the initial slope of the nozzle (beta_m)', 1e-4)}
    # contour_tol: Tolerância para convergência da inclinação da tubeira (beta)
    # usando fmin (referente à coordenada axial x) [m]
    self.contour_tol = {self.form_data.data.get('Tolerance for convergence of the slope of the nozzle (beta)', 1e-4)}

    # ---
    # DADO(S)/PARÂMETRO(S) DOS INJETORES:

    # fuel_inj_number: Número de injetores de combustível
    self.fuel_inj_number = {self.form_data.data.get('Number of fuel injectors', 24)}
    # oxid_inj_number: Número de injetores de oxidante
    self.oxid_inj_number = {self.form_data.data.get('Number of oxidizer injectors', 24)}

    # ---
    # DADOS/PARÂMETRO(S) DA JAQUETA DE REFRIGERAÇÃO:

    # is_jacket_inlet_at_nozzle_exit: Binário para informar se o ponto do divergente onde se inicia a
    # jaqueta de refrigeração é ponto de saída do divergente
    # (se verdadeiro, ignora a variável a seguir)
    self.is_jacket_inlet_at_nozzle_exit = {self.form_data.data.get('Is jacket inlet at nozzle exit', True)}
    # jacket_inlet_area_rt: Razão de área do ponto do divergente onde se inicia a refrigeração
    # (se a variável anterior for 'True', esse valor é ignorado)
    self.jacket_inlet_area_rt = {self.form_data.data.get('Jacket inlet area ratio', 1.0)}
    # wall_thickness: Espessura de parede [m]
    self.wall_thickness = {self.form_data.data.get('Wall thickness vector', 1e-3)}  # [m]
    # rib_thickness: Espessura do rib [m]
    self.rib_thickness = {self.form_data.data.get('Rib thickness', 1e-3)}  # [m]
    # rib_height: Altura do rib [m]
    self.rib_height = {self.form_data.data.get('Rib height', 2e-3)}  # [m]
    # is_rib_qty_constant: Binário que mostra se a quantidade de ribs é constante
    self.is_rib_qty_constant = {self.form_data.data.get('Is rib quantity constant', True)}
    # min_channel_width_throat: Menor largura do canal na seção crítica [m]
    self.min_channel_width_throat = {self.form_data.data.get('Minimum channel width at throat', 1e-3)}  # [m]
    # inner_wall_material: Material da parede interna
    self.inner_wall_material = '{self.form_data.data.get('Inner wall material', 'AISI304')}'
    # wall_max_service_temperature: Temperatura máxima de trabalho para a parede [K]
    self.wall_max_service_temperature = {self.form_data.data.get('Maximum wall service temperature', 723.0)}  # [K]
    # liq_side_wall_max_temperature: Temperatura máxima de trabalho para a parede interna [K]
    self.liq_side_wall_max_temperature = {self.form_data.data.get('Maximum liquid side wall temperature', 723.0)}  # [K]
    # outer_wall_material: Material da parede externa
    self.outer_wall_material = '{self.form_data.data.get('Outer wall material', 'AISI304')}'
    # jacket_coolant: Substância para resfriamento
    self.jacket_coolant = '{self.form_data.data.get('Coolant', 'ethanol')}'
    # manifold_fuel_inlet_pres_loss: Perda de pressão no manifold de entrada de combustível [Pa]
    self.manifold_fuel_inlet_pres_loss = {self.form_data.data.get('Fuel manifold inlet pressure loss', 1e3)}  # [Pa]
    # jacket_outlet_inj_pres_loss: Perda de pressão entre a saída da jaqueta e a entrada do injetor [Pa]
    self.jacket_outlet_inj_pres_loss = {self.form_data.data.get('Jacket outlet injector pressure loss', 1e3)}  # [Pa]
    # fuel_inj_pres_loss: Perda de pressão no injetor de combustível [Pa]
    self.fuel_inj_pres_loss = {self.form_data.data.get('Fuel injector pressure loss', 6e3)}  # [Pa]
    # oxid_inlet_pres_loss: Perda de pressão na entrada de oxidante [Pa]
    self.oxid_inlet_pres_loss = {self.form_data.data.get('Oxidizer inlet pressure loss', 1e3)}  # [Pa]
    # oxid_inj_pres_loss: Perda de pressão no injetor de combustível [Pa]
    self.oxid_inj_pres_loss = {self.form_data.data.get('Oxidizer injector pressure loss', 2e3)}  # [Pa]
    # jacket_fuel_inlet_temp: Temperatura da entrada do etanol na jaqueta [K]
    self.jacket_fuel_inlet_temp = {self.form_data.data.get('Fuel inlet temperature in jacket', 32.0)}  # [K]

    # ---
    # DADO(S)/PARÂMETRO(S) DE REFINAMENTO DA MALHA - PARA UTILIZAÇÃO EM `np.linspace()`

    # n_elem_cyl_before_flame: Número de elementos da malha antes na seção cilíndrica, antes da
    # frente de chama
    self.n_elem_cyl_before_flame = {self.form_data.data.get('Number of mesh elements in the cylindrical section before the flame front', 10)}
    # n_elem_cyl_after_flame: Número de elementos da malha antes na seção cilíndrica, antes da
    # frente de chama
    self.n_elem_cyl_after_flame = {self.form_data.data.get('Number of mesh elements in the cylindrical section after the flame front', 10)}
    # n_elem_conv: Número de elementos da malha antes na seção cilíndrica, antes da
    # frente de chama
    self.n_elem_conv = {self.form_data.data.get('Number of mesh elements in the cylindrical section before the flame front', 10)}
    # n_elem_throat: Número de elementos da malha antes na seção cilíndrica, antes da
    # frente de chama
    self.n_elem_throat = {self.form_data.data.get('Number of mesh elements in the divergent jacket', 10)}
    # n_elem_pre_div: Número de elementos da malha antes na seção cilíndrica, antes da
    # frente de chama
    self.n_elem_pre_div = {self.form_data.data.get('Number of mesh elements in the divergent not covered by the jacket', 10)}
    # n_div_jacket: Número de elementos da malha do divergente da jaqueta
    self.n_div_jacket = {self.form_data.data.get('Number of mesh elements in the divergent not covered by the jacket', 10)}
    # n_div_rad: Número de elementos da malha do divergente não coberto pela jaqueta
    self.n_div_rad = {self.form_data.data.get('Number of mesh elements in the divergent not covered by the jacket', 10)}

    # ---
    # DADO(S)/PARÂMETRO(S) PARA O CÁLCULO DO CALOR RADIATIVO:

    # max_radiative_heat_start_position: Distância a contar do cabeçote de injeção partir da qual o calor
    # radiativo pode ser considerado máximo. "Frente de chama". Tanto
    # Dorbrovolskiy 1968, p.159, quanto Vassiliev 1993, p.51, recomendam
    # um valor entre 50-100 mm, porém não dão nome para esse variável.
    # Valor menor é mais conservador, resulta em fluxo de calor maior na
    # região inicial. Valor em (m)
    self.max_radiative_heat_start_position = {self.form_data.data.get('Max radiative heat start position', 0.01)}

    # ---
    # DADO(S)/PARÂMETRO(S) PARA O CÁLCULO DO CALOR CONVECTIVO:

    # flame_front_start_position: Posição do início da frente de chama em relação ao início do
    # cilíndrico (m)
    self.flame_front_start_position = {self.form_data.data.get('Flame front start position', 0.01)}

    # ---
    # CONFIGURAÇÃO(ÕES) PARA PLOTAGEM:

    # Indicação se o gráfico do contorno deve ser mostrado
    self.show_geo_plot = {self.form_data.data.get('Show geometry plot', 'True')}
    self.show_mixture_ratio = {self.form_data.data.get('Show mixture ratio', 'False')}
    self.show_heat_flux = {self.form_data.data.get('Show heat flux', 'True')}
    self.show_wall_temperature = {self.form_data.data.get('Show wall temperature', 'True')}
    self.show_jacket_temperature = {self.form_data.data.get('Show jacket temperature', 'False')}
    self.show_jacket_heat_transfer_coefficient = {self.form_data.data.get('Show jacket heat transfer coefficient', 'True')}
    self.show_jacket_geometry = {self.form_data.data.get('Show jacket geometry', 'True')}
    self.show_coolant_properties = {self.form_data.data.get('Show coolant properties', 'True')}
    self.show_copper_thermal_conductivity = {self.form_data.data.get('Show copper thermal conductivity', 'False')}
    self.show_jacket_pressure = {self.form_data.data.get('Show jacket pressure', 'True')}
    self.show_jacket_flow_velocity = {self.form_data.data.get('Show jacket flow velocity', 'True')}
"""

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(param_file_content)

    if not self.testing:
        messagebox.showinfo("Success", "Parameter file created successfully.")
