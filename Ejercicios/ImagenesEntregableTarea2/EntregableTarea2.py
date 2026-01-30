from flask import Flask, request, render_template_string
import uuid
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt

app = Flask(__name__)

app.config['JWT_SECRET_KEY']='tu-clave-super-secreta-cambiar-en-produccion'
app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(minutes=15)

jwt = JWTManager(app)

host = 'mongodb+srv://juanCa15:PORT34erySADF@cluster0.fgze7ac.mongodb.net/?appName=Cluster0'
port = 27017
db_name = 'videogames_flask'
user_collection = None
videogames_collection = None

def connect_db():
    try:
        client = MongoClient(host+":"+str(port)+"/")
        db = client[db_name]
        client.admin.command('ping')
        global user_collection
        user_collection = db.users
        global videogames_collection
        videogames_collection = db.videogames
        print("✅ Conexión a MongoDB exitosa")
        print(f"DB Check : {db!=None}")        
        print(f"DB videogames_collection : {videogames_collection!=None}") 
        print(f"DB user_collection : {user_collection!=None}")         
    except Exception as e:
        pass

 # Returns list    
def check_if_user_exist(username): 
    global user_collection
    print(f"Debug username: {username}")
    query = {"username" : {"$eq": username }}
    return list(user_collection.find(query))
    
def create_user(user):
    global user_collection
    result = user_collection.insert_one(user)
    print( f"DEBUG ID value {result.inserted_id} type {type(result.inserted_id)}")
    user["_id"] = str(result.inserted_id)
    return user

def create_admin_if_exist(user):
    check_admin = check_if_user_exist(user["username"])
    if len(check_admin) > 0:
        return check_admin
    else:
        return create_user(user)

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
    html = """
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Videogames API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; background: #f6f7fb; color: #111; }
            header { padding: 36px 18px; background: linear-gradient(135deg,#111827,#1f2937); color: #fff; }
            .container { max-width: 980px; margin: 0 auto; padding: 18px; }
            .subtitle { opacity: .9; margin-top: 6px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 18px; }
            .card { background: #fff; border-radius: 14px; padding: 18px; box-shadow: 0 8px 24px rgba(17,24,39,.08); }
            .card h3 { margin: 0 0 10px 0; font-size: 18px; }
            .pill { display: inline-block; padding: 6px 10px; border-radius: 999px; background: #eef2ff; color: #3730a3; font-size: 12px; }
            .link { display: inline-block; margin-top: 10px; text-decoration: none; color: #fff; background: #4f46e5; padding: 8px 12px; border-radius: 10px; }
            .link:hover { filter: brightness(.95); }
            .hint { margin-top: 20px; padding: 14px 16px; background: #fff; border-radius: 12px; border: 1px solid #e5e7eb; }
            code { background: #111827; color: #fff; padding: 3px 7px; border-radius: 6px; font-size: 13px; }
            footer { color: #6b7280; font-size: 12px; padding: 24px 0; text-align: center; }
            ul { padding-left: 18px; }
        </style>
    </head>
    <body>
        <header>
            <div class="container">
                <h1>🎮 Videogames API</h1>
            </div>
        </header>

        <main class="container">

            <section class="hint">
                <h2>📌 ¿Qué es esta API?</h2>
                <p>
                    Esta API permite gestionar y consultar videojuegos mediante endpoints REST.
                    Algunos endpoints están protegidos con JWT y requieren rol de administrador.
                </p>
            </section>

            <section class="grid">

                <div class="card">
                    <h3>🔎 Obtener videojuegos</h3>
                    <span class="pill">GET</span>
                    <p>Listar o filtrar videojuegos disponibles.</p>
                    <p><code>/api/videogames</code></p>
                    <p><code>/api/videogames?plataforma=PS5</code></p>
                    <p>Requiere LogIn</p>
                </div>

                <div class="card">
                    <h3>🎯 Buscar por nombre</h3>
                    <span class="pill">GET</span>
                    <p>Acceder a un videojuego específico por su nombre.</p>
                    <p><code>/videogames/Minecraft</code></p>
                    <p>Requiere LogIn</p>
                </div>

                <div class="card">
                    <h3>➕ Crear videojuego</h3>
                    <span class="pill">POST</span>
                    <p>Endpoint protegido. Solo administradores.</p>
                    <p><code>/api/videogames/</code></p>
                    <p>Requiere token JWT</p>
                </div>

                <div class="card">
                    <h3>🔐 Seguridad</h3>
                    <p>Autenticación mediante JWT.</p>
                    <p>Header requerido:</p>
                    <p><code>Authorization: Bearer &lt;token&gt;</code></p>
                </div>

            </section>

            <section class="hint">
                <h3>🧪 Ejemplo rápido</h3>
                <p>
                    Prueba acceder directamente a:
                    api/videogames/
                </p>
            </section>

        </main>
    </body>
    </html>
    """

    return render_template_string(html)

