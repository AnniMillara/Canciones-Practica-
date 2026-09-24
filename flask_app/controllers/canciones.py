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
    lista_usuarios = Usuarios.toma_todo()
    return render_template("usuarios.html", usuarios=lista_usuarios)


@app.route("/usuarios/registro", methods=["POST"])
def inscribir():
    nombre = request.form.get("nombre", "").strip()
    email = request.form.get("email", "").strip()
    contrasena = request.form.get("contrasena", "").strip()

    if not nombre or not email or not contrasena:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for("usuarios"))

    data = {
        "nombre": nombre,
        "email": email,
        "contrasena": contrasena
    }
    resultado = Usuarios.salvar(data)
    if resultado is False:
        flash("No fue posible crear el usuario.", "danger")
        return redirect(url_for("usuarios"))

    flash("Usuario creado correctamente.", "success")
    return redirect(url_for("usuarios"))


@app.route("/usuarios/<int:id>")
def mostrar_usuario(id):
    data = {"id_usuario": id}
    usuario = Usuarios.id_con_favoritos(data)

    if usuario is None:
        return ("Usuario no encontrado", 404)

    canciones = Canciones.toma_todo()

    return render_template(
        "mostrar_usuario.html",
        usuario=usuario,
        canciones=canciones
    )


# CANCIONES
@app.route("/canciones")
def canciones():
    lista_canciones = Canciones.toma_todo()
    return render_template("canciones.html", canciones=lista_canciones)


@app.route("/canciones/crear", methods=["POST"])
def crear_cancion():
    titulo = request.form.get("titulo", "").strip()
    artista = request.form.get("artista", "").strip()

    if not titulo or not artista:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for("canciones"))

    data = {"titulo": titulo, "artista": artista}
    resultado = Canciones.salvar(data)

    if resultado is False:
        flash("No fue posible crear la canción.", "danger")
        return redirect(url_for("canciones"))

    flash("Canción guardada correctamente.", "success")
    return redirect(url_for("canciones"))


@app.route("/canciones/<int:id>")
def mostrar_cancion(id):
    data = {"id_cancion": id}
    cancion = Canciones.id_con_usuarios(data)

    if cancion is None:
        return ("Canción no encontrada", 404)

    usuarios = Canciones.usuarios_no_favorito({"cancion_id": id})

    return render_template(
        "mostrar_cancion.html",
        cancion=cancion,
        usuarios=usuarios
    )


@app.route("/favoritos/agregar", methods=["POST"])
def agregar_favorito():
    usuario_id_texto = request.form.get("usuario_id")
    cancion_id_texto = request.form.get("cancion_id")
    origen = request.form.get("origen")

    if not usuario_id_texto or not cancion_id_texto:
        flash("Debes seleccionar los datos necesarios.", "danger")
        return redirect(url_for("usuarios"))

    try:
        usuario_id = int(usuario_id_texto)
        cancion_id = int(cancion_id_texto)
    except ValueError:
        flash("Los identificadores no son válidos.", "danger")
        return redirect(url_for("usuarios"))

    usuario = Usuarios.tomar_por_id(usuario_id)
    if usuario is None:
        flash("El usuario seleccionado no existe.", "danger")
        return redirect(url_for("usuarios"))

    cancion = Canciones.tomar_por_id(cancion_id)
    if cancion is None:
        flash("La canción seleccionada no existe.", "danger")
        return redirect(url_for("canciones"))

    data = {
        "usuario_id": usuario_id,
        "cancion_id": cancion_id
    }

    if Favoritos.existe(data):
        flash("Esta canción ya está entre los favoritos del usuario.", "warning")
    else:
        resultado = Favoritos.agregar(data)
        if resultado is False:
            flash("No fue posible agregar el favorito.", "danger")
        else:
            flash("Favorito agregado correctamente.", "success")

    if origen == "usuario":
        return redirect(url_for("mostrar_usuario", id=usuario_id))
    if origen == "cancion":
        return redirect(url_for("mostrar_cancion", id=cancion_id))
    return redirect(url_for("usuarios"))