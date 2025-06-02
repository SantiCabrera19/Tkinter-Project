# tareas.py
# Funciones y estructura de datos para la gestión de tareas

tareas = []  # Lista para almacenar las tareas 

# Función para agregar una tarea a la lista
def agregar_tarea(texto, lista_tareas_widget, entry_widget):
    if texto:
        lista_tareas_widget.insert('end', texto)
        entry_widget.delete(0, 'end')
        tareas.append({'texto': texto, 'completada': False})

# Función para eliminar la tarea seleccionada en la lista
def eliminar_tarea(lista_tareas_widget):
    seleccion = lista_tareas_widget.curselection()
    if seleccion: # Si hay una tarea seleccionada
        idx = seleccion[0] # Índice de la tarea seleccionada
        lista_tareas_widget.delete(idx) # Elimina la tarea seleccionada
        del tareas[idx] # Elimina la tarea de la lista

# Función para marcar una tarea como completada
def marcar_como_completada(listbox_pendientes, listbox_completadas):
    seleccion = listbox_pendientes.curselection() # Trabajara con la seleccion de la lista pendientes
    if seleccion: # Si hay una tarea seleccionada
        idx = seleccion[0] # Índice de la tarea seleccionada
        tarea = tareas[idx] # Tarea seleccionada
        tarea['completada'] = True # Marcar la tarea como completada, anteriormente, en la lista de tareas, era False siempre
        # Mover visualmente
        listbox_completadas.insert('end', tarea['texto']) # Insertar la tarea en la lista de completadas
        listbox_pendientes.delete(idx) # Eliminar la tarea de la lista de pendientes
        # Mover en la estructura de datos
        tareas.append(tareas.pop(idx)) # Mover la tarea a la lista de completadas
