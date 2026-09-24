from flask_app.config.mysqlconnection import connectToMySQL


class Canciones:
    def __init__(self, data):
        self.id_cancion = data["id_cancion"]
        self.titulo = data["titulo"]
        self.artista = data["artista"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.usuarios = []

    @classmethod
    def toma_todo(cls):
        query = """
            SELECT
                id_cancion,
                titulo,
                artista,
                created_at,
                updated_at
            FROM canciones
            ORDER BY id_cancion;
        """
        resultados = connectToMySQL("esquema_canciones").query_db(query)
        canciones = []
        for cancion in resultados or []:
            canciones.append(cls(cancion))
        return canciones

    @classmethod
    def tomar_por_id(cls, id_cancion):
        query = """
            SELECT
                id_cancion,
                titulo,
                artista,
                created_at,
                updated_at
            FROM canciones
            WHERE id_cancion = %(id_cancion)s;
        """
        data = {"id_cancion": id_cancion}
        resultados = connectToMySQL("esquema_canciones").query_db(query, data)
        if resultados:
            return cls(resultados[0])
        return None

    @classmethod
    def salvar(cls, data):
        query = """
            INSERT INTO canciones (titulo, artista)
            VALUES (%(titulo)s, %(artista)s);
        """
        return connectToMySQL("esquema_canciones").query_db(query, data)

    @classmethod
    def id_con_usuarios(cls, data):
        query = """
            SELECT
                canciones.id_cancion AS cancion_id,
                canciones.titulo AS cancion_titulo,
                canciones.artista AS cancion_artista,
                canciones.created_at AS cancion_created_at,
                canciones.updated_at AS cancion_updated_at,

                usuarios.id_usuario AS usuario_id,
                usuarios.nombre AS usuario_nombre,
                usuarios.email AS usuario_email,
                usuarios.contrasena AS usuario_contrasena,
                usuarios.created_at AS usuario_created_at,
                usuarios.updated_at AS usuario_updated_at

            FROM canciones
            LEFT JOIN favoritos
                ON favoritos.cancion_id = canciones.id_cancion
            LEFT JOIN usuarios
                ON favoritos.usuario_id = usuarios.id_usuario
            WHERE canciones.id_cancion = %(id_cancion)s;
        """
        resultados = connectToMySQL("esquema_canciones").query_db(query, data)

        if not resultados:
            return None

        cancion_data = {
            "id_cancion": resultados[0]["cancion_id"],
            "titulo": resultados[0]["cancion_titulo"],
            "artista": resultados[0]["cancion_artista"],
            "created_at": resultados[0]["cancion_created_at"],
            "updated_at": resultados[0]["cancion_updated_at"]
        }
        cancion = cls(cancion_data)

        for fila in resultados:
            if fila["usuario_id"] is not None:
                cancion.usuarios.append({
                    "id_usuario": fila["usuario_id"],
                    "nombre": fila["usuario_nombre"],
                    "email": fila["usuario_email"],
                    "contrasena": fila["usuario_contrasena"],
                    "created_at": fila["usuario_created_at"],
                    "updated_at": fila["usuario_updated_at"]
                })
        return cancion

    @classmethod
    def usuarios_no_favorito(cls, data):
        query = """
            SELECT
                usuarios.id_usuario,
                usuarios.nombre,
                usuarios.email,
                usuarios.contrasena,
                usuarios.created_at,
                usuarios.updated_at
            FROM usuarios
            LEFT JOIN favoritos
                ON favoritos.usuario_id = usuarios.id_usuario
                AND favoritos.cancion_id = %(cancion_id)s
            WHERE favoritos.usuario_id IS NULL
            ORDER BY usuarios.nombre;
        """
        return connectToMySQL("esquema_canciones").query_db(query, data)