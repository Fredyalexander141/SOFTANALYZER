# -*- coding: utf-8 -*-
"""
Módulo de Interfaz - SoftAnalizr
Construye la interfaz de usuario con Tkinter/ttk, gestiona los eventos de teclado (F5),
e integra la lógica de procesamiento y algoritmos de compiladores.
"""

import time
import tkinter as tk
from tkinter import ttk, messagebox

# Importar constantes y configuraciones del proyecto
import estilos
from utilidades import validar_y_cargar_gramatica, formatear_conjunto
from gramatica import (
    eliminar_recursividad_izquierda,
    identificar_simbolos,
    tokenizar_produccion
)
from primera import calcular_primeros
from siguiente import calcular_siguientes

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurar la ventana principal
        self.title("SoftAnalizr - Sistema de Análisis de Gramáticas")
        self.geometry("1150x680")
        self.minsize(1000, 600)
        
        # Aplicar el tema monocromático minimalista
        estilos.aplicar_tema(self)
        
        # Crear la estructura de la interfaz
        self.crear_componentes()
        
        # Enlazar la tecla F5 para ejecutar el análisis
        self.bind("<F5>", lambda event: self.ejecutar_analisis())
        
        # Cargar gramática de demostración por defecto
        self.cargar_demo()

    def crear_componentes(self):
        """
        Crea los contenedores y controles de la ventana principal.
        """
        # --- 1. CABECERA ---
        header_frame = ttk.Frame(self, style="TFrame")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        lbl_titulo = ttk.Label(
            header_frame, 
            text="SOFTANALYZER", 
            foreground=estilos.FG_TITULO, 
            font=("Consolas", 15, "bold")
        )
        lbl_titulo.pack(anchor="w")
        
        lbl_subtitulo = ttk.Label(
            header_frame, 
            text="FREDY ALEXANDER RAMÍREZ GÓMEZ 5190-23-15803", 
            foreground=estilos.FG_MUTED, 
            font=("Consolas", 9)
        )
        lbl_subtitulo.pack(anchor="w", pady=(2, 0))
        
        # Separador superior
        sep = ttk.Separator(self, orient="horizontal")
        sep.pack(fill="x", padx=20, pady=(0, 10))

        # --- 2. CONTENEDOR PRINCIPAL ---
        main_container = ttk.Frame(self, style="TFrame")
        main_container.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Grid para el contenedor principal
        # Fila 0: Panel Superior (Entrada y Resultados de Gramática sin Rec)
        # Fila 1: Panel Inferior (Tablas de símbolos, producciones, primera, siguiente)
        main_container.rowconfigure(0, weight=4) # Editor de gramática
        main_container.rowconfigure(1, weight=5) # Tablas de resultados
        main_container.columnconfigure(0, weight=1)

        # --- PANEL SUPERIOR: ENTRADA Y SALIDA DE GRAMÁTICA ---
        top_frame = ttk.Frame(main_container, style="TFrame")
        top_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 15))
        top_frame.columnconfigure(0, weight=1) # Entrada
        top_frame.columnconfigure(1, weight=1) # Salida sin recursividad
        top_frame.rowconfigure(0, weight=1)

        # A. Editor de Texto (Izquierda)
        frame_input = ttk.Frame(top_frame, style="Card.TFrame")
        frame_input.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Título del panel de entrada
        lbl_title_in = ttk.Label(frame_input, text="[ ENTRADA DE GRAMÁTICA ]", style="CardTitle.TLabel")
        lbl_title_in.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Instrucción rápida
        lbl_desc_in = ttk.Label(
            frame_input, 
            text="Defina sus reglas usando '::' o '->' y separe alternativas con '|'", 
            style="CardMuted.TLabel"
        )
        lbl_desc_in.pack(anchor="w", padx=15, pady=(0, 8))

        # Área de edición de texto
        text_container = ttk.Frame(frame_input, style="TFrame")
        text_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        self.txt_entrada = tk.Text(
            text_container,
            wrap="none",
            bg=estilos.BG_ENTRADA,
            fg=estilos.FG_TEXTO,
            insertbackground=estilos.FG_TITULO,
            selectbackground=estilos.COLOR_RESALTADO_1,
            selectforeground=estilos.FG_TITULO,
            font=estilos.FUENTE_TEXTO,
            relief="flat",
            padx=10,
            pady=8,
            undo=True
        )
        self.txt_entrada.pack(side="left", fill="both", expand=True)
        
        scroll_txt_in = ttk.Scrollbar(text_container, orient="vertical", command=self.txt_entrada.yview)
        scroll_txt_in.pack(side="right", fill="y")
        self.txt_entrada.config(yscrollcommand=scroll_txt_in.set)

        # B. Gramática sin Recursividad (Derecha)
        frame_output = ttk.Frame(top_frame, style="Card.TFrame")
        frame_output.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Título del panel de salida
        lbl_title_out = ttk.Label(frame_output, text="[ GRAMÁTICA SIN RECURSIVIDAD POR LA IZQUIERDA ]", style="CardTitle.TLabel")
        lbl_title_out.pack(anchor="w", padx=15, pady=(10, 5))
        
        lbl_desc_out = ttk.Label(
            frame_output, 
            text="Gramática transformada resultante de la eliminación de recursividad", 
            style="CardMuted.TLabel"
        )
        lbl_desc_out.pack(anchor="w", padx=15, pady=(0, 8))

        # Área de texto de salida (no editable)
        text_out_container = ttk.Frame(frame_output, style="TFrame")
        text_out_container.pack(fill="both", expand=True, padx=15, pady=(0, 10))
        
        self.txt_salida = tk.Text(
            text_out_container,
            wrap="none",
            bg=estilos.BG_ENTRADA,
            fg=estilos.FG_TEXTO,
            insertbackground=estilos.FG_TITULO,
            font=estilos.FUENTE_TEXTO,
            relief="flat",
            padx=10,
            pady=8,
            state="disabled"
        )
        self.txt_salida.pack(side="left", fill="both", expand=True)
        
        scroll_txt_out = ttk.Scrollbar(text_out_container, orient="vertical", command=self.txt_salida.yview)
        scroll_txt_out.pack(side="right", fill="y")
        self.txt_salida.config(yscrollcommand=scroll_txt_out.set)

        # Botón Ejecutar
        controls_frame = ttk.Frame(frame_input, style="TFrame")
        controls_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        self.btn_ejecutar = ttk.Button(
            controls_frame, 
            text="EJECUTAR (F5)", 
            command=self.ejecutar_analisis
        )
        self.btn_ejecutar.pack(side="left")
        
        self.lbl_tecla_hint = ttk.Label(
            controls_frame, 
            text="Presione F5 en cualquier momento para procesar", 
            foreground=estilos.FG_MUTED, 
            font=("Consolas", 8)
        )
        self.lbl_tecla_hint.pack(side="left", padx=15)

        # --- PANEL INFERIOR: CUATRO TABLAS ALINEADAS HORIZONTALMENTE ---
        bottom_frame = ttk.Frame(main_container, style="TFrame")
        bottom_frame.grid(row=1, column=0, sticky="nsew")
        
        # 4 columnas iguales para las 4 tablas
        for col_idx in range(4):
            bottom_frame.columnconfigure(col_idx, weight=1, minsize=200)
        bottom_frame.rowconfigure(0, weight=1)

        # 1. Tabla: Vectores de Variables y Terminales
        frame_t1 = ttk.Frame(bottom_frame, style="Card.TFrame")
        frame_t1.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        lbl_t1 = ttk.Label(frame_t1, text="[ VECTORES V Y T ]", style="CardTitle.TLabel")
        lbl_t1.pack(anchor="w", padx=10, pady=(8, 4))
        
        self.tree_simbolos = ttk.Treeview(
            frame_t1, 
            columns=("var", "term"), 
            show="headings", 
            selectmode="browse"
        )
        self.tree_simbolos.heading("var", text="Variables (V)")
        self.tree_simbolos.heading("term", text="Terminales (T)")
        self.tree_simbolos.column("var", anchor="center", width=90)
        self.tree_simbolos.column("term", anchor="center", width=90)
        self.tree_simbolos.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # 2. Tabla: Matriz de Producciones
        frame_t2 = ttk.Frame(bottom_frame, style="Card.TFrame")
        frame_t2.grid(row=0, column=1, sticky="nsew", padx=(5, 5))
        
        lbl_t2 = ttk.Label(frame_t2, text="[ MATRIZ PRODUCCIONES ]", style="CardTitle.TLabel")
        lbl_t2.pack(anchor="w", padx=10, pady=(8, 4))
        
        self.tree_producciones = ttk.Treeview(
            frame_t2, 
            columns=("var", "prod"), 
            show="headings", 
            selectmode="browse"
        )
        self.tree_producciones.heading("var", text="Variable")
        self.tree_producciones.heading("prod", text="Producción")
        self.tree_producciones.column("var", anchor="center", width=80)
        self.tree_producciones.column("prod", anchor="w", width=120)
        self.tree_producciones.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # 3. Tabla: Función Primera
        frame_t3 = ttk.Frame(bottom_frame, style="Card.TFrame")
        frame_t3.grid(row=0, column=2, sticky="nsew", padx=(5, 5))
        
        lbl_t3 = ttk.Label(frame_t3, text="[ FUNCIÓN PRIMERA ]", style="CardTitle.TLabel")
        lbl_t3.pack(anchor="w", padx=10, pady=(8, 4))
        
        self.tree_primera = ttk.Treeview(
            frame_t3, 
            columns=("var", "prim"), 
            show="headings", 
            selectmode="browse"
        )
        self.tree_primera.heading("var", text="Variable")
        self.tree_primera.heading("prim", text="Primera (First)")
        self.tree_primera.column("var", anchor="center", width=80)
        self.tree_primera.column("prim", anchor="w", width=120)
        self.tree_primera.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # 4. Tabla: Función Siguiente
        frame_t4 = ttk.Frame(bottom_frame, style="Card.TFrame")
        frame_t4.grid(row=0, column=3, sticky="nsew", padx=(5, 0))
        
        lbl_t4 = ttk.Label(frame_t4, text="[ FUNCIÓN SIGUIENTE ]", style="CardTitle.TLabel")
        lbl_t4.pack(anchor="w", padx=10, pady=(8, 4))
        
        self.tree_siguiente = ttk.Treeview(
            frame_t4, 
            columns=("var", "sig"), 
            show="headings", 
            selectmode="browse"
        )
        self.tree_siguiente.heading("var", text="Variable")
        self.tree_siguiente.heading("sig", text="Siguiente (Follow)")
        self.tree_siguiente.column("var", anchor="center", width=80)
        self.tree_siguiente.column("sig", anchor="w", width=120)
        self.tree_siguiente.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # --- 3. BARRA DE ESTADO ---
        self.status_bar = ttk.Frame(self, style="TFrame")
        self.status_bar.pack(fill="x", side="bottom", padx=20, pady=(5, 10))
        
        self.lbl_estado = ttk.Label(
            self.status_bar, 
            text="Listo. Ingrese una gramática y presione F5 o Ejecutar para iniciar el análisis.", 
            foreground=estilos.FG_MUTED, 
            font=("Consolas", 8)
        )
        self.lbl_estado.pack(side="left")

    def cargar_demo(self):
        """
        Carga la gramática académica estándar en el editor de texto al iniciar.
        """
        gramatica_demo = "S::S+a|T\nT::T*F|F\nF::a|e\n"
        self.txt_entrada.delete("1.0", tk.END)
        self.txt_entrada.insert("1.0", gramatica_demo)

    def mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error en la barra de estado y en un messagebox.
        """
        self.lbl_estado.config(text=f"ERROR: {mensaje}", foreground="#cc0000")
        messagebox.showerror("Error de Análisis", mensaje)

    def ejecutar_analisis(self):
        """
        Flujo de control principal. Lee la gramática, realiza las transformaciones,
        ejecuta los cálculos y actualiza toda la interfaz gráfica.
        """
        # Registrar tiempo de inicio para medir desempeño
        t_inicio = time.time()
        
        # 1. Leer gramática ingresada
        texto_gramatica = self.txt_entrada.get("1.0", tk.END)
        
        # 2. Validar y procesar sintaxis inicial
        producciones, start_symbol, error = validar_y_cargar_gramatica(texto_gramatica)
        if error:
            self.mostrar_error(error)
            return
            
        try:
            # 3. Eliminar recursividad por la izquierda
            prod_sin_rec = eliminar_recursividad_izquierda(producciones)
            
            # 4. Identificar variables y terminales del sistema transformado
            variables, terminales = identificar_simbolos(prod_sin_rec)
            
            # 5. Calcular la función Primera (First)
            primeros = calcular_primeros(prod_sin_rec, variables, terminales)
            
            # 6. Calcular la función Siguiente (Follow)
            siguientes = calcular_siguientes(prod_sin_rec, variables, terminales, primeros, start_symbol)
            
            # 7. Actualizar la interfaz
            self.actualizar_interfaz_resultados(
                prod_sin_rec, 
                variables, 
                terminales, 
                primeros, 
                siguientes,
                t_inicio
            )
            
        except Exception as ex:
            self.mostrar_error(f"Error inesperado durante el procesamiento: {str(ex)}")

    def actualizar_interfaz_resultados(self, prod_sin_rec, variables, terminales, primeros, siguientes, t_inicio):
        """
        Vuelca todos los resultados computados en las tablas y áreas de texto del GUI.
        """
        # A. Actualizar panel de texto de Gramática transformada
        self.txt_salida.config(state="normal")
        self.txt_salida.delete("1.0", tk.END)
        
        for lhs, alts in prod_sin_rec.items():
            regla = f"{lhs}::{'|'.join(alts)}\n"
            self.txt_salida.insert(tk.END, regla)
            
        self.txt_salida.config(state="disabled")
        
        # B. Limpiar tablas inferiores
        self.tree_simbolos.delete(*self.tree_simbolos.get_children())
        self.tree_producciones.delete(*self.tree_producciones.get_children())
        self.tree_primera.delete(*self.tree_primera.get_children())
        self.tree_siguiente.delete(*self.tree_siguiente.get_children())
        
        # C. Llenar Tabla 1: Vectores V y T (lado a lado)
        max_len = max(len(variables), len(terminales))
        for i in range(max_len):
            var_val = variables[i] if i < len(variables) else ""
            term_val = terminales[i] if i < len(terminales) else ""
            self.tree_simbolos.insert("", tk.END, values=(var_val, term_val))
            
        # D. Llenar Tabla 2: Matriz de Producciones
        # Formato: cada renglón es una sola alternativa (Variable | Producción)
        for lhs, alts in prod_sin_rec.items():
            for alt in alts:
                self.tree_producciones.insert("", tk.END, values=(lhs, alt))
                
        # E. Llenar Tabla 3: Función Primera
        for var in variables:
            prim_str = formatear_conjunto(primeros.get(var, set()))
            self.tree_primera.insert("", tk.END, values=(var, prim_str))
            
        # F. Llenar Tabla 4: Función Siguiente
        for var in variables:
            sig_str = formatear_conjunto(siguientes.get(var, set()))
            self.tree_siguiente.insert("", tk.END, values=(var, sig_str))
            
        # G. Actualizar barra de estado con estadísticas de rendimiento
        t_total_ms = (time.time() - t_inicio) * 1000
        self.lbl_estado.config(
            text=f"Análisis completado con éxito en {t_total_ms:.2f} ms. Tecla F5 enlazada.", 
            foreground=estilos.FG_MUTED
        )
