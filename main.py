# -*- coding: utf-8 -*-
"""
Punto de Entrada - SoftAnalizr
Inicializa y arranca el ciclo principal de la aplicación.
"""

import sys
from interfaz import Aplicacion

def main():
    try:
        app = Aplicacion()
        app.mainloop()
    except Exception as e:
        print(f"Error crítico al iniciar la aplicación: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
