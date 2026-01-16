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

pets = {"Tito":{"especie": "Hamster", "edad": 2},
        "Lorenzo":{"especie": "Gato", "edad": 8},
        "Caramelo":{"especie": "Perro", "edad": 7}}

@app.route("/pets/<string:name>/")

def get_pets(name):
    if name in pets:
        return pets[name], 200
    else:
        return {"message": "Pet not found"}, 404
if __name__ == '__main__':
    app.run(debug=True,
            port=8002,
            host='0.0.0.0')