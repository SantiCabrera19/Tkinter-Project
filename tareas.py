# tareas.py
# Funciones y estructura de datos para la gestión de tareas

from persistencia import guardar_tareas, cargar_tareas  # Importa funciones de persistencia

# Variable global para almacenar la ruta del archivo de datos actual
ruta_actual = None

def set_ruta_actual(ruta):
    # Actualiza la ruta del archivo de datos actual
    global ruta_actual
    ruta_actual = ruta

def get_ruta_actual():
    # Devuelve la ruta del archivo de datos actual
    return ruta_actual

# Lista global que almacena todas las tareas
# Cada tarea es un diccionario con formato: {'texto': str, 'completada': bool}
tareas = []

# Variable global que almacena la tarea actualmente en proceso
tarea_en_proceso = None

def poblar_listbox_desde_tareas(listbox_pendientes, listbox_completadas, listbox_en_proceso=None):
    # Limpia todos los listboxes
    listbox_pendientes.delete(0, 'end')
    listbox_completadas.delete(0, 'end')
    if listbox_en_proceso:
        listbox_en_proceso.delete(0, 'end')
    
    # Recorre todas las tareas y las agrega al listbox correspondiente
    for tarea in tareas:
        if tarea['completada']:
            listbox_completadas.insert('end', tarea['texto'])
        else:
            listbox_pendientes.insert('end', tarea['texto'])
    
    # Si hay una tarea en proceso, la muestra en su listbox
    if listbox_en_proceso and tarea_en_proceso:
        listbox_en_proceso.insert('end', tarea_en_proceso)

def set_tarea_en_proceso(texto):
    # Actualiza la tarea en proceso
    global tarea_en_proceso
    tarea_en_proceso = texto

def agregar_tarea(texto, lista_tareas_widget, entry_widget):
    import tkinter.messagebox as messagebox
    
    if texto:
        # Normaliza el texto para comparación (elimina espacios y convierte a minúsculas)
        texto_normalizado = texto.strip().lower()
        
        # Verifica duplicados en la lista de tareas
        for tarea in tareas:
            if tarea['texto'].strip().lower() == texto_normalizado:
                messagebox.showerror("Duplicado", "Ya existe una tarea con ese texto.")
                return
        
        # Verifica duplicados con la tarea en proceso
        from tareas import tarea_en_proceso
        if tarea_en_proceso and tarea_en_proceso.strip().lower() == texto_normalizado:
            messagebox.showerror("Duplicado", "Ya existe una tarea en proceso con ese texto.")
            return
        
        # Agrega la tarea a la interfaz y a la lista de tareas
        lista_tareas_widget.insert('end', texto)
        entry_widget.delete(0, 'end')
        tareas.append({'texto': texto, 'completada': False})
        messagebox.showinfo("Tarea agregada", f"Tarea '{texto}' agregada correctamente.")

def eliminar_tarea(lista_tareas_widget):
    import tkinter.messagebox as messagebox
    
    # Obtiene la tarea seleccionada
    seleccion = lista_tareas_widget.curselection()
    if seleccion:
        idx = seleccion[0]
        tarea_texto = tareas[idx]['texto']
        
        # Pide confirmación antes de eliminar
        resp = messagebox.askyesno("Eliminar tarea", f"¿Seguro que deseas eliminar la tarea '{tarea_texto}'?")
        if resp:
            # Elimina la tarea de la interfaz y de la lista
            lista_tareas_widget.delete(idx)
            del tareas[idx]
            messagebox.showinfo("Tarea eliminada", f"Tarea '{tarea_texto}' eliminada correctamente.")

def marcar_como_completada(listbox_pendientes, listbox_completadas):
    import tkinter.messagebox as messagebox
    
    # Obtiene la tarea seleccionada
    seleccion = listbox_pendientes.curselection()
    if seleccion:
        idx = seleccion[0]
        tarea = tareas[idx]
        
        # Marca la tarea como completada
        tarea['completada'] = True
        
        # Mueve la tarea a la lista de completadas
        listbox_completadas.insert('end', tarea['texto'])
        listbox_pendientes.delete(idx)
        
        # Reordena la lista de tareas (completadas al final)
        tareas.append(tareas.pop(idx))
        
        messagebox.showinfo("Tarea completada", f"Tarea '{tarea['texto']}' marcada como completada.")

def cargar_tareas_desde_archivo(listbox_pendientes, listbox_completadas, listbox_en_proceso=None):
    # Carga las tareas desde un archivo y actualiza la interfaz
    global tareas, tarea_en_proceso
    
    # Intenta cargar las tareas desde el archivo
    nuevas_tareas, nueva_en_proceso = cargar_tareas()
    
    if nuevas_tareas is not None:
        # Actualiza las variables globales
        tareas = nuevas_tareas
        tarea_en_proceso = nueva_en_proceso
        
        # Actualiza la interfaz con las nuevas tareas
        poblar_listbox_desde_tareas(listbox_pendientes, listbox_completadas, listbox_en_proceso)
