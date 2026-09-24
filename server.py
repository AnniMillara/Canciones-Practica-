# PUNTO DE ENTRADA DE LA APLICACIÓN
from flask_app import app

# ==========================================================
# IMPORTAR CONTROLADORES
# ==========================================================
# Aunque no utilizamos directamente la variable "tacos",
# esta importación ejecuta el módulo y registra sus rutas
# utilizando la instancia "app".
# ==========================================================

from flask_app.controllers import canciones

# EJECUTAR SERVIDOR
if __name__ == "__main__":
    app.run(debug=True)
