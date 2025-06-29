# estilos.py
# Configuración de estilos y layout para la app

# Constantes de padding para widgets
PADDING_X = 10  # Padding horizontal
PADDING_Y = 8   # Padding vertical

# Configuración de fuentes para diferentes elementos
FONT_LABEL = ("Arial", 12, "bold")    # Fuente para labels
FONT_LISTBOX = ("Arial", 11)          # Fuente para listboxes
FONT_BOTON = ("Arial", 10)            # Fuente para botones
FONT_RELOJ = ("Arial", 24, "bold")    # Fuente para el reloj Pomodoro

# Paleta de colores para el modo claro
MODO_CLARO = {
    'bg': '#f4f4f4',              # Color de fondo principal
    'fg': '#222',                 # Color de texto principal
    'label_bg': '#f4f4f4',        # Color de fondo de labels
    'label_fg': '#111',           # Color de texto de labels
    'listbox_bg': '#fff',         # Color de fondo de listboxes
    'listbox_fg': '#222',         # Color de texto de listboxes
    'boton_bg': '#e0e0e0',        # Color de fondo de botones
    'boton_fg': '#222',           # Color de texto de botones
    'pomodoro_bg': '#222244',     # Color de fondo del Pomodoro
    'pomodoro_fg': '#fff',        # Color de texto del Pomodoro
    'frame_bg': '#f4f4f4',        # Color de fondo de frames
    'entry_bg': '#fff',           # Color de fondo de entries
    'entry_fg': '#222',           # Color de texto de entries
    'entry_placeholder': '#888',  # Color de texto placeholder
    'reloj_bg': '#222244',        # Color de fondo del reloj
    'reloj_fg': '#ffffff'         # Color de texto del reloj
}

# Paleta de colores para el modo oscuro
MODO_OSCURO = {
    'bg': '#181830',             # Color de fondo principal
    'fg': '#eee',                # Color de texto principal
    'label_bg': '#181830',       # Color de fondo de labels
    'label_fg': '#fff',          # Color de texto de labels
    'listbox_bg': '#23233a',     # Color de fondo de listboxes
    'listbox_fg': '#fff',        # Color de texto de listboxes
    'boton_bg': '#23233a',       # Color de fondo de botones
    'boton_fg': '#fff',          # Color de texto de botones
    'pomodoro_bg': '#222244',    # Color de fondo del Pomodoro
    'pomodoro_fg': '#fff',       # Color de texto del Pomodoro
    'frame_bg': '#181830',       # Color de fondo de frames
    'entry_bg': '#fff',          # Color de fondo de entries
    'entry_fg': '#222',          # Color de texto de entries
    'entry_placeholder': '#888', # Color de texto placeholder
    'reloj_bg': '#222244',       # Color de fondo del reloj
    'reloj_fg': '#ffffff'        # Color de texto del reloj
}

def aplicar_estilo_label(label):
    """
    Aplica el estilo predefinido a un label.
    
    Args:
        label: El widget Label a estilizar
    """
    label.config(font=FONT_LABEL, pady=2)

def aplicar_estilo_listbox(listbox):
    """
    Aplica el estilo predefinido a un listbox.
    
    Args:
        listbox: El widget Listbox a estilizar
    """
    listbox.config(font=FONT_LISTBOX, width=25, height=10)

def aplicar_estilo_boton(boton):
    """
    Aplica el estilo predefinido a un botón.
    
    Args:
        boton: El widget Button a estilizar
    """
    boton.config(font=FONT_BOTON, padx=8, pady=3)

def aplicar_estilo_entry(entry, tema, placeholder_text=None):
    """
    Aplica el estilo predefinido a un entry.
    
    Args:
        entry: El widget Entry a estilizar
        tema: Diccionario con los colores del tema actual
        placeholder_text: Texto opcional para mostrar como placeholder
    """
    # Aplicamos colores básicos
    entry.config(bg=tema['entry_bg'], fg=tema['entry_fg'], 
                insertbackground=tema['entry_fg'])
    
    # Si hay placeholder, lo configuramos
    if placeholder_text is not None:
        entry.delete(0, 'end')
        entry.insert(0, placeholder_text)
        entry.config(fg=tema['entry_placeholder'])

def aplicar_tema(widgets, tema):
    """
    Aplica un tema a todos los widgets principales de la aplicación.
    
    Args:
        widgets: Diccionario con los widgets a estilizar
        tema: Diccionario con los colores del tema a aplicar
    """
    # Aplicamos el tema a la ventana principal
    widgets['ventana'].config(bg=tema['bg'])
    
    # Aplicamos el tema a todos los labels
    for label in widgets['labels']:
        label.config(bg=tema['label_bg'], fg=tema['label_fg'])
    
    # Aplicamos el tema a todos los listboxes
    for lb in widgets['listboxes']:
        lb.config(bg=tema['listbox_bg'], fg=tema['listbox_fg'],
                 selectbackground='#4a4a7a', selectforeground='#fff')
    
    # Aplicamos el tema a todos los botones
    for boton in widgets['botones']:
        boton.config(bg=tema['boton_bg'], fg=tema['boton_fg'],
                    activebackground=tema['pomodoro_bg'],
                    activeforeground=tema['pomodoro_fg'])
    
    # Aplicamos el tema a todos los frames
    for frame in widgets.get('frames', []):
        frame.config(bg=tema['frame_bg'])
    
    # Aplicamos el tema al frame del Pomodoro si existe
    if 'pomodoro_frame' in widgets:
        widgets['pomodoro_frame'].config(bg=tema['pomodoro_bg'])
    
    # Aplicamos el tema al label del Pomodoro si existe
    if 'pomodoro_label' in widgets:
        widgets['pomodoro_label'].config(bg=tema['pomodoro_bg'],
                                       fg=tema['pomodoro_fg'])

def aplicar_tema_columna_izquierda(frame, widgets, tema):
    """
    Aplica un tema a los widgets de la columna izquierda.
    
    Args:
        frame: Frame principal de la columna
        widgets: Diccionario con los widgets a estilizar
        tema: Diccionario con los colores del tema a aplicar
    """
    # Aplicamos el tema al frame principal
    frame.config(bg=tema['bg'])
    
    # Aplicamos el tema al label si existe
    if 'label' in widgets:
        widgets['label'].config(bg=tema['bg'], fg=tema['label_fg'])
    
    # Aplicamos el tema al listbox si existe
    if 'listbox' in widgets:
        widgets['listbox'].config(bg=tema['listbox_bg'], fg=tema['listbox_fg'])
    
    # Aplicamos el tema a los botones si existen
    if 'botones' in widgets:
        for boton in widgets['botones']:
            boton.config(bg=tema['boton_bg'], fg=tema['boton_fg'],
                        activebackground=tema['pomodoro_bg'],
                        activeforeground=tema['pomodoro_fg'])
    
    # Aplicamos el tema al logo si existe
    if 'logo' in widgets and widgets['logo'] is not None:
        widgets['logo'].config(bg=tema['bg'])