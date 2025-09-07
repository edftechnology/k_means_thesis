# -*- coding: utf-8 -*-

import os
import sys
from tkinter import Tk, Label, CENTER
from PIL.ImageTk import PhotoImage

# Verifica a variável de ambiente DEBUG_MODE
debug_mode = os.getenv("DEBUG_MODE") == "True"

if debug_mode:
    from gui.main_gui_modules import open_main_gui_modules
else:
    from gui.main_gui_modules import open_main_gui_modules

# Use PIL replacement class
imgdir = 'figures'
imgfile = 'mini_logo_iae.png'

# Does gif, jpg, png, tiff, etc.
if len(sys.argv) > 1:
    imgfile = sys.argv[1]

imgpath = os.path.join(imgdir, imgfile)

win = Tk()

# Set window title
win.title("Propulsion Library prolib")

# Set window background color to white
win.configure(bg='white')

# Create title labels
title_above = Label(win, text="Institute of Aeronautics and Space (IAE)", bg='white', font=("Helvetica", 16))
title_below = Label(win, text="Propulsion Library proplib", bg='white', font=("Helvetica", 16))

# Open image using PIL
imgobj = PhotoImage(file=imgpath)
image_label = Label(win, image=imgobj, bg='white')

# Pack labels and image label
title_above.pack(pady=10)  # Add some padding for spacing
image_label.pack(expand=True, anchor=CENTER)
title_below.pack(pady=10)  # Add some padding for spacing

# Define a size for the window with 16:9 aspect ratio
window_width = 800  # Largura desejada da janela
window_height = int(window_width / 16 * 9)  # Altura calculada para manter a proporção 16:9

# Set window size
win.geometry("{}x{}".format(window_width, window_height))

# Set the window to close after 5 seconds and open the settings window
win.after(5000, lambda: [win.destroy(), open_main_gui_modules()])

win.mainloop()

# print(imgobj.width(), imgobj.height())
# Show size in pixels on exit
