import tkinter as tk
import time
from widgets import crear_boton_pomodoro, crear_frame
from estilos import FONT_RELOJ, MODO_OSCURO

class Pomodoro(tk.Frame):
    """
    Implementa un temporizador tipo Pomodoro con modos de trabajo y descanso.
    """
    def __init__(self, parent, minutos_iniciales=10, on_finish=None):
        super().__init__(parent)
        # Variables privadas (por convención)
        self._tiempo_restante = minutos_iniciales * 60
        self._corriendo = False
        self._modo = 'trabajo'
        self._min_trabajo = 10
        self._min_descanso = 5
        self._on_finish = on_finish
        # Configuramos el estilo base
        self._configurar_estilo()
        # Creamos los widgets
        self._crear_widgets()
        # Configuramos el layout
        self._configurar_layout()

    def _configurar_estilo(self):
        """Configura el estilo base del widget"""
        self.config(bg=MODO_OSCURO['bg'], bd=2, relief="ridge")
        self.grid_propagate(True)
        self.update_idletasks()
        self.config(width=320, height=120)

    def _crear_widgets(self):
        """Crea todos los widgets necesarios"""
        # Frame interno
        self.frame = crear_frame(self)
        self.frame.config(bg=MODO_OSCURO['bg'])
        
        # Label del tiempo
        self.label = tk.Label(self.frame, font=FONT_RELOJ, bg=MODO_OSCURO['reloj_bg'], 
                            fg=MODO_OSCURO['reloj_fg'], pady=8, padx=20)
        
        # Botones de control
        self.boton_play = crear_boton_pomodoro(self.frame, "▶", self.iniciar)
        self.boton_pausa = crear_boton_pomodoro(self.frame, "⏸", self.pausar)
        self.boton_reset = crear_boton_pomodoro(self.frame, "⟳", self.resetear)
        self.boton_5 = crear_boton_pomodoro(self.frame, "+5 min", lambda: self.agregar_tiempo(5))
        self.boton_10 = crear_boton_pomodoro(self.frame, "+10 min", lambda: self.agregar_tiempo(10))
        
        # Botones de modo
        self.boton_trabajo = crear_boton_pomodoro(self.frame, "Trabajo", self.set_trabajo)
        self.boton_descanso = crear_boton_pomodoro(self.frame, "Descanso", self.set_descanso)
        
        # Botones de configuración
        self.boton_mas_trabajo = crear_boton_pomodoro(self.frame, "+1 trabajo", 
                                                     lambda: self.configurar_trabajo(1))
        self.boton_menos_trabajo = crear_boton_pomodoro(self.frame, "-1 trabajo", 
                                                      lambda: self.configurar_trabajo(-1))
        self.boton_mas_descanso = crear_boton_pomodoro(self.frame, "+1 desc", 
                                                     lambda: self.configurar_descanso(1))
        self.boton_menos_descanso = crear_boton_pomodoro(self.frame, "-1 desc", 
                                                       lambda: self.configurar_descanso(-1))
        
        # Label de modo
        self.label_modo = tk.Label(self.frame, text=self.get_modo_texto(), 
                                 bg=MODO_OSCURO['bg'], fg=MODO_OSCURO['fg'])

    def _configurar_layout(self):
        """Configura el layout de los widgets"""
        # Posicionamos el frame interno
        self.frame.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        
        # Posicionamos el label del tiempo
        self.label.grid(row=0, column=0, columnspan=6, sticky='ew', padx=5, pady=5)
        
        # Posicionamos los botones de control
        self.boton_play.grid(row=1, column=0, padx=5, pady=5)
        self.boton_pausa.grid(row=1, column=1, padx=5, pady=5)
        self.boton_reset.grid(row=1, column=2, padx=5, pady=5)
        self.boton_5.grid(row=1, column=3, padx=5, pady=5)
        self.boton_10.grid(row=1, column=4, padx=5, pady=5)
        
        # Posicionamos los botones de modo
        self.boton_trabajo.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        self.boton_descanso.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky='ew')
        
        # Posicionamos los botones de configuración
        self.boton_mas_trabajo.grid(row=2, column=4, padx=5, pady=5)
        self.boton_menos_trabajo.grid(row=2, column=5, padx=5, pady=5)
        self.boton_mas_descanso.grid(row=3, column=4, padx=5, pady=5)
        self.boton_menos_descanso.grid(row=3, column=5, padx=5, pady=5)
        
        # Posicionamos el label de modo
        self.label_modo.grid(row=3, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
        
        # Configuramos la expansión de widgets
        self.frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Actualizamos el label inicial
        self.actualizar_label()

    # Getters y setters para propiedades privadas
    # El decorador @property en Python permite definir métodos que se acceden como atributos.
    # El símbolo @ se llama "decorador" y modifica el comportamiento de la función que sigue.
    # Acá, @property convierte el método en un getter, así podés hacer obj.tiempo_restante en vez de obj.tiempo_restante()
    #
    # El guion bajo "_" al inicio de una variable (ej: self._tiempo_restante) es una convención FUERTE en Python para indicar que es PRIVADA: no la toques desde afuera de la clase.
    # No es privado real (como en otros lenguajes), pero es una advertencia para otros programadores: "esto es interno, no lo uses afuera".
    #
    # El setter con @<propiedad>.setter permite asignar el valor como si fuera un atributo, pero ejecutando lógica personalizada.
    @property  # <- DECORADOR: esto hace que el método funcione como un atributo de solo lectura
    def tiempo_restante(self):
        return self._tiempo_restante  # _variable: CONVENCIÓN de privado, no tocar desde afuera

    @tiempo_restante.setter  # <- DECORADOR: esto permite asignar con obj.tiempo_restante = valor
    def tiempo_restante(self, valor):
        if valor >= 0:
            self._tiempo_restante = valor
            self.actualizar_label()

    @property
    def corriendo(self):
        return self._corriendo

    @corriendo.setter
    def corriendo(self, valor):
        self._corriendo = valor

    @property
    def modo(self):
        return self._modo

    @modo.setter
    def modo(self, valor):
        if valor in ['trabajo', 'descanso']:
            self._modo = valor
            self.actualizar_label_modo()

    def actualizar_label(self):
        # Convierte el tiempo restante en segundos a formato MM:SS
        minutos = self._tiempo_restante // 60
        segundos = self._tiempo_restante % 60
        self.label.config(text=f"{minutos:02}:{segundos:02}")

    def actualizar_label_modo(self):
        # Actualiza el texto del label de modo con la configuración actual
        self.label_modo.config(text=self.get_modo_texto())

    def get_modo_texto(self):
        # Genera el texto que muestra el modo actual y los tiempos configurados
        return f"Modo: {self._modo.capitalize()} | Trabajo: {self._min_trabajo} min | Descanso: {self._min_descanso} min"

    def tick(self):
        # Función que se ejecuta cada segundo para actualizar el temporizador
        if self._corriendo and self._tiempo_restante > 0:
            # Si está corriendo y hay tiempo restante, decrementamos
            self._tiempo_restante -= 1
            self.actualizar_label()
            # Programamos el próximo tick
            self.after(1000, self.tick)
        elif self._tiempo_restante == 0:
            # Si se acabó el tiempo
            self._corriendo = False
            self.label.config(text="¡Tiempo!")
            # Ejecutamos el callback de finalización si existe
            if self._on_finish:
                self._on_finish()

    def iniciar(self):
        # Inicia el temporizador si no está corriendo y hay tiempo restante
        if not self._corriendo and self._tiempo_restante > 0:
            self._corriendo = True
            self.tick()

    def pausar(self):
        # Pausa el temporizador
        self._corriendo = False

    def resetear(self):
        # Reinicia el temporizador al tiempo inicial del modo actual
        if self._modo == 'trabajo':
            self._tiempo_restante = self._min_trabajo * 60
        else:
            self._tiempo_restante = self._min_descanso * 60
        self.actualizar_label()
        self._corriendo = False

    def agregar_tiempo(self, minutos):
        # Agrega minutos al tiempo restante actual
        self._tiempo_restante += minutos * 60
        self.actualizar_label()

    def set_trabajo(self):
        # Cambia al modo trabajo y reinicia el temporizador
        self._modo = 'trabajo'
        self._tiempo_restante = self._min_trabajo * 60
        self.actualizar_label()
        self.actualizar_label_modo()
        self._corriendo = False

    def set_descanso(self):
        # Cambia al modo descanso y reinicia el temporizador
        self._modo = 'descanso'
        self._tiempo_restante = self._min_descanso * 60
        self.actualizar_label()
        self.actualizar_label_modo()
        self._corriendo = False

    def configurar_trabajo(self, delta):
        # Ajusta el tiempo de trabajo, mínimo 1 minuto
        self._min_trabajo = max(1, self._min_trabajo + delta)
        # Si estamos en modo trabajo, actualizamos el tiempo restante
        if self._modo == 'trabajo':
            self._tiempo_restante = self._min_trabajo * 60
            self.actualizar_label()
        self.actualizar_label_modo()

    def configurar_descanso(self, delta):
        # Ajusta el tiempo de descanso, mínimo 1 minuto
        self._min_descanso = max(1, self._min_descanso + delta)
        # Si estamos en modo descanso, actualizamos el tiempo restante
        if self._modo == 'descanso':
            self._tiempo_restante = self._min_descanso * 60
            self.actualizar_label()
        self.actualizar_label_modo()

    # Métodos para posicionar el widget en la interfaz
    def grid(self, **kwargs):
        super().grid(**kwargs) # super() es una referencia a la clase padre (tk.Frame)

    def pack(self, **kwargs):
        super().pack(**kwargs) # super() es una referencia a la clase padre (tk.Frame)

    # Explicacion sustancial de porque los metodos para posicionar el widget en la interfaz son necesarios
    # y que diferencia hay entre grid y pack
    #
    # grid: es una grilla que permite posicionar el widget en una posición específica de la grilla.
    # pack: es un empaquetado que permite posicionar el widget en una posición específica de la ventana.
    #
    # grid es más flexible y permite posicionar el widget en una posición específica de la grilla.
    # pack es más simple y permite posicionar el widget en una posición específica de la ventana.
