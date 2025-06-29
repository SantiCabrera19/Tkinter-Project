import tkinter as tk

# Clase que implementa la barra de menú de la aplicación
class MenuDesplegable:
    def __init__(self, parent, on_modo_claro, on_modo_oscuro, on_guardar=None, on_cargar=None):
        """
        Inicializa la barra de menú con sus opciones.
        
        Args:
            parent: Widget padre donde se creará el menú
            on_modo_claro: Callback para cambiar al modo claro
            on_modo_oscuro: Callback para cambiar al modo oscuro
            on_guardar: Callback opcional para guardar datos
            on_cargar: Callback opcional para cargar datos
        """
        # Creamos el menú principal
        self.menubar = tk.Menu(parent)
        
        # Creamos el menú Archivo
        self.menu_archivo = tk.Menu(self.menubar, tearoff=0)  # tearoff=0 evita que el menú se pueda desprender
        
        # Agregamos opciones al menú Archivo si se proporcionaron los callbacks
        if on_guardar:
            self.menu_archivo.add_command(label="Guardar datos", command=on_guardar)
        if on_cargar:
            self.menu_archivo.add_command(label="Cargar datos", command=on_cargar)
        
        # Agregamos el menú Archivo a la barra principal
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)
        
        # Creamos el menú Configuración
        self.menu_config = tk.Menu(self.menubar, tearoff=0)
        
        # Creamos el submenú Modo dentro de Configuración
        self.menu_modo = tk.Menu(self.menu_config, tearoff=0)
        
        # Agregamos las opciones de modo al submenú
        self.menu_modo.add_command(label="Claro", command=on_modo_claro)
        self.menu_modo.add_command(label="Oscuro", command=on_modo_oscuro)
        
        # Agregamos el submenú Modo al menú Configuración
        self.menu_config.add_cascade(label="Modo", menu=self.menu_modo)
        
        # Agregamos el menú Configuración a la barra principal
        self.menubar.add_cascade(label="Configuración", menu=self.menu_config)

    def get_menubar(self):
        """
        Devuelve la barra de menú configurada.
        
        Returns:
            tk.Menu: La barra de menú lista para usar
        """
        return self.menubar
