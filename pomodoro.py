import tkinter as tk # importamos tkinter
import tkinter.messagebox as messagebox # importamos messagebox
from widgets import crear_entry_con_placeholder, crear_listbox_con_label, crear_boton, actualizar_label_con_contador, crear_listbox_en_proceso # importamos los widgets
from tareas import agregar_tarea, eliminar_tarea, marcar_como_completada, poblar_listbox_desde_tareas, set_tarea_en_proceso, cargar_tareas_desde_archivo, get_ruta_actual, set_ruta_actual, tareas, tarea_en_proceso # importamos las tareas y funciones de ruta
from estilos import PADDING_X, PADDING_Y, MODO_CLARO, MODO_OSCURO, aplicar_tema, aplicar_tema_columna_izquierda # importamos los estilos
from reloj import Pomodoro # importamos el reloj
from menu_despl import MenuDesplegable # importamos el menú desplegable
import os # importamos os, necesario para el path de la imagen
from PIL import Image, ImageTk # importamos Image y ImageTk, necesario para la imagen del logo
from PIL import ImageDraw # importamos ImageDraw, necesario para la imagen del logo

modo_actual = {'tema': MODO_CLARO} # modo actual, por defecto es claro

ventana = tk.Tk() # creamos la ventana
ventana.title('Pomodoro🍅') # título de la ventana
ventana.geometry('1000x700') # tamaño de la ventana
ventana.resizable(False, False) # No permitir maximizar ni redimensionar

# Frame horizontal para Entry y botón de agregar, centrado y ancho limitado
frame_entry = tk.Frame(ventana, bg=modo_actual['tema']['bg'])
frame_entry.grid(row=0, column=0, columnspan=3, pady=(PADDING_Y, 0))

# Entry con decorado visual y placeholder
entry_frame, entry = crear_entry_con_placeholder(frame_entry, 'Escribe una tarea…', modo_actual['tema'], width=32)
entry_frame.pack(side=tk.LEFT, padx=(0, 8))

boton_agregar = crear_boton(frame_entry, 'Agregar tarea', lambda: (agregar_tarea(entry.get(), listbox_pendientes, entry), actualizar_contadores()))
boton_agregar.pack(side=tk.LEFT)


# Frame para la columna izquierda
frame_izq = tk.Frame(ventana, bg=modo_actual['tema']['bg']) 
frame_izq.grid(row=2, column=0, rowspan=10, sticky='n', padx=(30, 0), pady=(20, 0))

# Label y listbox de pendientes en frame_izq
label_pend, frame_pend, listbox_pendientes = crear_listbox_con_label(frame_izq, 'Pendientes', use_scroll=True)
label_pend.config(bg=modo_actual['tema']['bg'], fg=modo_actual['tema']['label_fg'])
label_pend.pack(pady=(0, 5))
frame_pend.pack(pady=(0, 10))  # No expand ni fill

# Frame para los botones debajo de pendientes
def asociar_tarea_en_proceso(): # función para asociar una tarea a la tarea en proceso
    seleccion = listbox_pendientes.curselection() # seleccion es la tarea seleccionada
    if seleccion: # si hay una tarea seleccionada entonces
        idx = seleccion[0] # idx es el índice de la tarea seleccionada
        tarea = listbox_pendientes.get(idx) # tarea es la tarea seleccionada
        if listbox_en_proceso.size() > 0: # si hay una tarea en proceso entonces
            tarea_en_proceso = listbox_en_proceso.get(0) # tarea_en_proceso es la tarea en proceso
            if tarea_en_proceso == tarea: # si la tarea en proceso es igual a la tarea seleccionada entonces
                return # se retorna
            resp = messagebox.askyesno( # se pregunta si se quiere reemplazar la tarea en proceso
                "Reemplazar tarea en proceso",
                f"¿Quieres reemplazar la tarea '{tarea_en_proceso}' por '{tarea}' en proceso?"
            )
            if not resp:
                return
            listbox_en_proceso.delete(0, 'end')
        listbox_en_proceso.insert('end', tarea)
        set_tarea_en_proceso(tarea)  # Persistir tarea en proceso

frame_botones_pendientes = tk.Frame(frame_izq, bg=modo_actual['tema']['bg'])
frame_botones_pendientes.pack(pady=(0, 10))

