# estilos.py
# Configuración de estilos y layout para la app

PADDING_X = 10
PADDING_Y = 8
FONT_LABEL = ("Arial", 12, "bold") # (fuente, tamaño, negrita)
FONT_LISTBOX = ("Arial", 11) # (fuente, tamaño)
FONT_BOTON = ("Arial", 10) # (fuente, tamaño)
FONT_RELOJ = ("Arial", 24, "bold")

# Paletas de colores para modo claro y oscuro
MODO_CLARO = {
    'bg': '#f4f4f4',
    'fg': '#222',
    'label_bg': '#f4f4f4',
    'label_fg': '#111',
    'listbox_bg': '#fff',
    'listbox_fg': '#222',
    'boton_bg': '#e0e0e0',
    'boton_fg': '#222',
    'pomodoro_bg': '#222244',
    'pomodoro_fg': '#fff',
    'frame_bg': '#f4f4f4',
    'entry_bg': '#fff',
    'entry_fg': '#222',
    'entry_placeholder': '#888',
    'reloj_bg': '#222244',
    'reloj_fg': '#ffffff'
}
MODO_OSCURO = {
    'bg': '#181830',
    'fg': '#eee',
    'label_bg': '#181830',
    'label_fg': '#fff',
    'listbox_bg': '#23233a',
    'listbox_fg': '#fff',
    'boton_bg': '#23233a',
    'boton_fg': '#fff',
    'pomodoro_bg': '#222244',
    'pomodoro_fg': '#fff',
    'frame_bg': '#181830',
    'entry_bg': '#fff',
    'entry_fg': '#222',
    'entry_placeholder': '#888',
    'reloj_bg': '#222244',
    'reloj_fg': '#ffffff'
}

# Función para aplicar estilos a un label
def aplicar_estilo_label(label): # se le aplica los estilos a un label
    label.config(font=FONT_LABEL, pady=2) # (fuente, padding_y)

# Función para aplicar estilos a un listbox
def aplicar_estilo_listbox(listbox): # se le aplica los estilos a un listbox
    listbox.config(font=FONT_LISTBOX, width=25, height=10) # (fuente, ancho, alto)

# Función para aplicar estilos a un botón
def aplicar_estilo_boton(boton): # se le aplica los estilos a un botón
    boton.config(font=FONT_BOTON, padx=8, pady=3) # (fuente, padding_x, padding_y)

def aplicar_estilo_entry(entry, tema, placeholder_text=None): # se le aplica los estilos a un entry
    entry.config(bg=tema['entry_bg'], fg=tema['entry_fg'], insertbackground=tema['entry_fg']) # (background, foreground, insertbackground)
    if placeholder_text is not None: # si el placeholder_text no es None
        entry.delete(0, 'end') # se elimina el texto del entry
        entry.insert(0, placeholder_text) # se inserta el placeholder_text en el entry (para que vuelva a aparecer)
        entry.config(fg=tema['entry_placeholder']) # se cambia el color del texto del entry, según el tema

# Aplica el tema a widgets principales
# widgets: dict con keys: ventana, labels, listboxes, botones, pomodoro_frame, pomodoro_label, frames



# Función para aplicar el tema a los widgets principales
# usamos selectbackground y selectforeground para que el texto y el fondo de los listboxes sean distintos cuando están seleccionados
# usamos activebackground y activeforeground para que el fondo y el texto de los botones sean distintos cuando están activos
def aplicar_tema(widgets, tema):
    # Fondo ventana
    widgets['ventana'].config(bg=tema['bg'])
    # Labels
    for label in widgets['labels']:
        label.config(bg=tema['label_bg'], fg=tema['label_fg'])
    # Listboxes
    for lb in widgets['listboxes']:
        lb.config(bg=tema['listbox_bg'], fg=tema['listbox_fg'], selectbackground='#4a4a7a', selectforeground='#fff')
    # Botones
    for boton in widgets['botones']:
        boton.config(bg=tema['boton_bg'], fg=tema['boton_fg'], activebackground=tema['pomodoro_bg'], activeforeground=tema['pomodoro_fg'])
    # Frames
    for frame in widgets.get('frames', []):
        frame.config(bg=tema['frame_bg'])
    # Pomodoro
    if 'pomodoro_frame' in widgets:
        widgets['pomodoro_frame'].config(bg=tema['pomodoro_bg'])
    if 'pomodoro_label' in widgets:
        widgets['pomodoro_label'].config(bg=tema['pomodoro_bg'], fg=tema['pomodoro_fg'])

# Función para aplicar el tema a los widgets de la columna izquierda
# usamos bg y fg para que el fondo y el texto de los labels sean distintos según el tema
# usamos bg y fg para que el fondo y el texto de los listboxes sean distintos según el tema
# usamos bg y fg para que el fondo y el texto de los botones sean distintos según el tema
# usamos bg y fg para que el fondo y el texto de los frames sean distintos según el tema
# usamos bg y fg para que el fondo y el texto de los pomodoros sean distintos según el tema

def aplicar_tema_columna_izquierda(frame, widgets, tema):
    frame.config(bg=tema['bg'])
    if 'label' in widgets:
        widgets['label'].config(bg=tema['bg'], fg=tema['label_fg'])
    if 'listbox' in widgets:
        widgets['listbox'].config(bg=tema['listbox_bg'], fg=tema['listbox_fg'])
    if 'botones' in widgets:
        for boton in widgets['botones']:
            boton.config(bg=tema['boton_bg'], fg=tema['boton_fg'], activebackground=tema['pomodoro_bg'], activeforeground=tema['pomodoro_fg'])
    if 'logo' in widgets and widgets['logo'] is not None:
        widgets['logo'].config(bg=tema['bg'])