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

def inicializar_tabla_alarmas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alarmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            nivel TEXT NOT NULL,
            codigo TEXT NOT NULL,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            activa INTEGER DEFAULT 1,
            correo_enviado INTEGER DEFAULT 0,
            fecha_resolucion TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def obtener_alarma_activa(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, fecha, nivel, codigo, titulo, descripcion, activa, correo_enviado
        FROM alarmas
        WHERE codigo = ? AND activa = 1
        ORDER BY id DESC
        LIMIT 1
        """,
        (codigo,)
    )
    alarma = cursor.fetchone()
    conn.close()
    return alarma


def crear_alarma_bd(nivel, codigo, titulo, descripcion):
    conn = conectar()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
        INSERT INTO alarmas (fecha, nivel, codigo, titulo, descripcion, activa, correo_enviado)
        VALUES (?, ?, ?, ?, ?, 1, 0)
        """,
        (ahora, nivel, codigo, titulo, descripcion)
    )
    conn.commit()
    conn.close()


def marcar_correo_alarma_enviado(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE alarmas
        SET correo_enviado = 1
        WHERE codigo = ? AND activa = 1
        """,
        (codigo,)
    )
    conn.commit()
    conn.close()


def resolver_alarma_bd(codigo):
    conn = conectar()
    cursor = conn.cursor()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
        UPDATE alarmas
        SET activa = 0, fecha_resolucion = ?
        WHERE codigo = ? AND activa = 1
        """,
        (ahora, codigo)
    )
    conn.commit()
    conn.close()


def alarmas_activas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT fecha, nivel, codigo, titulo, descripcion
        FROM alarmas
        WHERE activa = 1
        ORDER BY id DESC
        """
    )
    datos = cursor.fetchall()
    conn.close()
    return datos
