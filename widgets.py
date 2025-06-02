# widgets.py
# Funciones para crear widgets de la app

import tkinter as tk
from estilos import aplicar_estilo_label, aplicar_estilo_listbox, aplicar_estilo_boton


# Función para crear un botón
def crear_boton(ventana, texto, comando):
    boton = tk.Button(ventana, text=texto, command=comando)
    aplicar_estilo_boton(boton)
    return boton

# Función para crear un Listbox con label opcional
def crear_listbox_con_label(ventana, texto_label=None):
    label = None
    if texto_label:
        label = tk.Label(ventana, text=texto_label)
        aplicar_estilo_label(label)
    listbox = tk.Listbox(ventana)
    aplicar_estilo_listbox(listbox)
    return label, listbox

# Función para actualizar el label con el contador
def actualizar_label_con_contador(label, texto_base, cantidad):
    label.config(text=f"{texto_base} ({cantidad})") # Actualiza el label con el texto base y la cantidad

# Entry con placeholder y decorado visual a la izquierda
def crear_entry_con_placeholder(frame, placeholder_text, tema, width=40):
    # Frame interno para el decorado y el entry
    entry_frame = tk.Frame(frame, bg=tema['bg'])
    # Decorado visual: círculo a la izquierda del entry
    decor = tk.Canvas(entry_frame, width=18, height=18, bg=tema['bg'], highlightthickness=0)
    decor.create_oval(2, 2, 16, 16, fill='#e74c3c', outline='') # Tomate/rojo
    decor.grid(row=0, column=0, padx=(0, 6))
    # Entry principal
    entry = tk.Entry(entry_frame, width=width, relief='flat', borderwidth=2, highlightthickness=1, highlightbackground='#888', highlightcolor='#e74c3c')
    entry.grid(row=0, column=1)
    # Lógica de placeholder
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, 'end')
            entry.config(fg=tema['entry_fg'])
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg=tema['entry_placeholder'])
    entry.insert(0, placeholder_text)
    entry.config(fg=tema['entry_placeholder'], bg=tema['entry_bg'])
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)
    # Devuelvo el frame que contiene decorado+entry y el entry en sí
    return entry_frame, entry

def crear_frame(ventana):
    frame = tk.Frame(ventana)
    return frame

def crear_boton_pomodoro(parent, texto, comando):
    boton = tk.Button(parent, text=texto, command=comando)
    aplicar_estilo_boton(boton)
    return boton

def crear_listbox_en_proceso(ventana, texto_label="En proceso"):
    label = tk.Label(ventana, text=texto_label)
    aplicar_estilo_label(label)
    listbox = tk.Listbox(ventana, height=3, width=30)
    aplicar_estilo_listbox(listbox)
    return label, listbox