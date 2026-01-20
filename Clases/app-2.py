from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "<h1>Hola mundo</h1>"

@app.route('/hello/<string:name>')
def grettings(name):
    return "<h1>Hola mundo " + name + "</h1>"

saludo = {"ES": "Hola mundo",
          "EN": "Hello world"}

@app.route('/dynamic/<string:name>/')
def data(name):
    language = request.args.get("language", "EN")
    uppercase = request.args.get("uppercase", False)
    phase = saludo[language] + " " + name
    if bool(uppercase):
        phase = phase.upper()
    return "<h1>" + phase + "<h1>"

furnitures = {"1": {"name": "Mesa redonda", "width": 150, "depth": 150, "heigh": 150, "price": 110000},
              "2": {"name": "Mesa rectangular", "width": 150, "depth": 60, "heigh": 120, "price": 120000},
              "3": {"name": "Silla triangular", "width": 85, "depth": 65, "heigh": 130, "price": 60000}}

@app.route('/api/furnitures/<string:id>/', methods = ["GET"])
def get_furniture(id):
    if id in furnitures:
        return furnitures[id], 200
    else:
        return {"message": "forniture with" + id + "not found"}, 404
    
@app.route('/api/furnitures/')
def get_furnitures():
    width = request.args.get("width", 0)
    heigh = request.args.get("heigh", 0)
    filtered = list(filter(lambda key : furnitures[key]["width"] >= int(width) and furnitures[key]["heigh"] >= int(heigh), furnitures))
    return list(map(lambda k : furnitures[k], filtered))

@app.route('/api/furniture/', methods = ["POST"])
def post_furnitures():
    body = request.json
    copy = body.copy()
    new_id = body["id"]
    del body["id"]
    furnitures[new_id] = body
    return copy, 201

if __name__ == '__main__':
    app.run(debug=True,
            port=8002,
            host='0.0.0.0')