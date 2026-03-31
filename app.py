from flask import Flask, render_template, request
import os
import urllib.parse

app = Flask(__name__)

NUMERO_WHATSAPP = "50689872394"  # 👈 TU NÚMERO


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/reserva", methods=["GET", "POST"])
def reserva():
    fechas_ocupadas = set()
    mensaje = ""
    link_whatsapp = ""

    # leer reservas
    if os.path.exists("reservas.txt"):
        with open("reservas.txt", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split(" - ")
                if len(partes) == 2:
                    fechas_ocupadas.add(partes[1])

    if request.method == "POST":
        nombre = request.form["nombre"]
        fecha = request.form["fecha"]

        if fecha in fechas_ocupadas:
            mensaje = "❌ Lo sentimos, esta fecha ya está reservada"
        else:
            with open("reservas.txt", "a") as archivo:
                archivo.write(f"{nombre} - {fecha}\n")

            mensaje = "✅ Reserva guardada correctamente"

            mensaje_whatsapp = f"Hola soy {nombre} y quiero confirmar mi reserva para {fecha}"
            link_whatsapp = f"https://wa.me/{NUMERO_WHATSAPP}?text={urllib.parse.quote(mensaje_whatsapp)}"

    return render_template(
        "reserva.html",
        fechas=sorted(fechas_ocupadas),
        mensaje=mensaje,
        link_whatsapp=link_whatsapp
    )


if __name__ == "__main__":
    app.run(debug=True)
