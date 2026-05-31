# SOFTANALYZER

SoftAnalizr es una herramienta académica para el análisis de gramáticas en el contexto de compiladores. Permite ingresar una gramática, eliminar recursividad por la izquierda, identificar variables y terminales, y calcular las funciones **Primera (First)** y **Siguiente (Follow)**.

## Características

- Interfaz gráfica con Tkinter.
- Carga automática de una gramática de demostración.
- Soporte para reglas con separadores `::` o `->`.
- Eliminación de recursividad por la izquierda.
- Cálculo de conjuntos `FIRST` y `FOLLOW`.
- Presentación de resultados en tablas claras.
- Tecla rápida `F5` para ejecutar el análisis.

## Requisitos

- Python 3.10+ (utiliza la biblioteca estándar de Python).

## Estructura del proyecto

- `main.py` - Punto de entrada de la aplicación.
- `interfaz.py` - Construye la interfaz gráfica y controla el flujo de análisis.
- `gramatica.py` - Lógica de manipulación de gramáticas y eliminación de recursividad.
- `primera.py` - Cálculo de la función `FIRST`.
- `siguiente.py` - Cálculo de la función `FOLLOW`.
- `utilidades.py` - Validación de gramáticas y funciones auxiliares.
- `estilos.py` - Estilos visuales y temas de la interfaz.

## Uso

1. Clona el repositorio o descarga el código.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta:

```bash
python main.py
```

4. Ingresa la gramática en el panel izquierdo.
5. Presiona el botón `EJECUTAR (F5)` o la tecla `F5`.
6. Revisa la gramática transformada, los vectores de símbolos y los conjuntos `FIRST` y `FOLLOW`.

## Formato de gramática

- Utiliza `::` o `->` para separar el lado izquierdo del lado derecho.
- Separa alternativas con `|`.
- Ejemplo:

```text
S::S+a|T
T::T*F|F
F::a|e
```

## Ejemplo rápido

Gramática de demostración cargada por defecto:

```text
S::S+a|T
T::T*F|F
F::a|e
```

## Notas

- Las producciones se procesan sin espacios adicionales.
- Si se detecta un error de sintaxis, se muestra un mensaje en la interfaz.

## Autor

Fredy Alexander Ramírez Gómez
