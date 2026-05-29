# -*- coding: utf-8 -*-
"""
Módulo de Utilidades - SoftAnalizr
Funciones auxiliares para el procesamiento de texto, validación y formateo.
"""

def formatear_conjunto(conjunto):
    """
    Toma un conjunto o lista de símbolos y lo convierte en una cadena ordenada 
    y formateada por comas (por ejemplo: 'a, b, e').
    Si 'e' (épsilon) está en el conjunto, se suele colocar ordenado o al final.
    """
    if not conjunto:
        return "-"
    
    # Ordenamos los elementos para que sea consistente
    elementos = sorted(list(conjunto))
    
    # Si '$' está presente, lo ponemos al final o al inicio según convención acadámica
    # Generalmente es agradable verlos ordenados alfabéticamente
    return ", ".join(elementos)

def limpiar_linea(linea):
    """
    Limpia espacios en blanco innecesarios de una línea de texto.
    """
    return linea.strip()

def validar_y_cargar_gramatica(texto):
    """
    Analiza la gramática ingresada como texto en un diccionario de producciones.
    Soporta separadores '::' y '->'.
    Retorna una tupla (producciones, start_symbol, error_msg).
    
    Estructura de producciones:
    {
        "S": ["S+a", "T"],
        "T": ["T*F", "F"],
        "F": ["a", "e"]
    }
    """
    producciones = {}
    start_symbol = None
    
    lineas = texto.splitlines()
    for num_linea, linea in enumerate(lineas, 1):
        linea = limpiar_linea(linea)
        if not linea or linea.startswith("#"):
            continue # Ignorar líneas vacías o comentarios
        
        # Detectar el separador
        separador = None
        if "::" in linea:
            separador = "::"
        elif "->" in linea:
            separador = "->"
        
        if not separador:
            return None, None, f"Error en línea {num_linea}: Falta separador '::' o '->'."
        
        partes = linea.split(separador, 1)
        lhs = partes[0].strip()
        rhs_completo = partes[1].strip()
        
        if not lhs:
            return None, None, f"Error en línea {num_linea}: El lado izquierdo (LHS) no puede estar vacío."
        if not rhs_completo:
            return None, None, f"Error en línea {num_linea}: El lado derecho (RHS) de '{lhs}' no puede estar vacío."
        
        # Eliminar todos los espacios internos del LHS y RHS para consistencia sintáctica
        # e.g., "S + a" -> "S+a"
        lhs = "".join(lhs.split())
        
        alternativas = []
        for alt in rhs_completo.split("|"):
            alt_limpia = "".join(alt.split())
            if alt_limpia:
                alternativas.append(alt_limpia)
            else:
                # Si hay una alternativa vacía, la tratamos como 'e' (épsilon)
                alternativas.append("e")
                
        if lhs not in producciones:
            producciones[lhs] = []
            if start_symbol is None:
                start_symbol = lhs
                
        for alt in alternativas:
            if alt not in producciones[lhs]:
                producciones[lhs].append(alt)
                
    if not producciones:
        return None, None, "La gramática ingresada está vacía o no es válida."
        
    return producciones, start_symbol, None
