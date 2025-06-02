import tkinter as tk

# Componente de barra de menú modular
class MenuDesplegable:
    def __init__(self, parent, on_modo_claro, on_modo_oscuro, on_guardar=None, on_cargar=None):
        self.menubar = tk.Menu(parent) # menú principal
        # Menú Archivo
        self.menu_archivo = tk.Menu(self.menubar, tearoff=0)
        if on_guardar:
            self.menu_archivo.add_command(label="Guardar datos", command=on_guardar)
        if on_cargar:
            self.menu_archivo.add_command(label="Cargar datos", command=on_cargar)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)
        # Menú Configuración
        self.menu_config = tk.Menu(self.menubar, tearoff=0) # menú de configuración, tearoff=0 es para que no se pueda deslizar
        # Submenú Modo
        self.menu_modo = tk.Menu(self.menu_config, tearoff=0) # menú de modo, tearoff=0 es para que no se pueda deslizar
        self.menu_modo.add_command(label="Claro", command=on_modo_claro) # comando para el modo claro
        self.menu_modo.add_command(label="Oscuro", command=on_modo_oscuro) # comando para el modo oscuro
        self.menu_config.add_cascade(label="Modo", menu=self.menu_modo) # menú de modo en el menú de configuración
        self.menubar.add_cascade(label="Configuración", menu=self.menu_config) # menú de configuración en el menú principal

    def get_menubar(self): 
        return self.menubar # devuelve el menú principal
