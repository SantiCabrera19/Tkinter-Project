# tareas.py
# Funciones y estructura de datos para la gestión de tareas

from persistencia import guardar_tareas, cargar_tareas  # Importa funciones de persistencia

ruta_actual = None  # Ruta del archivo de datos actualmente cargado o guardado

def set_ruta_actual(ruta):
    global ruta_actual
    ruta_actual = ruta

def get_ruta_actual():
    return ruta_actual

# Al iniciar, no cargamos nada automáticamente
# Función para poblar los widgets con las tareas cargadas (para usar desde la UI)
tareas = []
tarea_en_proceso = None

def poblar_listbox_desde_tareas(listbox_pendientes, listbox_completadas, listbox_en_proceso=None):
    listbox_pendientes.delete(0, 'end')
    listbox_completadas.delete(0, 'end')
    if listbox_en_proceso:
        listbox_en_proceso.delete(0, 'end')
    for tarea in tareas:
        if tarea['completada']:
            listbox_completadas.insert('end', tarea['texto'])
        else:
            listbox_pendientes.insert('end', tarea['texto'])
    if listbox_en_proceso and tarea_en_proceso:
        listbox_en_proceso.insert('end', tarea_en_proceso)

def set_tarea_en_proceso(texto):
    global tarea_en_proceso
    tarea_en_proceso = texto
    # No guardar automáticamente

def agregar_tarea(texto, lista_tareas_widget, entry_widget):
    import tkinter.messagebox as messagebox
    if texto:
        # Validar duplicados (en pendientes, completadas o en proceso)
        texto_normalizado = texto.strip().lower()
        for tarea in tareas:
            if tarea['texto'].strip().lower() == texto_normalizado:
                messagebox.showerror("Duplicado", "Ya existe una tarea con ese texto.")
                return
        from tareas import tarea_en_proceso
        if tarea_en_proceso and tarea_en_proceso.strip().lower() == texto_normalizado:
            messagebox.showerror("Duplicado", "Ya existe una tarea en proceso con ese texto.")
            return
        lista_tareas_widget.insert('end', texto)
        entry_widget.delete(0, 'end')
        tareas.append({'texto': texto, 'completada': False})
        messagebox.showinfo("Tarea agregada", f"Tarea '{texto}' agregada correctamente.")
        # No guardar automáticamente

def eliminar_tarea(lista_tareas_widget):
    import tkinter.messagebox as messagebox
    seleccion = lista_tareas_widget.curselection()
    if seleccion:
        idx = seleccion[0]
        tarea_texto = tareas[idx]['texto']
        resp = messagebox.askyesno("Eliminar tarea", f"¿Seguro que deseas eliminar la tarea '{tarea_texto}'?")
        if resp:
            lista_tareas_widget.delete(idx)
            del tareas[idx]
            messagebox.showinfo("Tarea eliminada", f"Tarea '{tarea_texto}' eliminada correctamente.")
        # No guardar automáticamente

def marcar_como_completada(listbox_pendientes, listbox_completadas):
    import tkinter.messagebox as messagebox
    seleccion = listbox_pendientes.curselection()
    if seleccion:
        idx = seleccion[0]
        tarea = tareas[idx]
        tarea['completada'] = True
        listbox_completadas.insert('end', tarea['texto'])
        listbox_pendientes.delete(idx)
        tareas.append(tareas.pop(idx))
        messagebox.showinfo("Tarea completada", f"Tarea '{tarea['texto']}' marcada como completada.")
        # No guardar automáticamente

# Función para cargar tareas desde archivo y poblar la UI
def cargar_tareas_desde_archivo(listbox_pendientes, listbox_completadas, listbox_en_proceso=None):
    global tareas, tarea_en_proceso
    nuevas_tareas, nueva_en_proceso = cargar_tareas()
    if nuevas_tareas is not None:
        tareas = nuevas_tareas
        tarea_en_proceso = nueva_en_proceso
        poblar_listbox_desde_tareas(listbox_pendientes, listbox_completadas, listbox_en_proceso)
