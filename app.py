from flask import Flask, render_template, redirect, url_for
import requests
import os

app = Flask(__name__)

API_URL = "https://randomuser.me/api/"

# Página principal  
@app.route("/")
def index():
    return render_template("index.html")


# Petición a la API y renderizado de la página con los resultados
@app.route("/generar", methods=["POST"])
def generar():
    try:
        response = requests.get("https://randomuser.me/api/")
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return render_template("index.html", error=f"Error al consultar la API: {e}")

    resultado = data["results"][0]

    genero=""
    if resultado["gender"] == "male":
        genero = "Masculino"
    else:
        genero = "Femenino"


    persona = {
        "imagen": resultado["picture"]["large"],
        "gen": genero,
        "edad": resultado["dob"]["age"],
        "pais": resultado["location"]["country"],
        "correo": resultado["email"],
        "telefono": resultado["phone"],
        "direccion": resultado["location"]["city"]+ ", "+resultado["location"]["country"],
        "nombre": f"{resultado['name']['title']} {resultado['name']['first']} {resultado['name']['last']}",
    }

    return render_template("persona.html", persona=persona)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=8000)
