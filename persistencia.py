# persistencia.py
# Funciones para guardar y cargar tareas en archivo JSON

import json  # Para manejar archivos JSON
import os  # Para operaciones con archivos y rutas
from pathlib import Path  # Para manejar rutas de manera segura
import tkinter as tk
from tkinter import filedialog  # Para diálogos de selección de archivos

def ruta_escritorio():
    # Devuelve la ruta al escritorio del usuario actual
    return str(Path.home() / 'Desktop')

def guardar_tareas(tareas, en_proceso=None, ruta_archivo=None):
    """
    Guarda la lista de tareas y la tarea en proceso en un archivo JSON.
    
    Args:
        tareas: Lista de diccionarios con formato [{'texto': str, 'completada': bool}]
        en_proceso: Texto de la tarea en proceso o None
        ruta_archivo: Ruta donde guardar el archivo (si es None, pide al usuario)
    """
    # Preparamos los datos para guardar
    data = {
        'tareas': tareas,
        'en_proceso': en_proceso
    }
    
    # Si no se especificó ruta, mostramos diálogo para elegir
    if ruta_archivo is None:
        root = tk.Tk()
        root.withdraw()  # Ocultamos la ventana temporal
        ruta_archivo = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('Archivos JSON', '*.json')],
            initialdir=ruta_escritorio(),
            title='Guardar datos de Pomodoro'
        )
        root.destroy()
        if not ruta_archivo:
            return  # Usuario canceló
    
    # Guardamos los datos en el archivo JSON
    with open(ruta_archivo, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cargar_tareas(ruta_archivo=None):
    """
    Carga la lista de tareas y la tarea en proceso desde un archivo JSON.
    
    Args:
        ruta_archivo: Ruta del archivo a cargar (si es None, pide al usuario)
    
    Returns:
        tuple: (tareas, en_proceso) donde tareas es la lista de tareas y en_proceso es la tarea en proceso
    """
    # Si no se especificó ruta, mostramos diálogo para elegir
    if ruta_archivo is None:
        root = tk.Tk()
        root.withdraw()  # Ocultamos la ventana temporal
        ruta_archivo = filedialog.askopenfilename(
            defaultextension='.json',
            filetypes=[('Archivos JSON', '*.json')],
            initialdir=ruta_escritorio(),
            title='Cargar datos de Pomodoro'
        )
        root.destroy()
        if not ruta_archivo:
            return [], None  # Usuario canceló
    
    # Verificamos que el archivo exista
    if not os.path.exists(ruta_archivo):
        return [], None
    
    # Cargamos los datos del archivo JSON
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Extraemos las tareas y la tarea en proceso, con valores por defecto
        tareas = data.get('tareas', [])
        en_proceso = data.get('en_proceso', None)
        return tareas, en_proceso 