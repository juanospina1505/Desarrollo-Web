from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    #mensaje = "<h1>Bienvenido, para acceder a un video juego añade a la URL \"/videogames/nombre_videjuego\"</h1>\n<h2>Opciones:</h2>\n<h3> - /videogames/FC25</h3><h3>\n - /videogames/GTAV</h3><h3> - /videogames/It_Takes_Two</h3><h3>\n - /videogames/F125</h3>"
    mensaje = """
                <h1>Bienvenido, para acceder a un video juego añade a la URL \"/videogames/nombre_videjuego\"</h1>
                <h2>Videojuegos disponibles:</h2>
                <ul>
                    <h3>- /videogames/FC25</h3>
                    <h3>- /videogames/GTAV</h3>
                    <h3>- /videogames/It_Takes_Two</h3>
                    <h3>- /videogames/F125</h3>
                </ul>
            """

    return mensaje

videogames = {"FC25": {"plataforma": "PS5", "Fecha": 2024},
               "GTAV": {"plataforma": "PC", "Fecha": 2013},
               "It_Takes_Two": {"plataforma": "PS5", "Fecha": 2021},
               "F125": {"plataforma": "PS5", "Fecha": 2025}}

@app.route("/videogames/<string:name>/")

def get_pets(name):
    if name in videogames:
        return videogames[name], 200
    else:
        return {"message": "Videogame not found"}, 404
if __name__ == '__main__':
    app.run(debug=True,
            port=8002,
            host='0.0.0.0')