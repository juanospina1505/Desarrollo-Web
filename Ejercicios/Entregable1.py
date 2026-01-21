from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    #mensaje = "<h1>Bienvenido, para acceder a un video juego añade a la URL \"/videogames/nombre_videjuego\"</h1>\n<h2>Opciones:</h2>\n<h3> - /videogames/FC25</h3><h3>\n - /videogames/GTAV</h3><h3> - /videogames/It_Takes_Two</h3><h3>\n - /videogames/F125</h3>"
    mensaje = """
                <h1>Bienvenido, para acceder a un video juego añade a la URL \"/videogames/nombre_videjuego\"</h1>
                <h2>Videojuegos disponibles:</h2>
                <ul>
                    <h3>- /videogames/EA_SPORTS_FC_25</h3>
                    <h3>- /videogames/Grand_Theft_Auto_V</h3>
                    <h3>- /videogames/It_Takes_Two</h3>
                    <h3>- /videogames/F1_25</h3>
                    <h3>- /videogames/Minecraft</h3>
                </ul>
            """

    return mensaje

videogames = { 
            "1": {"nombre": "EA_SPORTS_FC_25", "plataforma": "PS5", "fecha": 2024, "genero": "Deportes", "clasificacion": "+3", "precio": 280000},
            "2": {"nombre": "Grand_Theft_Auto_V", "plataforma": "PC", "fecha": 2013, "genero": "Acción/Aventura", "clasificacion": "+18","precio": 90000},
            "3": {"nombre": "It_Takes_Two", "plataforma": "PS5", "fecha": 2021, "genero": "Aventura", "clasificacion": "+12", "precio": 150000},
            "4": {"nombre": "F1_25", "plataforma": "PS5", "fecha": 2025, "genero": "Carreras", "clasificacion": "+3", "precio": 300000},
            "5": {"nombre": "Minecraft", "plataforma": "PC", "fecha": 2011, "genero": "Sandbox", "clasificacion": "+7", "precio": 120000}
            }

@app.route("/videogames/<string:name>/")

def get_videogame(name):
    for videogame in videogames.values():
        if videogame["nombre"] == name:
            return videogame, 200

    return {"message": "Videogame not found"}, 404

@app.route('/api/videogames/',methods = ["GET", "DELETE"])
def get_videogames():   
    videogame_id = request.args.get("id", "")
    print(f"METHOD {request.method}")
    if request.method == "GET":
        return videogames, 200  
    else:
        if videogame_id in videogames:
            element = videogames[videogame_id]
            del videogames[videogame_id]
            return element , 200
        else:
            return {}, 204      

@app.route('/api/filter_videogames/')
def filter_videogames(): 
    plataforma = request.args.get("plataforma","")              
    genero = request.args.get("genero","")  
    precio_max = request.args.get("precio_max", "")       
    filtered = list(filter(lambda key:(plataforma == "" or videogames[key]["plataforma"] == plataforma)
            and (genero == "" or videogames[key]["genero"] == genero)
            and (precio_max == "" or videogames[key]["precio"] <= int(precio_max)),videogames))
    
    return list(map(lambda k: videogames[k], filtered))

@app.route('/api/videogames/', methods = ["POST"])
def post_videogames():
    body = request.json
    copy = body.copy()
    new_id = body["id"]
    if new_id in videogames:
        return {"message": "videogame with id "+ new_id + " already exist" }, 409    
    else:
        del body["id"]
        videogames[new_id] = body   
        return copy, 201

if __name__ == '__main__':
    app.run(debug=True,
            port=8002, 
            host='0.0.0.0')
