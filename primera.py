# -*- coding: utf-8 -*-
"""
Módulo Primera - SoftAnalizr
Calcula la función Primera (First) para todas las variables de la gramática.
"""

from gramatica import tokenizar_produccion

def calcular_primeros(producciones, variables, terminales):
    """
    Calcula los conjuntos de Primera para todas las variables mediante
    el algoritmo clásico de punto fijo en compiladores.
    
    Retorna un diccionario { variable: set(terminales) }
    donde 'e' denota épsilon.
    """
    # Inicializar los conjuntos Primera como vacíos para cada variable
    primeros = {var: set() for var in variables}
    set_variables = set(variables)
    set_terminales = set(terminales)
    
    cambio = True
    while cambio:
        cambio = False
        
        for var in variables:
            alts = producciones.get(var, [])
            for alt in alts:
                # Tokenizar la alternativa de producción
                tokens = tokenizar_produccion(alt, set_variables)
                
                # Caso vacío o épsilon directo
                if not tokens or tokens == ["e"]:
                    if "e" not in primeros[var]:
                        primeros[var].add("e")
                        cambio = True
                    continue
                
                # Analizar secuencia de tokens X1 X2 ... Xk
                todos_derivan_epsilon = True
                for token in tokens:
                    if token in set_terminales:
                        # Si es un terminal (distinto de 'e'), lo agregamos y rompemos
                        if token == "e":
                            # Épsilon en medio se salta pero sigue derivando épsilon
                            continue
                        if token not in primeros[var]:
                            primeros[var].add(token)
                            cambio = True
                        todos_derivan_epsilon = False
                        break
                        
                    elif token in set_variables:
                        # Si es una variable, agregamos First(token) - {e}
                        primeros_token = primeros[token]
                        solo_terminales = primeros_token - {"e"}
                        
                        tamanio_previo = len(primeros[var])
                        primeros[var].update(solo_terminales)
                        if len(primeros[var]) > tamanio_previo:
                            cambio = True
                            
                        # Si 'e' no está en First(token), no podemos avanzar más
                        if "e" not in primeros_token:
                            todos_derivan_epsilon = False
                            break
                    else:
                        # Tratamiento por defecto para cualquier otro símbolo
                        if token not in primeros[var]:
                            primeros[var].add(token)
                            cambio = True
                        todos_derivan_epsilon = False
                        break
                
                # Si toda la cadena de la producción puede derivar épsilon,
                # entonces la variable principal puede derivar épsilon.
                if todos_derivan_epsilon:
                    if "e" not in primeros[var]:
                        primeros[var].add("e")
                        cambio = True
                        
    return primeros
