# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox

import os

# Verifica a variável de ambiente DEBUG_MODE
debug_mode = os.getenv("DEBUG_MODE") == "True"

if debug_mode:
    from main_gui_tca import open_main_gui_tca
else:
    from gui.main_gui_tca import open_main_gui_tca

class OrgChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Propulsion Library proplib")
        self.canvas = tk.Canvas(self.root, width=800, height=1000)
        self.canvas.pack(expand=True, fill='both')
        self.create_org_chart()

    def create_org_chart(self):
        self.buttons = []
        self.lines = []

        # Calculando as coordenadas centrais da janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        central_line_x = width // 2

        # Desenhando caixas principais do organograma como botões
        main_button = self.create_button(self.canvas, "Propulsion Library proplib",
                                         central_line_x - 150, 50,
                                         self.create_open_function("proplib"), "lightgrey")
        self.root.update_idletasks()  # Atualiza o layout
        button_height = main_button.winfo_height()  # Armazena a altura do botão em uma variável
        top_y = 50 + button_height

        # Desenhando caixas subordinadas do organograma como botões
        offset_ = 50
        lpre_button = self.create_button(self.canvas, "Liquid Propellant Rocket Engine (LPRE)",
                                         central_line_x - 350, 50 + 1 * offset_,
                                         self.create_open_function("Liquid Propellant " +
                                                                   "Rocket Engine (LPRE)"),
                                         "lightgrey")
        srm_button = self.create_button(self.canvas, "Solid Rocket Motor (SRM)",
                                        central_line_x + 50, 50 + 1 * offset_,
                                        self.create_open_function("Solid Rocket Motor (SRM)"),
                                        "lightgrey")

        # Adiciona linhas horizontais e verticais para LPRE e SRM
        # linha vertical do topo até o ponto entre LPRE e SRM:
        self.lines.append(self.canvas.create_line(central_line_x, top_y, central_line_x,
                                                  75 + 1 * offset_))
        # linha horizontal até o LPRE:
        self.lines.append(self.canvas.create_line(central_line_x, 75 + 1 * offset_,
                                                  central_line_x - offset_, 75 + 1 * offset_))
        # linha horizontal até o SRM:
        self.lines.append(self.canvas.create_line(central_line_x, 75 + 1 * offset_,
                                                  central_line_x + offset_, 75 + 1 * offset_))

        # Desenhando caixas subordinadas do LPRE como botões
        y_of_subordinate_boxes = 150
        boxes_lpre = [
            ("Engine Support Structure (ESS)", y_of_subordinate_boxes + 0 * offset_, "lightgrey"),
            ("Propellant Feed System (PFS)", y_of_subordinate_boxes + 1 * offset_, "lightgrey"),
            ("Pump (PUMP)", y_of_subordinate_boxes + 2 * offset_, "lightgrey"),
            ("Thrust Chamber Assembly (TCA)", y_of_subordinate_boxes + 3 * offset_, "lightgrey"),
            ("Thrust Vector Control (TVC)", y_of_subordinate_boxes + 4 * offset_, "lightgrey"),
            ("Turbine Assembly (TA)", y_of_subordinate_boxes + 5 * offset_, "lightgrey"),
            ("Valves and Pipe Lines (VPL)", y_of_subordinate_boxes + 6 * offset_, "lightgrey")
        ]

        x_initial_coord = central_line_x - 3 * offset_
        for i, (text, y, color) in enumerate(boxes_lpre, start=1):
            if text.lower() == "Thrust Chamber Assembly (TCA)".lower():
                button = self.create_button(self.canvas, text, x_initial_coord, y,
                                            self.create_open_function(text, close_current=True), color)
            else:
                button = self.create_button(self.canvas, text, x_initial_coord, y,
                                            self.create_open_function(text), color)
            # Adiciona linhas horizontais e verticais
            x_coord = central_line_x - 200
            self.lines.append(self.canvas.create_line(x_coord, 75 + 1 * offset_,
                                                      x_coord, y + 25))  # linha vertical do topo até o box atual
            self.lines.append(self.canvas.create_line(x_coord, y + 25, x_initial_coord,
                                                      y + 25))  # linha horizontal até o texto da caixa

    def create_button(self, canvas, text, x, y, command, color):
        button = tk.Button(canvas, text=text, bg=color, command=command, width=40,
                           height=1)  # altura ajustada
        canvas.create_window(x + 150, y + 20, window=button)
        self.buttons.append(button)
        return button

    def create_open_function(self, title, close_current=False):
        return lambda: self.open_new_window(title, close_current)

    def open_new_window(self, title, close_current):
        if title.lower() == "Thrust Chamber Assembly (TCA)".lower():
            self.root.destroy()
            open_main_gui_tca()
        else:
            new_window = tk.Toplevel(self.root)
            new_window.title(title)
            label = tk.Label(new_window, text="In development")  #, font=("Arial", 12))
            label.pack(pady=20)
            button = tk.Button(new_window, text="Close", command=new_window.destroy)
            button.pack(pady=10)

    def centralize_org_chart(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        org_chart_height = self.canvas.winfo_height()
        org_chart_width = self.canvas.winfo_width()
        x_offset = (width - org_chart_width) // 2
        y_offset = (height - org_chart_height) // 2

        for button in self.buttons:
            x, y = button.winfo_x(), button.winfo_y()
            self.canvas.coords(button, x + x_offset, y + y_offset)

        for line in self.lines:
            coords = self.canvas.coords(line)
            new_coords = [coord + (x_offset if i % 2 == 0 else y_offset) for i, coord in enumerate(coords)]
            self.canvas.coords(line, *new_coords)

def open_main_gui_modules():
    root = tk.Tk()
    app = OrgChartApp(root)
    root.state('normal')  # Use 'normal' to open the window in normal state
    root.attributes('-zoomed', True)  # Maximize the window (Linux)

    def on_resize(event):
        app.centralize_org_chart()

    root.bind('<Configure>', on_resize)
    root.mainloop()

if __name__ == "__main__":
    open_main_gui_modules()
