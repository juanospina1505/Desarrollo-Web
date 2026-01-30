from flask import Flask, request
import uuid
#import os
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt
#from dotenv import load_dotenv

app = Flask(__name__)

#load_dotenv()

app.config['JWT_SECRET_KEY'] = 'tu-clave-super-secreta-cambiar-en-produccio'

#app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)

jwt = JWTManager(app)
host = 'mongodb+srv://juanCa15:PORT34erySADF@cluster0.fgze7ac.mongodb.net/?appName=Cluster0'
port = 27017
db_name = 'furniture_flask'
# admin , manager , user
user_collection = None
furniture_collection = None

def connect_db():
    try:
        client = MongoClient(host+":"+str(port)+"/")
        db = client[db_name]
        client.admin.command('ping')
        global user_collection
        user_collection = db.users
        global furniture_collection
        furniture_collection = db.furnitures
        print("✅ Conexión a MongoDB exitosa")
        print(f"DB Check : {db!=None}")        
        print(f"DB furniture_collection : {furniture_collection!=None}") 
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
        return claims.get('role','user')
    except:
        return None
    

def manager_required(f):
    @jwt_required()
    def custom_validation(*args,**kwargs):
        role = get_token_role()
        if role == 'manager' or role == 'admin':
            return f(*args,**kwargs)
        else:
            print(f"Debug Role: {role}")
            return {
                'error': 'Acceso denegado',
                'message': 'Solo los manager pueden acceder a este endpoint'
            }, 403
    return custom_validation         
        


@app.route('/')
def hello():
    return "<h1> Hola Mundo </h1>"

@app.route('/hello/<string:name>')
def grettings(name):
    return "<h1> Hola Mundo "+ name +  "</h1>"

saludo = {"ES": "Hola Mundo",
          "EN": "Hello World"}

@app.route('/dynamic-hello/<string:name>/')
def data(name):
    language = request.args.get("language", "EN")
    uppercase = request.args.get("uppercase", False)
    phase = saludo[language] + " " + name
    if uppercase == "True" or uppercase == "true":
        phase = phase.upper()
    return "<h1>" + phase + "</h1>"

#furnitures = { "1": {"name": "Mesa Redonda", "width": 150 , "depth": 150 , "heigh": 150, "price": 110000},
#        "2": {"name": "Mesa Rectangular", "width": 150 , "depth": 60 , "heigh": 120, "price": 120000},
#        "3": {"name": "Silla triangular", "width": 85 , "depth": 65 , "heigh": 130, "price": 60000} }


@app.route('/api/furniture/<string:id>/',methods = ["GET", "DELETE"])
@jwt_required()
def get_furniture(id):   
    print(f"METHOD {request.method}")
    global furniture_collection
    found = furniture_collection.find_one({"_id": ObjectId(id)})
    found["_id"] = str(found["_id"])
    if request.method == "GET":        
        if id is not None:
            return found, 200
        else:
            return {"messsage": "furniture with "+id+" not found"}, 404
    else:
        if id is not None:
            furniture_collection.delete_one({"_id": ObjectId(id)})
            return found , 200
        else:
            return {}, 204

def normalize_id(item):
    item["_id"] = str(item["_id"])
    return item    

@app.route('/api/furnitures/')
@jwt_required()
def get_furnitures(): 
    width = request.args.get("width",0)
    heigh =  request.args.get("heigh",0)   
    query = {"width" : {"$gte": int(width) },
             "heigh" : {"$gte": int(heigh) }}
    global furniture_collection    
    result = list(furniture_collection.find(query))
    results = list(map(lambda fur: normalize_id(fur), result))
    return result, 200

def insert_furniture(body):
    global furniture_collection    
    result = furniture_collection.insert_one(body)
    body["_id"] = str(result.inserted_id)
    return body

@app.route('/api/furniture/', methods = ["POST"])
@manager_required
def post_furnitures():   
    return insert_furniture(request.json), 200    
 
@app.route('/api/furniture/<string:id>/', methods=["PATCH"])
@jwt_required()
def put_furniture(id):
    body = request.json
    price = body.get("price")
    name = body.get("name")
    found = furniture_collection.find_one({"_id": ObjectId(id)})
    query = {"$set":{}}
    if found is not None:
        if price != None:
            query["$set"]["price"] = price
        if name != None:
            query["$set"]["name"] = name
        furniture_collection.update_one({"_id": ObjectId(id)}, query)
        found = furniture_collection.find_one({"_id": ObjectId(id)})
        found["_id"] = str(found["_id"])
        return found , 200
    else:
        return {"messsage": "furniture with "+id+" not found"}, 404
    
@app.route('/api/admin/signIn/manager', methods= ['POST'])
#manager_required
def admin_sign_in():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return { 'error': 'Datos inválidos', 
                'message': 'Se requieren username y password'}, 400
    else:
        username = request.json['username']
        password = request.json['password']
        if len(check_if_user_exist(username)) >0:
            return {
            'error': 'Datos inválidos',
            'message': 'el usuario ya existe'}, 400
        else:
            new_user = {
                'username': username,
                'password_hash': generate_password_hash(password),
                'created_at': datetime.now(),
                'role': 'manager'
            }
            user_created = create_user(new_user)
            
            return { 'username': username, '_id': user_created["_id"], 'role': 'manager'}, 201
   

@app.route('/api/signIn', methods= ['POST'])
def sign_in():
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
                'role': 'client'
            }
            user_created = create_user(new_user)
            
            return { 'username': username, '_id': user_created["_id"], 'role': 'client'}, 201

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
                token = create_access_token(identity=username,additional_claims={
                    "user_id" : user.get('user_id'),
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