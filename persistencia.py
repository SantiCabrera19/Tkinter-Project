# persistencia.py
# Funciones para guardar y cargar tareas en archivo JSON

import json # importamos el modulo json, que nos permite trabajar con archivos json
import os # y os que bueno, para manejar los archivos
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

# Devuelve la ruta al escritorio del usuario
def ruta_escritorio():
    return str(Path.home() / 'Desktop')

# Guarda la lista de tareas y la tarea en proceso en un archivo JSON
# tareas: lista de dicts [{'texto': str, 'completada': bool}]
# en_proceso: texto de la tarea en proceso o None
# ruta_archivo: ruta donde guardar el archivo (si es None, pide al usuario)
def guardar_tareas(tareas, en_proceso=None, ruta_archivo=None):
    data = {
        'tareas': tareas,
        'en_proceso': en_proceso
    }
    if ruta_archivo is None:
        root = tk.Tk()
        root.withdraw()
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('Archivos JSON', '*.json')],
            initialdir=ruta_escritorio(),
            title='Guardar datos de Pomodoro'
        )
        root.destroy()
        if not ruta_archivo:
            return  # Usuario canceló
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Carga la lista de tareas y la tarea en proceso desde un archivo JSON
# Devuelve (tareas, en_proceso)
# ruta_archivo: ruta del archivo a cargar (si es None, pide al usuario)
def cargar_tareas(ruta_archivo=None):
    if ruta_archivo is None:
        root = tk.Tk()
        root.withdraw()
        ruta_archivo = filedialog.askopenfilename(
            defaultextension='.json',
            filetypes=[('Archivos JSON', '*.json')],
            initialdir=ruta_escritorio(),
            title='Cargar datos de Pomodoro'
        )
        root.destroy()
        if not ruta_archivo:
            return [], None  # Usuario canceló
    if not os.path.exists(ruta_archivo):
        return [], None
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
        tareas = data.get('tareas', [])
        en_proceso = data.get('en_proceso', None)
        return tareas, en_proceso 