boton_eliminar = crear_boton(frame_botones_pendientes, 'Eliminar tarea', lambda: (eliminar_tarea(listbox_pendientes), actualizar_contadores()))
boton_eliminar.config(bg=modo_actual['tema']['boton_bg'], fg=modo_actual['tema']['boton_fg'])
boton_eliminar.pack(side=tk.TOP, fill=tk.X, pady=2)
boton_completar = crear_boton(frame_botones_pendientes, 'Marcar como completada', lambda: (marcar_como_completada(listbox_pendientes, listbox_completadas), actualizar_contadores()))
boton_completar.config(bg=modo_actual['tema']['boton_bg'], fg=modo_actual['tema']['boton_fg'])
boton_completar.pack(side=tk.TOP, fill=tk.X, pady=2)
boton_asociar = crear_boton(frame_botones_pendientes, 'Iniciar Pomodoro con tarea', asociar_tarea_en_proceso)
boton_asociar.config(bg=modo_actual['tema']['boton_bg'], fg=modo_actual['tema']['boton_fg'])
boton_asociar.pack(side=tk.TOP, fill=tk.X, pady=2)

# Logo Pomodoro debajo de los botones de pendientes, centrado, usando pomodoro_logo2.png
logo_path = os.path.join(os.path.dirname(__file__), 'pomodoro_logo2.png') # logo_path es el path de la imagen del logo
if os.path.exists(logo_path): # si existe la imagen del logo entonces
    img = Image.open(logo_path).convert('RGBA') # se abre la imagen del logo y se convierte a RGBA
    img = img.resize((180, 180), Image.LANCZOS) # se redimensiona la imagen del logo
    # Máscara circular
    mask = Image.new('L', (180, 180), 0) # se crea una máscara circular
    draw = ImageDraw.Draw(mask) # se crea un dibujo en la máscara
    draw.ellipse((0, 0, 180, 180), fill=255) # se dibuja una elipse en la máscara
    img.putalpha(mask) # se aplica la máscara a la imagen
    pomodoro_logo_img = ImageTk.PhotoImage(img) # se convierte la imagen a un objeto PhotoImage
    label_logo = tk.Label(frame_izq, image=pomodoro_logo_img, bg=modo_actual['tema']['bg'], bd=0, highlightthickness=0)
    label_logo.image = pomodoro_logo_img  # Referencia para evitar garbage collection
    label_logo.pack(pady=(20, 0)) # se pack para el label del logo
else:
    label_logo = None # si no existe la imagen del logo entonces se asigna None

# Columna derecha: Completadas
label_comp, frame_comp, listbox_completadas = crear_listbox_con_label(ventana, 'Completadas', use_scroll=True)
label_comp.grid(row=2, column=1, padx=PADDING_X, pady=(PADDING_Y, 0), sticky='n')
frame_comp.grid(row=3, column=1, padx=PADDING_X, pady=(0, PADDING_Y), sticky='n')

# Configuramos las columnas para que se expandan cuando se expanda la ventana
ventana.grid_columnconfigure(0, weight=1) # Configuramos la columna 0 para que se expanda
ventana.grid_columnconfigure(1, weight=1) # Configuramos la columna 1 para que se expanda

# Función para actualizar los contadores
def actualizar_contadores():
    actualizar_label_con_contador(label_pend, 'Pendientes', listbox_pendientes.size()) # actualiza el label con el número de pendientes
    actualizar_label_con_contador(label_comp, 'Completadas', listbox_completadas.size())

# Función para manejar Enter

PLACEHOLDER = 'Escribe una tarea…' # placeholder para el entry
def on_enter(event=None): # función para manejar el enter
    if entry.focus_get() == entry: # si el entry tiene el focus entonces
        texto = entry.get() # se agrega la tarea
        if texto and texto != PLACEHOLDER: # si el texto no es vacio y no es el placeholder entonces
            agregar_tarea(texto, listbox_pendientes, entry) # se agrega la tarea a la lista de pendientes
            actualizar_contadores() # se actualiza el contador de pendientes
    else: # si el entry no tiene el focus entonces
        seleccion = listbox_pendientes.curselection() # se selecciona la tarea
        if seleccion: # si hay una tarea seleccionada entonces
            marcar_como_completada(listbox_pendientes, listbox_completadas) # se marca la tarea como completada
            actualizar_contadores() # se actualiza el contador de pendientes

ventana.bind('<Return>', on_enter) # se bindea el enter a la función on_enter ('<Return>' es el enter)

