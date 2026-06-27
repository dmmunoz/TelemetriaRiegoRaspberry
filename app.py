from flask import Flask, render_template, redirect, url_for, jsonify

from database import obtener_estado, ultimos_eventos, actualizar_estado, registrar_evento
from control import ciclo_control
from sensores_gpio import activar_salida_trasvase, parar_salida_trasvase

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/estado")
def api_estado():
    ciclo_control()

    return jsonify({
        "estado": obtener_estado(),
        "eventos": ultimos_eventos(8)
    })


@app.route("/accion/iniciar_trasvase")
def iniciar_trasvase():
    activar_salida_trasvase()
    actualizar_estado("trasvase", "ACTIVO")
    registrar_evento("TRASVASE", "INICIADO MANUAL", "Orden manual desde pantalla")
    return redirect(url_for("index"))


@app.route("/accion/parar_trasvase")
def parar_trasvase():
    parar_salida_trasvase()
    actualizar_estado("trasvase", "PARADO")
    registrar_evento("TRASVASE", "PARADO MANUAL", "Parada manual desde pantalla")
    return redirect(url_for("index"))


@app.route("/accion/bloquear")
def bloquear():
    parar_salida_trasvase()
    actualizar_estado("trasvase", "PARADO")
    actualizar_estado("bloqueo", "SI")
    registrar_evento("SISTEMA", "BLOQUEADO", "Bloqueo manual")
    return redirect(url_for("index"))


@app.route("/accion/desbloquear")
def desbloquear():
    actualizar_estado("bloqueo", "NO")
    registrar_evento("SISTEMA", "DESBLOQUEADO", "Desbloqueo manual")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
