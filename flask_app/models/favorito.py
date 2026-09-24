from flask_app.config.mysqlconnection import connectToMySQL


class Favoritos:
    @classmethod
    def existe(cls, data):
        query = """
            SELECT usuario_id, cancion_id
            FROM favoritos
            WHERE usuario_id = %(usuario_id)s
              AND cancion_id = %(cancion_id)s;
        """
        resultado = connectToMySQL("esquema_canciones").query_db(query, data)
        return bool(resultado)

    @classmethod
    def agregar(cls, data):
        query = """
            INSERT INTO favoritos (usuario_id, cancion_id)
            VALUES (%(usuario_id)s, %(cancion_id)s);
        """
        return connectToMySQL("esquema_canciones").query_db(query, data)


    @classmethod
    def toma_todo(cls):
        query = """
            SELECT
                usuarios.id_usuario,
                usuarios.nombre,
                usuarios.email,
                canciones.id_cancion,
                canciones.titulo

            FROM favoritos

            INNER JOIN usuarios
                ON favoritos.usuarios_id =
                    usuarios.id_usuario
            INNER JOIN canciones
                ON favoritos.cancion_id =
                    canciones.id_cancion
            ORDER BY
                usuarios.id_usuario,
                canciones.id_cancion;
        """

        return connectToMySQL(
            "esquema_canciones"
        ).query_db(query)