actualizar_contadores() # se actualiza el contador de pendientes

# Después de crear listbox_completadas...
# agregamos el Pomodoro
def on_pomodoro_finish():
    # Chequeamos el modo actual del Pomodoro
    if pomodoro.modo == 'trabajo':
        tarea = listbox_en_proceso.get(0) if listbox_en_proceso.size() > 0 else None
        if not tarea:
            messagebox.showinfo("Pomodoro terminado", "¡Tiempo terminado! No hay tarea en proceso.")
            return
        # Si hay tarea en proceso, preguntamos qué hacer con ella
        respuesta = messagebox.askyesnocancel(
            "Pomodoro terminado",
            f"¿Agregar '{tarea}' a completadas? (Sí para completar, No para agregar 5 min, Cancelar para dejar en proceso)"
        )
        if respuesta is True:
            # Buscar y mover la tarea de pendientes a completadas
            for idx in range(listbox_pendientes.size()): # recorremos la lista de pendientes
                if listbox_pendientes.get(idx) == tarea: # si la tarea de pendientes es igual a la tarea entonces
                    listbox_pendientes.delete(idx) # eliminamos la tarea de pendientes
                    listbox_completadas.insert('end', tarea) # insertamos la tarea en completadas
                    listbox_en_proceso.delete(0, 'end') # eliminamos la tarea en proceso
                    set_tarea_en_proceso(None)  # Limpiar tarea en proceso
                    actualizar_contadores() # actualizamos los contadores
                    break # salimos del bucle
        elif respuesta is False: # si no queremos agregar la tarea a completadas entonces
            pomodoro.agregar_tiempo(5) # agregamos 5 minutos al pomodoro
        # Si es None (cancel), no hace nada
    elif pomodoro.modo == 'descanso':
        # Si estamos en modo descanso, mostramos mensaje diferente
        respuesta = messagebox.askyesnocancel(
            "Descanso terminado",
            "¡Descanso terminado! ¿Listo para volver al trabajo?\n\nSí: Empezar trabajo\nNo: Agregar 5 min de descanso\nCancelar: Quedarse en descanso"
        )
        if respuesta is True:
            pomodoro.set_trabajo() # Cambiamos a modo trabajo y reseteamos el tiempo
        elif respuesta is False:
            pomodoro.agregar_tiempo(5) # Agregamos 5 minutos de descanso
        # Si es None (cancel), no hace nada

# Después de crear el Pomodoro
label_en_proceso, frame_en_proceso, listbox_en_proceso = crear_listbox_en_proceso(ventana, use_scroll=True, width=30, height=3)
label_en_proceso.grid(row=6, column=1, padx=0, pady=(PADDING_Y, 0), sticky='n')
frame_en_proceso.grid(row=7, column=1, padx=0, pady=(0, 0), sticky='n')
frame_en_proceso.grid_propagate(False)
frame_en_proceso.config(width=220, height=70)  # Ajustar si querés más o menos ancho/alto
listbox_en_proceso.config(width=30, height=3)

# Frame y botones debajo de 'En proceso'
frame_botones_en_proceso = tk.Frame(ventana)
frame_botones_en_proceso.grid(row=8, column=1, padx=0, pady=(0, PADDING_Y), sticky='n')

# Función para terminar la tarea en proceso
def terminar_tarea_en_proceso():
    if listbox_en_proceso.size() > 0:
        tarea = listbox_en_proceso.get(0)
        for idx in range(listbox_pendientes.size()):
            if listbox_pendientes.get(idx) == tarea:
                listbox_pendientes.delete(idx)
                listbox_completadas.insert('end', tarea)
                listbox_en_proceso.delete(0, 'end')
                set_tarea_en_proceso(None)  # Limpiar tarea en proceso
                actualizar_contadores()
                break

# Función para quitar la tarea en proceso
def quitar_tarea_en_proceso():
    if listbox_en_proceso.size() > 0:
        listbox_en_proceso.delete(0, 'end')
        set_tarea_en_proceso(None)  # Limpiar tarea en proceso

# Botones debajo de 'En proceso'
boton_terminar = crear_boton(frame_botones_en_proceso, 'Terminar tarea', terminar_tarea_en_proceso) # pack para el botón de terminar tarea en proceso
boton_terminar.pack(side=tk.TOP, fill=tk.X, pady=2, anchor='center') # pack para el botón de terminar tarea en proceso
 
