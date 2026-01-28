from flask import Flask, request
import uuid
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt

app = Flask(__name__)

app.config['JWT_SECRET_KEY']='tu-clave-super-secreta-cambiar-en-produccion'
app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(minutes=15)

jwt = JWTManager(app)

def get_token_role():
    try:
        claims = get_jwt()
        return claims.get('role', 'user')
    except:
        return None

def admin_required(f):
    @jwt_required()
    def custom_validation(*args, **kwargs):
        role = get_token_role()
        if role == 'admin':
            return f(*args, **kwargs)
        else:
            print(f"Debug Role: {role}")
            return {
                'error': 'Acceso denegado',
                'message': 'Solo los admin pueden acceder a este endpoint'
            }, 403
    return custom_validation
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
@jwt_required()
def get_videogame(name):
    for videogame in videogames.values():
        if videogame["nombre"] == name:
            return videogame, 200

    return {"message": "Videogame not found"}, 404

@app.route('/api/filter_videogames/')
@jwt_required()
def filter_videogames(): 
    plataforma = request.args.get("plataforma","")              
    genero = request.args.get("genero","")  
    precio_max = request.args.get("precio_max", "")       
    filtered = list(filter(lambda key:(plataforma == "" or videogames[key]["plataforma"] == plataforma)
            and (genero == "" or videogames[key]["genero"] == genero)
            and (precio_max == "" or videogames[key]["precio"] <= int(precio_max)),videogames))
    
    return list(map(lambda k: videogames[k], filtered))

@app.route('/api/videogames/', methods = ["POST"])
@admin_required
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
    
@app.route('/api/videogames/',methods = ["GET", "DELETE"])
@jwt_required()
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

users = [
            {
                'user_id': "admin-1234",
                'username': "admin",
                'password_hash': generate_password_hash('123456'),
                'created_at': datetime.now(),
                'role': "admin"
            }
        ]

def get_users_by_username(username):
    return list(filter(lambda u: u["username"]== username, users))

@app.route('/api/admin/signIn/manager', methods= ['POST'])
def sign_in_manager():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos inválidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        password = request.json['password']
        role = request.json['role']
        if len(get_users_by_username(username) ) >0:
            return {
            'error': 'Datos inválidos',
            'message': 'el usuario ya existe'}, 400
        else:
            user_id = 'user-'+str(uuid.uuid4())
            new_user = {
                'user_id': user_id,
                'username': username,
                'password_hash': generate_password_hash(password),
                'created_at': datetime.now(),
                'role': 'manager'
            }
            users.append(new_user)
            return { 'username': username, 'user_id': user_id,'role': role}, 201

@app.route('/api/signIn', methods= ['POST'])
def sign_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos inválidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        password = request.json['password']
        role = request.json['role']
        if len(get_users_by_username(username) ) >0:
            return {
            'error': 'Datos inválidos',
            'message': 'el usuario ya existe'}, 400
        else:
            user_id = 'user-'+str(uuid.uuid4())
            new_user = {
                'user_id': user_id,
                'username': username,
                'password_hash': generate_password_hash(password),
                'created_at': datetime.now(),
                'role': 'user'
            }
            users.append(new_user)
            return { 'username': username, 'user_id': user_id,'role': role}, 201
        
@app.route('/api/login', methods= ['POST'])
def log_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos inválidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        body_password = request.json['password']
        if len(get_users_by_username(username) ) == 0:
            return {
            'error': 'Datos inválidos',
            'message': 'el usuario no existe'}, 400
        else:
            user = get_users_by_username(username)[0]
            user_password = user["password_hash"]
            if check_password_hash(user_password, body_password):
                token = create_access_token(identity=username, additional_claims={
                    "user_id": user.get('user_id'),
                    "role": user.get('role')
                })
                return { 'message': "login correcto",
                        'token': token}, 200
            else:
                 return { 'message': "contraseña incorrecta"}, 401
            
if __name__ == '__main__':
    app.run(debug=True,
            port=8002, 
            host='0.0.0.0')