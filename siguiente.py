# -*- coding: utf-8 -*-
"""
Módulo Siguiente - SoftAnalizr
Calcula la función Siguiente (Follow) para todas las variables de la gramática.
"""

from gramatica import tokenizar_produccion

def calcular_siguientes(producciones, variables, terminales, primeros, start_symbol):
    """
    Calcula los conjuntos de Siguiente para todas las variables mediante
    el algoritmo clásico de punto fijo en compiladores.
    
    Retorna un diccionario { variable: set(terminales) }
    donde '$' denota el fin de la cadena de entrada.
    """
    # Inicializar los conjuntos Siguiente como vacíos para cada variable
    siguientes = {var: set() for var in variables}
    
    # El símbolo inicial siempre contiene el fin de archivo '$'
    if start_symbol and start_symbol in siguientes:
        siguientes[start_symbol].add("$")
        
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
                
                # Recorrer cada token para encontrar variables y actualizar sus Siguiente
                for i in range(len(tokens)):
                    B = tokens[i]
                    if B in set_variables:
                        # Encontramos la variable B en la producción: var -> alfa B beta
                        beta = tokens[i+1:]
                        
                        if beta:
                            # Calcular First(beta)
                            first_beta = set()
                            beta_deriva_epsilon = True
                            
                            for token in beta:
                                if token in set_terminales:
                                    if token == "e":
                                        continue
                                    first_beta.add(token)
                                    beta_deriva_epsilon = False
                                    break
                                elif token in set_variables:
                                    first_token = primeros[token]
                                    first_beta.update(first_token - {"e"})
                                    if "e" not in first_token:
                                        beta_deriva_epsilon = False
                                        break
                                else:
                                    first_beta.add(token)
                                    beta_deriva_epsilon = False
                                    break
                            
                            # Regla: Todo en First(beta) (excepto épsilon) va a Follow(B)
                            tamanio_previo = len(siguientes[B])
                            siguientes[B].update(first_beta)
                            if len(siguientes[B]) > tamanio_previo:
                                cambio = True
                                
                            # Regla: Si beta puede derivar épsilon, entonces Follow(var) va a Follow(B)
                            if beta_deriva_epsilon:
                                tamanio_previo = len(siguientes[B])
                                siguientes[B].update(siguientes[var])
                                if len(siguientes[B]) > tamanio_previo:
                                    cambio = True
                        else:
                            # Regla: Si B es el último símbolo (var -> alfa B),
                            # entonces todo en Follow(var) va a Follow(B)
                            tamanio_previo = len(siguientes[B])
                            siguientes[B].update(siguientes[var])
                            if len(siguientes[B]) > tamanio_previo:
                                cambio = True
                                
    return siguientes
