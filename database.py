import sqlite3
from datetime import datetime

from config import DB_PATH


def conectar():
    return sqlite3.connect(DB_PATH)


def obtener_estado():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT variable, valor, actualizado FROM estado")
    datos = cursor.fetchall()
    conn.close()
    return {fila[0]: {"valor": fila[1], "actualizado": fila[2]} for fila in datos}


def actualizar_estado(variable, valor):
    conn = conectar()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
        UPDATE estado
        SET valor = ?, actualizado = ?
        WHERE variable = ?
        """,
        (valor, ahora, variable)
    )
    conn.commit()
    conn.close()


def registrar_evento(tipo, estado, detalle=""):
    conn = conectar()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
        INSERT INTO eventos (fecha, tipo, estado, detalle)
        VALUES (?, ?, ?, ?)
        """,
        (ahora, tipo, estado, detalle)
    )
    conn.commit()
    conn.close()


def ultimos_eventos(limite=10):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT fecha, tipo, estado, detalle
        FROM eventos
        ORDER BY id DESC
        LIMIT ?
        """,
        (limite,)
    )
    datos = cursor.fetchall()
    conn.close()
    return datos
