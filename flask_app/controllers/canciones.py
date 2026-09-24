from flask_app import app
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from flask_app.models.cancion import Canciones
from flask_app.models.favorito import Favoritos
from flask_app.models.usuario import Usuarios

# USUARIOS
@app.route("/")
def index():
    return redirect(url_for("usuarios"))

@app.route("/usuarios")
def usuarios():
    list_usuarios = Usuarios.tomar_todo()

# CREAR INSCRIPCIÓN
@app.route("/registro",methods=["POST"])
def inscribir():
    """
    Recibe estudiante_id y curso_id y crea
    una relación en la tabla inscripciones.
    """

    usuario_id_texto = request.form.get(
        "usuario_id"
    )
    cancion_id_texto = request.form.get(
        "cancion_id"
    )

    # Comprobar que ambos valores fueron enviados.
    if not usuario_id_texto or not cancion_id_texto:
        flash(
            "Por favor seleccionar usuarios y canción favorita.",
            "danger"
        )
        return redirect(
            url_for("index")
        )

    # Convertir IDs a enteros.
    try:
        usuario_id = int(
            usuario_id_texto
        )
        cancion_id = int(
            cancion_id_texto
        )
    except ValueError:
        flash(
            "Los identificadores no son válidos.",
            "danger"
        )
        return redirect(
            url_for("index")
        )

    # Comprobar que el estudiante exista.
    usuario = Usuarios.tomar_por_id(
        usuario_id
    )
    if usuario is None:
        flash(
            "El usuario seleccionado no existe.",
            "danger"
        )
        return redirect(
            url_for("index")
        )

    # Comprobar que el curso exista.
    cancion = Canciones.tomar_por_id(
        cancion_id
    )
    if cancion is None:
        flash(
            "La cancion seleccionado no existe.",
            "danger"
        )

        return redirect(
            url_for("index")
        )

    # Crear diccionario para la relación.
    data = {
        "usuario_id": usuario_id,
        "cancion_id": cancion_id
    }

    # Evitar una inscripción duplicada.
    if Favoritos.existe(data):
        flash(
            "El usuario ya marco esta canción como favorita.",
            "warning"
        )
        return redirect(
            url_for("index")
        )

    # Insertar relación.
    resultado = Favoritos.usuario_favoritos(data)
    if resultado is False:
        flash(
            "No fue posible crear la unión.",
            "danger"
        )
        return redirect(
            url_for("index")
        )

    # Inscripción exitosa.
    flash(
        "Unión realizada correctamente.",
        "success"
    )
    return redirect(
        url_for("index")
    )