# Botón para quitar la tarea en proceso
boton_quitar = crear_boton(frame_botones_en_proceso, 'Quitar de en proceso', quitar_tarea_en_proceso) # pack para el botón de quitar tarea en proceso
boton_quitar.pack(side=tk.TOP, fill=tk.X, pady=2, anchor='center') # pack para el botón de quitar tarea en proceso

pomodoro = Pomodoro(ventana, on_finish=on_pomodoro_finish)
pomodoro.grid(row=4, column=1, rowspan=2, padx=(PADDING_X, PADDING_X), pady=(PADDING_Y, 0), sticky='n')

# ... ahora definir widgets_tema ...
widgets_tema = {
    'ventana': ventana,
    'labels': [label_pend, label_comp, label_en_proceso],
    'listboxes': [listbox_pendientes, listbox_completadas, listbox_en_proceso],
    'botones': [boton_eliminar, boton_completar, boton_asociar, boton_terminar, boton_quitar],
    'frames': [frame_botones_pendientes, frame_botones_en_proceso],
    'pomodoro_frame': pomodoro,
    'pomodoro_label': pomodoro.label,
}
aplicar_tema(widgets_tema, MODO_CLARO)

def set_modo(modo, revertible=True):
    tema = MODO_CLARO if modo == 'claro' else MODO_OSCURO
    aplicar_tema(widgets_tema, tema)
    # Aplico el tema a la columna izquierda
    aplicar_tema_columna_izquierda(
        frame_izq,
        {
            'label': label_pend,
            'listbox': listbox_pendientes,
            'botones': [boton_eliminar, boton_completar, boton_asociar],
            'logo': label_logo
        },
        tema
    )
    entry.config(bg=tema['entry_bg'], fg=tema['entry_fg'], insertbackground=tema['entry_fg'])
    modo_actual['tema'] = tema
    if revertible:
        resp = messagebox.askyesno(f"Modo {modo.capitalize()} aplicado", f"Modo {modo.capitalize()} aplicado. ¿Aceptar el cambio? (No para revertir)")
        if not resp:
            otro = 'oscuro' if modo == 'claro' else 'claro'
            set_modo(otro, revertible=False)

def set_modo_claro():
    set_modo('claro')
def set_modo_oscuro():
    set_modo('oscuro')

# --- Callbacks para el menú (deben estar antes de crear el menú) ---
def on_guardar_datos():
    from persistencia import guardar_tareas
    import tkinter.messagebox as messagebox
    resp = messagebox.askyesno("Guardar datos", "¿Deseas guardar los datos actuales?")
    if resp:
        try:
            guardar_tareas(tareas, tarea_en_proceso)  # Pide ruta al usuario
            messagebox.showinfo("Guardado", "Datos guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))
    # Si elige No, no hace nada

def on_cargar_datos():
    import tkinter.messagebox as messagebox
    try:
        cargar_tareas_desde_archivo(listbox_pendientes, listbox_completadas, listbox_en_proceso)
        messagebox.showinfo("Cargado", "Datos cargados correctamente.")
    except Exception as e:
        messagebox.showerror("Error al cargar", str(e))

# --- Fin callbacks menú ---

# Ahora crear el menú, después de definir todos los callbacks y funciones necesarias
menu = MenuDesplegable(
    ventana,
    set_modo_claro,
    set_modo_oscuro,
    on_guardar=on_guardar_datos,
    on_cargar=on_cargar_datos
)
ventana.config(menu=menu.get_menubar())

poblar_listbox_desde_tareas(listbox_pendientes, listbox_completadas, listbox_en_proceso)  # Pobla los listbox con las tareas guardadas

# Handler de cierre de ventana con confirmación y opciones de guardado
def on_cerrar():
    resp = messagebox.askyesnocancel(
        "¿Deseas salir?",
        "¿Deseas guardar antes de salir? (Sí: guardar y salir, No: salir sin guardar, Cancelar: no salir)",
        icon='question'
    )
    if resp is True:
        from persistencia import guardar_tareas
        try:
            guardar_tareas(tareas, tarea_en_proceso)
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))
        ventana.destroy()
    elif resp is False:
        ventana.destroy()
    else:
        return

ventana.protocol("WM_DELETE_WINDOW", on_cerrar)

ventana.mainloop()