# -*- coding: utf-8 -*-
"""
Módulo de Gramática - SoftAnalizr
Contiene la lógica para tokenizar producciones, identificar variables y terminales,
y eliminar la recursividad por la izquierda de forma general.
"""

def tokenizar_produccion(prod_str, variables):
    """
    Divide una cadena de producción en una lista de tokens.
    Busca primero coincidencias con las variables conocidas (de mayor a menor longitud)
    y luego trata los caracteres individuales restantes como terminales.
    Ignora espacios en blanco.
    """
    if prod_str == "e":
        return ["e"]
        
    sorted_vars = sorted(list(variables), key=len, reverse=True)
    tokens = []
    i = 0
    n = len(prod_str)
    
    while i < n:
        matched = False
        for var in sorted_vars:
            if prod_str.startswith(var, i):
                tokens.append(var)
                i += len(var)
                matched = True
                break
        if not matched:
            char = prod_str[i]
            if not char.isspace():
                tokens.append(char)
            i += 1
            
    return tokens

def empieza_con_variable(prod_str, var):
    """
    Determina si la cadena de producción empieza con la variable dada,
    evitando falsos positivos (por ejemplo, que 'S' coincida al inicio de 'S!').
    """
    if not prod_str.startswith(var):
        return False
    # Evitar que coincida con un prefijo si el siguiente caracter es un modificador de variable
    if len(prod_str) > len(var) and prod_str[len(var)] == '!':
        return False
    return True

def identificar_simbolos(producciones):
    """
    Identifica las variables y terminales presentes en un diccionario de producciones.
    Retorna (variables, terminales) ordenados para su visualización.
    """
    variables = list(producciones.keys())
    set_variables = set(variables)
    set_terminales = set()
    
    for lhs, alts in producciones.items():
        for alt in alts:
            tokens = tokenizar_produccion(alt, set_variables)
            for tok in tokens:
                if tok not in set_variables:
                    set_terminales.add(tok)
                    
    # Ordenar variables manteniendo el orden de aparición original y luego las nuevas
    # Ordenar terminales alfabéticamente/técnicamente
    terminales_ordenados = sorted(list(set_terminales))
    
    return variables, terminales_ordenados

def eliminar_recursividad_izquierda(producciones_orig):
    """
    Elimina la recursividad por la izquierda (tanto inmediata como indirecta)
    aplicando el algoritmo general de compiladores.
    Retorna un nuevo diccionario de producciones transformado sin recursividad.
    """
    # Hacer una copia profunda del diccionario original para evitar modificarlo
    gramatica = {lhs: list(alts) for lhs, alts in producciones_orig.items()}
    
    # Lista ordenada de las variables originales
    variables_ordenadas = list(gramatica.keys())
    todas_las_variables = set(variables_ordenadas)
    
    resultado = {}
    
    # 1. Aplicar algoritmo general de eliminación de recursividad indirecta
    for i in range(len(variables_ordenadas)):
        Ai = variables_ordenadas[i]
        
        for j in range(i):
            Aj = variables_ordenadas[j]
            # Obtener producciones de Ai actuales
            alts_Ai = gramatica.get(Ai, [])
            nuevas_alts_Ai = []
            
            for alt in alts_Ai:
                if empieza_con_variable(alt, Aj):
                    # Reemplazar Aj por sus producciones correspondientes
                    resto = alt[len(Aj):]
                    for alt_Aj in gramatica.get(Aj, []):
                        if alt_Aj == "e":
                            # Si es épsilon, queda el resto o épsilon si el resto es vacío
                            nuevas_alts_Ai.append(resto if resto else "e")
                        else:
                            nuevas_alts_Ai.append(alt_Aj + resto)
                else:
                    nuevas_alts_Ai.append(alt)
            gramatica[Ai] = nuevas_alts_Ai
            
        # 2. Eliminar la recursividad por la izquierda inmediata para Ai
        alts_Ai = gramatica.get(Ai, [])
        recursivas = []
        no_recursivas = []
        
        for alt in alts_Ai:
            if empieza_con_variable(alt, Ai):
                resto = alt[len(Ai):]
                recursivas.append(resto)
            else:
                no_recursivas.append(alt)
                
        if recursivas:
            # Encontró recursividad inmediata
            Ai_nueva = Ai + "!"
            while Ai_nueva in todas_las_variables:
                Ai_nueva += "!"
                
            todas_las_variables.add(Ai_nueva)
            
            # Si no hay no recursivas, introducimos épsilon para no dejar el no-terminal vacío
            if not no_recursivas:
                no_recursivas = ["e"]
                
            # Reglas para Ai: beta_j Ai!
            nuevas_Ai = []
            for beta in no_recursivas:
                if beta == "e":
                    nuevas_Ai.append(Ai_nueva)
                else:
                    nuevas_Ai.append(beta + Ai_nueva)
            gramatica[Ai] = nuevas_Ai
            
            # Reglas para Ai!: alpha_k Ai! y e
            nuevas_Ai_nueva = []
            for alpha in recursivas:
                if alpha == "":
                    # Evitar bucles infinitos triviales como S -> S
                    continue
                nuevas_Ai_nueva.append(alpha + Ai_nueva)
            nuevas_Ai_nueva.append("e")
            
            # Guardamos las nuevas reglas de la variable extendida
            gramatica[Ai_nueva] = nuevas_Ai_nueva
            
            # Actualizamos también en resultado
            resultado[Ai] = nuevas_Ai
            resultado[Ai_nueva] = nuevas_Ai_nueva
        else:
            resultado[Ai] = alts_Ai

    # Reordenamos el diccionario para que las variables generadas queden adyacentes a sus creadoras
    # Esto facilita la lectura académica
    resultado_ordenado = {}
    for var in variables_ordenadas:
        if var in resultado:
            resultado_ordenado[var] = resultado[var]
        # Añadir las derivadas
        derivada = var + "!"
        while derivada in todas_las_variables:
            if derivada in resultado:
                resultado_ordenado[derivada] = resultado[derivada]
            derivada += "!"
            
    return resultado_ordenado
