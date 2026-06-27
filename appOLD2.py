from flask import Flask, render_template, redirect, url_for, jsonify
from database import obtener_estado, ultimos_eventos, actualizar_estado, registrar_evento
from sensores_gpio import leer_nivel_agua, activar_trasvase, parar_trasvase

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/estado")
def api_estado():
    nivel = leer_nivel_agua()
    estado_actual = obtener_estado()

    bloqueo = estado_actual["bloqueo"]["valor"]

    actualizar_estado("nivel_agua", nivel)

    if bloqueo != "SI":
        if nivel == "BAJO":
            activar_trasvase()
            actualizar_estado("trasvase", "ACTIVO")
        else:
            parar_trasvase()
            actualizar_estado("trasvase", "PARADO")
    else:
        parar_trasvase()
        actualizar_estado("trasvase", "PARADO")

    return jsonify({
        "estado": obtener_estado(),
        "eventos": ultimos_eventos(8)
    })


@app.route("/accion/iniciar_trasvase")
def iniciar_trasvase():
    actualizar_estado("trasvase", "ACTIVO")
    registrar_evento("TRASVASE", "INICIADO MANUAL", "Orden manual desde pantalla")
    return redirect(url_for("index"))


@app.route("/accion/parar_trasvase")
def parar_trasvase():
    actualizar_estado("trasvase", "PARADO")
    registrar_evento("TRASVASE", "PARADO MANUAL", "Parada manual desde pantalla")
    return redirect(url_for("index"))


@app.route("/accion/bloquear")
def bloquear():
    actualizar_estado("bloqueo", "SI")
    registrar_evento("SISTEMA", "BLOQUEADO", "Bloqueo manual")
    return redirect(url_for("index"))


@app.route("/accion/desbloquear")
def desbloquear():
    actualizar_estado("bloqueo", "NO")
    registrar_evento("SISTEMA", "DESBLOQUEADO", "Desbloqueo manual")
    return redirect(url_for("index"))


@app.route("/test/nivel_bajo")
def test_nivel_bajo():
    actualizar_estado("nivel_agua", "BAJO")
    registrar_evento("NIVEL_AGUA", "BAJO", "Prueba manual desde web")
    return redirect(url_for("index"))


@app.route("/test/nivel_correcto")
def test_nivel_correcto():
    actualizar_estado("nivel_agua", "CORRECTO")
    registrar_evento("NIVEL_AGUA", "CORRECTO", "Prueba manual desde web")
    return redirect(url_for("index"))


@app.route("/test/riego_on")
def test_riego_on():
    actualizar_estado("riego", "ACTIVO")
    registrar_evento("RIEGO", "INICIADO", "Prueba manual desde web")
    return redirect(url_for("index"))


@app.route("/test/riego_off")
def test_riego_off():
    actualizar_estado("riego", "PARADO")
    registrar_evento("RIEGO", "FINALIZADO", "Prueba manual desde web")
    return redirect(url_for("index"))


@app.route("/reset_bloqueo")
def reset_bloqueo():
    actualizar_estado("bloqueo", "NO")
    registrar_evento("SISTEMA", "RESET", "Bloqueo reseteado manualmente")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
