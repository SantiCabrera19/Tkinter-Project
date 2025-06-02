import tkinter as tk
import time
from widgets import crear_boton_pomodoro, crear_frame
from estilos import FONT_RELOJ, MODO_OSCURO

# Clase para el reloj
class Pomodoro:
    # Constructor de la clase
    def __init__(self, parent, minutos_iniciales=10, on_finish=None): # on_finish=None basicamente por si no se le pasa un callback, es decir un parametro que se ejecuta cuando se termina el pomodoro

        # Atributos self es el objeto de la clase, parent es el widget padre, minutos_iniciales es el tiempo inicial, on_finish es el callback al terminar
        self.parent = parent # widget padre
        self.minutos_iniciales = minutos_iniciales # minutos por defecto
        self.tiempo_restante = minutos_iniciales * 60 # tiempo restante en segundos, se iran disminuyendo cada segundo por la funcion tick
        self.corriendo = False # bandera de si está corriendo
        self.on_finish = on_finish # callback al terminar
        self.modo = 'trabajo' # 'trabajo' o 'descanso'
        self.min_trabajo = 10 # minutos de trabajo por defecto
        self.min_descanso = 5 # minutos de descanso por defecto
        # Frame de fondo para resaltar el Pomodoro
        self.bg_frame = tk.Frame(parent, bg=MODO_OSCURO['bg'], bd=2, relief="ridge") # bg es el color de fondo del frame
        self.bg_frame.grid_propagate(True) # para que el frame se ajuste al contenido
        self.bg_frame.update_idletasks() # para que el frame se ajuste al contenido, usando update_idletasks que es una función de tkinter que actualiza el frame
        self.bg_frame.config(width=320, height=120) # ancho y alto del frame 
        self.frame = crear_frame(self.bg_frame) # frame para los botones y el reloj
        self.frame.config(bg=MODO_OSCURO['bg']) # color de fondo del frame
        self.frame.grid(row=0, column=0, sticky='nsew', padx=0, pady=0) # posición del frame (fila, columna, sticky, padding horizontal, padding vertical)
        # Label del reloj
        self.label = tk.Label(self.frame, font=FONT_RELOJ, bg=MODO_OSCURO['reloj_bg'], fg=MODO_OSCURO['reloj_fg'], pady=8, padx=20) # label para mostrar el tiempo restante
        self.label.grid(row=0, column=0, columnspan=6, sticky='ew', padx=5, pady=5) # posición del label (fila, columna, span, sticky, padding horizontal, padding vertical)
        self.actualizar_label() # actualiza el label del reloj
        # Botón Play
        self.boton_play = crear_boton_pomodoro(self.frame, "▶", self.iniciar) # botón para iniciar el pomodoro
        self.boton_play.grid(row=1, column=0, padx=5, pady=5) # posición del botón (fila, columna, padding horizontal, padding vertical)
        # Botón Pausa
        self.boton_pausa = crear_boton_pomodoro(self.frame, "⏸", self.pausar) # botón para pausar el pomodoro
        self.boton_pausa.grid(row=1, column=1, padx=5, pady=5)
        # Botón Reset
        self.boton_reset = crear_boton_pomodoro(self.frame, "⟳", self.resetear) # botón para resetear el pomodoro
        self.boton_reset.grid(row=1, column=2, padx=5, pady=5) # posición del botón (fila, columna, padding horizontal, padding vertical)
        # Botón +5 min
        self.boton_5 = crear_boton_pomodoro(self.frame, "+5 min", lambda: self.agregar_tiempo(5)) # botón para agregar 5 minutos al pomodoro
        self.boton_5.grid(row=1, column=3, padx=5, pady=5) # posición del botón (fila, columna, padding horizontal, padding vertical)               
        # Botón +10 min
        self.boton_10 = crear_boton_pomodoro(self.frame, "+10 min", lambda: self.agregar_tiempo(10)) # botón para agregar 10 minutos al pomodoro
        self.boton_10.grid(row=1, column=4, padx=5, pady=5) # posición del botón (fila, columna, padding horizontal, padding vertical)
        # Botón para cambiar a modo trabajo
        self.boton_trabajo = crear_boton_pomodoro(self.frame, "Trabajo", self.set_trabajo) # botón para cambiar a modo trabajo
        self.boton_trabajo.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew') # posición del botón (fila, columna, span, padding horizontal, padding vertical, sticky)
        # Botón para cambiar a modo descanso
        self.boton_descanso = crear_boton_pomodoro(self.frame, "Descanso", self.set_descanso) # botón para cambiar a modo descanso
        self.boton_descanso.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky='ew') # posición del botón (fila, columna, span, padding horizontal, padding vertical, sticky)
        # Botón para configurar minutos de trabajo
        self.boton_mas_trabajo = crear_boton_pomodoro(self.frame, "+1 trabajo", lambda: self.configurar_trabajo(1)) # botón para agregar 1 minuto de trabajo
        self.boton_mas_trabajo.grid(row=2, column=4, padx=5, pady=5) # posición del botón (fila, columna, padding horizontal, padding vertical)
        self.boton_menos_trabajo = crear_boton_pomodoro(self.frame, "-1 trabajo", lambda: self.configurar_trabajo(-1)) # botón para restar 1 minuto de trabajo
        self.boton_menos_trabajo.grid(row=2, column=5, padx=5, pady=5) # posición del botón (fila, columna, padding horizontal, padding vertical)
        # Botón para configurar minutos de descanso 
        self.boton_mas_descanso = crear_boton_pomodoro(self.frame, "+1 desc", lambda: self.configurar_descanso(1)) # botón para agregar 1 minuto de descanso
        self.boton_mas_descanso.grid(row=3, column=4, padx=5, pady=5) # posición del botón (fila, columna, padding horizontal, padding vertical)
        self.boton_menos_descanso = crear_boton_pomodoro(self.frame, "-1 desc", lambda: self.configurar_descanso(-1)) # botón para restar 1 minuto de descanso
        self.boton_menos_descanso.grid(row=3, column=5, padx=5, pady=5) # posición del botón (fila, columna, padding horizontal, padding vertical)
        # Label para mostrar modo y tiempos
        self.label_modo = tk.Label(self.frame, text=self.get_modo_texto(), bg=MODO_OSCURO['bg'], fg=MODO_OSCURO['fg']) # label para mostrar el modo y los tiempos
        self.label_modo.grid(row=3, column=0, columnspan=4, sticky='ew', padx=5, pady=5) # posición del label (fila, columna, span, sticky, padding horizontal, padding vertical)
        # Expansión
        self.frame.grid_columnconfigure((0,1,2,3,4,5), weight=1) # expansión de las columnas
        self.bg_frame.grid_rowconfigure(0, weight=1) # expansión de la fila
        self.bg_frame.grid_columnconfigure(0, weight=1) # expansión de la columna

    # Funcion que actualiza el label del reloj
    def actualizar_label(self): # parametros: self es el objeto de la clase
        minutos = self.tiempo_restante // 60 # división entera de tiempo_restante entre 60
        segundos = self.tiempo_restante % 60 # resto de la división entera de tiempo_restante entre 60
        self.label.config(text=f"{minutos:02}:{segundos:02}") # actualiza el label del reloj con el tiempo restante

    # Actualiza el label de modo y tiempos
    def actualizar_label_modo(self): 
        self.label_modo.config(text=self.get_modo_texto())

    # Devuelve el texto del modo actual
    def get_modo_texto(self):
        return f"Modo: {self.modo.capitalize()} | Trabajo: {self.min_trabajo} min | Descanso: {self.min_descanso} min"

    # Tick del temporizador
    def tick(self):
        if self.corriendo and self.tiempo_restante > 0: # Si está corriendo y el tiempo restante es mayor que 0
            self.tiempo_restante -= 1 # Se disminuye el tiempo restante en 1 segundo
            self.actualizar_label() # Se actualiza el label del reloj
            self.parent.after(1000, self.tick) # Se llama a la función tick cada segundo
        elif self.tiempo_restante == 0: # Si el tiempo restante es 0
            self.corriendo = False # Se desactiva la bandera de corriendo, es decir se desactiva el temporizador
            self.label.config(text="¡Tiempo!") # Se actualiza el label del reloj
            if self.on_finish: # Si se le pasó un callback al terminar
                self.on_finish() # Se llama al callback (Tiempo terminado)

    # Inicia el Pomodoro
    def iniciar(self):
        if not self.corriendo and self.tiempo_restante > 0: # Si no está corriendo y el tiempo restante es mayor que 0
            self.corriendo = True # Se activa la bandera de corriendo, es decir se activa el temporizador
            self.tick() # Se llama a la función tick que va a ir disminuyendo el tiempo restante cada segundo

    # Pausa el Pomodoro
    def pausar(self):
        self.corriendo = False

    # Resetea el Pomodoro al valor inicial del modo actual
    def resetear(self):
        if self.modo == 'trabajo':
            self.tiempo_restante = self.min_trabajo * 60
        else:
            self.tiempo_restante = self.min_descanso * 60
        self.actualizar_label()
        self.corriendo = False

    # Agrega minutos al temporizador
    def agregar_tiempo(self, minutos):
        self.tiempo_restante += minutos * 60
        self.actualizar_label()

    # Cambia a modo trabajo
    def set_trabajo(self):
        self.modo = 'trabajo'
        self.tiempo_restante = self.min_trabajo * 60
        self.actualizar_label()
        self.actualizar_label_modo()
        self.corriendo = False

    # Cambia a modo descanso
    def set_descanso(self):
        self.modo = 'descanso'
        self.tiempo_restante = self.min_descanso * 60
        self.actualizar_label()
        self.actualizar_label_modo()
        self.corriendo = False

    # Configura minutos de trabajo
    def configurar_trabajo(self, delta):
        self.min_trabajo = max(1, self.min_trabajo + delta)
        if self.modo == 'trabajo':
            self.tiempo_restante = self.min_trabajo * 60
            self.actualizar_label()
        self.actualizar_label_modo()

    # Configura minutos de descanso
    def configurar_descanso(self, delta):
        self.min_descanso = max(1, self.min_descanso + delta)
        if self.modo == 'descanso':
            self.tiempo_restante = self.min_descanso * 60
            self.actualizar_label()
        self.actualizar_label_modo()

    # Métodos para grid y pack
    def grid(self, **kwargs):
        self.bg_frame.grid(**kwargs)

    def pack(self, **kwargs):
        self.bg_frame.pack(**kwargs)
