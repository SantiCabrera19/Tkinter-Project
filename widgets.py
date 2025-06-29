# widgets.py
# Funciones para crear widgets de la app

import tkinter as tk
from estilos import aplicar_estilo_label, aplicar_estilo_listbox, aplicar_estilo_boton

# Función para crear un botón con estilo predefinido
def crear_boton(ventana, texto, comando):
    # Creamos el botón con el texto y comando especificados
    boton = tk.Button(ventana, text=texto, command=comando)
    # Aplicamos el estilo predefinido al botón
    aplicar_estilo_boton(boton)
    return boton

# Función para crear un Listbox con label opcional y scrollbar opcional
def crear_listbox_con_label(ventana, texto_label=None, use_scroll=False, width=25, height=10):
    label = None
    # Si se especifica un texto para el label, lo creamos
    if texto_label:
        label = tk.Label(ventana, text=texto_label)
        aplicar_estilo_label(label)
    
    # Creamos un frame para contener el listbox y opcionalmente el scrollbar
    frame = tk.Frame(ventana)
    
    # Si se requiere scrollbar
    if use_scroll:
        # Creamos el scrollbar vertical
        scrollbar = tk.Scrollbar(frame, orient='vertical')
        # Creamos el listbox conectado al scrollbar
        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=width, height=height)
        # Configuramos el scrollbar para que controle el listbox
        scrollbar.config(command=listbox.yview)
        # Posicionamos el listbox a la izquierda
        listbox.pack(side=tk.LEFT)
        # Posicionamos el scrollbar a la derecha, ocupando todo el alto
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    else:
        # Si no se requiere scrollbar, creamos solo el listbox
        listbox = tk.Listbox(frame, width=width, height=height)
        aplicar_estilo_listbox(listbox)
        listbox.pack()
    
    # Aplicamos el estilo al listbox
    aplicar_estilo_listbox(listbox)
    return label, frame, listbox

# Función para actualizar el label con el contador de elementos
def actualizar_label_con_contador(label, texto_base, cantidad):
    # Actualizamos el texto del label concatenando el texto base con la cantidad entre paréntesis
    label.config(text=f"{texto_base} ({cantidad})")

# Entry con placeholder y decorado visual a la izquierda
def crear_entry_con_placeholder(frame, placeholder_text, tema, width=40):
    # Creamos un frame interno para contener el decorado y el entry
    entry_frame = tk.Frame(frame, bg=tema['bg'])
    
    # Creamos el decorado visual: un círculo rojo a la izquierda
    decor = tk.Canvas(entry_frame, width=18, height=18, bg=tema['bg'], highlightthickness=0)
    # Dibujamos un círculo rojo (tomate) en el canvas
    decor.create_oval(2, 2, 16, 16, fill='#e74c3c', outline='')
    # Posicionamos el decorado a la izquierda con un pequeño padding
    decor.grid(row=0, column=0, padx=(0, 6))
    
    # Creamos el entry principal con estilo plano y borde resaltado
    entry = tk.Entry(entry_frame, width=width, relief='flat', borderwidth=2, 
                    highlightthickness=1, highlightbackground='#888', highlightcolor='#e74c3c')
    entry.grid(row=0, column=1)
    
    # Función que se ejecuta cuando el entry recibe el foco
    def on_focus_in(event):
        # Si el texto actual es el placeholder, lo limpiamos
        if entry.get() == placeholder_text:
            entry.delete(0, 'end')
            entry.config(fg=tema['entry_fg'])
    
    # Función que se ejecuta cuando el entry pierde el foco
    def on_focus_out(event):
        # Si el entry está vacío, restauramos el placeholder
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg=tema['entry_placeholder'])
    
    # Configuramos el estado inicial del entry
    entry.insert(0, placeholder_text)
    entry.config(fg=tema['entry_placeholder'], bg=tema['entry_bg'])
    
    # Vinculamos los eventos de foco con sus funciones correspondientes
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)
    
    # Devolvemos tanto el frame que contiene todo como el entry en sí
    return entry_frame, entry

# Función para crear un frame simple
def crear_frame(ventana):
    frame = tk.Frame(ventana)
    return frame

# Función para crear un botón específico para el Pomodoro
def crear_boton_pomodoro(parent, texto, comando): # parent es el frame que contiene el botón
    boton = tk.Button(parent, text=texto, command=comando)
    aplicar_estilo_boton(boton)
    return boton

# Función para crear un listbox específico para tareas en proceso
def crear_listbox_en_proceso(ventana, texto_label="En proceso", use_scroll=False, width=30, height=3):
    # Creamos el label con el texto especificado
    label = tk.Label(ventana, text=texto_label)
    aplicar_estilo_label(label)
    
    # Creamos el frame contenedor
    frame = tk.Frame(ventana)
    
    # Si se requiere scrollbar
    if use_scroll:
        # Creamos el scrollbar vertical
        scrollbar = tk.Scrollbar(frame, orient='vertical')
        # Creamos el listbox conectado al scrollbar
        listbox = tk.Listbox(frame, width=width, height=height, yscrollcommand=scrollbar.set)
        # Configuramos el scrollbar para que controle el listbox
        scrollbar.config(command=listbox.yview)
        # Posicionamos el listbox a la izquierda
        listbox.pack(side=tk.LEFT)
        # Posicionamos el scrollbar a la derecha, ocupando todo el alto
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    else:
        # Si no se requiere scrollbar, creamos solo el listbox
        listbox = tk.Listbox(frame, width=width, height=height)
        aplicar_estilo_listbox(listbox)
        listbox.pack()
    
    # Aplicamos el estilo al listbox
    aplicar_estilo_listbox(listbox)
    return label, frame, listbox