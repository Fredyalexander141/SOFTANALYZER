# -*- coding: utf-8 -*-
"""
Módulo de Estilos - SoftAnalizr
Define la paleta de colores académica en escala de grises y configura el tema ttk.
"""

import tkinter as tk
from tkinter import ttk

# Paleta de colores técnica (Escala de Grises - Tema Claro)
BG_PRINCIPAL = "#f5f5f5"      # Fondo de la ventana principal (Gris muy claro)
BG_CONTENEDOR = "#ffffff"     # Fondo de los paneles y secciones (Blanco puro)
BG_ENTRADA = "#ffffff"        # Fondo para áreas de texto e inputs (Blanco)
FG_TEXTO = "#1c1c1c"          # Texto principal (Negro suave/Gris muy oscuro)
FG_TITULO = "#000000"         # Títulos y encabezados (Negro puro)
FG_MUTED = "#666666"          # Texto secundario o etiquetas de ayuda (Gris oscuro)
COLOR_BORDES = "#cccccc"       # Bordes finos y delimitadores
COLOR_RESALTADO_1 = "#e5e5e5" # Resaltado primario (Gris claro para encabezados y botones)
COLOR_RESALTADO_2 = "#cccccc" # Resaltado secundario (Gris medio para hover y focus)

# Tipografías técnicas (ideales para compiladores)
FUENTE_TITULO = ("Consolas", 11, "bold")
FUENTE_TEXTO = ("Consolas", 10)
FUENTE_TABLA_HEAD = ("Consolas", 9, "bold")
FUENTE_TABLA_CELL = ("Consolas", 9)

def aplicar_tema(root):
    """
    Configura el aspecto visual de la aplicación Tkinter utilizando estilos ttk.
    """
    # Configurar fondo de la ventana principal
    root.configure(bg=BG_PRINCIPAL)
    
    style = ttk.Style()
    style.theme_use("clam")
    
    # 1. Configuración de Frames
    style.configure(
        "TFrame",
        background=BG_PRINCIPAL
    )
    style.configure(
        "Card.TFrame",
        background=BG_CONTENEDOR,
        borderwidth=1,
        relief="solid"
    )
    
    # 2. Configuración de Etiquetas (Labels)
    style.configure(
        "TLabel",
        background=BG_PRINCIPAL,
        foreground=FG_TEXTO,
        font=FUENTE_TEXTO
    )
    style.configure(
        "CardTitle.TLabel",
        background=BG_CONTENEDOR,
        foreground=FG_TITULO,
        font=FUENTE_TITULO
    )
    style.configure(
        "CardMuted.TLabel",
        background=BG_CONTENEDOR,
        foreground=FG_MUTED,
        font=FUENTE_TEXTO
    )
    
    # 3. Botones (Buttons)
    style.configure(
        "TButton",
        background=COLOR_RESALTADO_1,
        foreground=FG_TITULO,
        bordercolor=COLOR_BORDES,
        lightcolor=COLOR_BORDES,
        darkcolor=COLOR_BORDES,
        font=FUENTE_TITULO,
        padding=(10, 5),
        relief="flat"
    )
    # Estados de hover y active para botones
    style.map(
        "TButton",
        background=[("active", COLOR_RESALTADO_2), ("pressed", COLOR_RESALTADO_1)],
        foreground=[("active", FG_TITULO)]
    )
    
    # 4. Tablas (Treeview)
    style.configure(
        "Treeview",
        background=BG_ENTRADA,
        fieldbackground=BG_ENTRADA,
        foreground=FG_TEXTO,
        rowheight=22,
        font=FUENTE_TABLA_CELL,
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        background=COLOR_RESALTADO_1,
        foreground=FG_TITULO,
        font=FUENTE_TABLA_HEAD,
        borderwidth=1,
        relief="flat"
    )
    style.map(
        "Treeview.Heading",
        background=[("active", COLOR_RESALTADO_2)],
        foreground=[("active", FG_TITULO)]
    )
    # Estilo de selección de renglón
    style.map(
        "Treeview",
        background=[("selected", COLOR_RESALTADO_2)],
        foreground=[("selected", FG_TITULO)]
    )
    
    # 5. Scrollbars
    style.configure(
        "Vertical.TScrollbar",
        gripcount=0,
        background=COLOR_RESALTADO_1,
        troughcolor=BG_PRINCIPAL,
        bordercolor=BG_PRINCIPAL,
        lightcolor=BG_PRINCIPAL,
        darkcolor=BG_PRINCIPAL,
        arrowsize=12
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", COLOR_RESALTADO_2)]
    )
    
    # 6. Separadores
    style.configure(
        "TSeparator",
        background=COLOR_BORDES
    )