"""videogames = { 
            "1": {"nombre": "EA_SPORTS_FC_25", "plataforma": "PS5", "fecha": 2024, "genero": "Deportes", "clasificacion": "+3", "precio": 280000},
            "2": {"nombre": "Grand_Theft_Auto_V", "plataforma": "PC", "fecha": 2013, "genero": "Acción/Aventura", "clasificacion": "+18","precio": 90000},
            "3": {"nombre": "It_Takes_Two", "plataforma": "PS5", "fecha": 2021, "genero": "Aventura", "clasificacion": "+12", "precio": 150000},
            "4": {"nombre": "F1_25", "plataforma": "PS5", "fecha": 2025, "genero": "Carreras", "clasificacion": "+3", "precio": 300000},
            "5": {"nombre": "Minecraft", "plataforma": "PC", "fecha": 2011, "genero": "Sandbox", "clasificacion": "+7", "precio": 120000}
            }
"""  
def normalize_id(item):
    item["_id"] = str(item["_id"])
    return item    

@app.route('/api/videogames/')
@jwt_required()
def videogames(): 
    plataforma = request.args.get("plataforma","")              
    genero = request.args.get("genero","")  
    precio_max = request.args.get("precio_max", "0")       
    query = {}

    if plataforma != "":
        query["plataforma"] = plataforma

    if genero != "":
        query["genero"] = genero

    if int(precio_max) > 0:
        query["precio"] = {"$lte": int(precio_max)}

    global videogames_collection
    result = list(videogames_collection.find(query))

    results = list(map(lambda vg: normalize_id(vg), result))

    return results, 200

def insert_videogame(body):
    global videogames_collection    
    result = videogames_collection.insert_one(body)
    body["_id"] = str(result.inserted_id)
    return body


@app.route('/api/agregar_videogames/', methods = ["POST"])
@admin_required
def post_videogames():
    return insert_videogame(request.json), 200    
    
@app.route('/api/videogames/<string:id>',methods = ["GET", "DELETE"])
@jwt_required()
def get_videogames(id):
    print(f"METHOD {request.method}")
    global videogames_collection
    found = videogames_collection.find_one({"_id": ObjectId(id)})
    found["_id"] = str(found["_id"])
    if request.method == "GET":        
        if id is not None:
            return found, 200
        else:
            return {"messsage": "videogame with "+id+" not found"}, 404       
    else:
        if id is not None:
            videogames_collection.delete_one({"_id": ObjectId(id)})
            return found , 200
        else:
            return {}, 204
        
@app.route('/api/admin/signIn/admin', methods= ['POST'])
@jwt_required()
def sign_in_admin():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return {
            "error": "Acceso denegado",
            "message": "Solo un administrador puede crear otro administrador"
        }, 403
    
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos inválidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        password = request.json['password']
        if len(check_if_user_exist(username) ) >0:
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
                'role': 'admin'
            }
            user_created = create_user(new_user)
            
            return { 'username': username, '_id': user_created["_id"], 'role': 'admin'}, 201

@app.route('/api/admin/signIn/manager', methods= ['POST'])
def sign_in_manager():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos inválidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        password = request.json['password']
        role = request.json['role']
        if len(check_if_user_exist(username) ) >0:
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
            user_created = create_user(new_user)
            
            return { 'username': username, '_id': user_created["_id"], 'role': 'manager'}, 201

@app.route('/api/signIn', methods= ['POST'])
def sign_in_user():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos inválidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        password = request.json['password']
        if len(check_if_user_exist(username) ) >0:
            return {
            'error': 'Datos inválidos',
            'message': 'el usuario ya existe'}, 400
        else:
            new_user = {
                'username': username,
                'password_hash': generate_password_hash(password),
                'created_at': datetime.now(),
                'role': 'user'
            }
            user_created = create_user(new_user)
            
            return { 'username': username, '_id': user_created["_id"], 'role': 'user'}, 201

@app.route('/api/login', methods= ['POST'])
def log_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos inválidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        body_password = request.json['password']
        if len(check_if_user_exist(username) ) == 0:
            return {
            'error': 'Datos inválidos',
            'message': 'el usuario no existe'}, 400
        else:
            user = check_if_user_exist(username)[0]
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
    connect_db()
    admin_user =    {
                'username': "admin",
                'password_hash': generate_password_hash('123456'),
                'created_at': datetime.now(),
                'role': "admin"
            }
    print( f"Admin user: {create_admin_if_exist(admin_user)}")
    app.run(debug=True,
            port=8002, 
            host='0.0.0.0')