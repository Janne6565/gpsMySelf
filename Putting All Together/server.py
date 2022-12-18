from flask import Flask, request
import allTogether, distanceCalculator, json

app = Flask(__name__)

@app.route('/')
def index():
    return open("index.html","r").read()


@app.route('/style.css')
def style(): 
    return open("style.css", "r").read()


@app.route('/app.js')
def runCommand(): 
    return open("app.js", "r").read()

@app.route('/vue.js')
def vueJs():
    return open("vue.js", "r").read()


controller = allTogether.Controller()

@app.route('/makeSound')
def calcPoints(): 
    try: 
        satelite = int(request.args.get("id"))
        if (satelite > 2 or satelite < 0): 
            raise("Not a valid number")
    except: 
        return "Not a valid number"
    controller.calculatePoint(satelite)
    return "Finished"

@app.route('/getPoints')
def returnPoints(): 
    sat = controller.calculator.satelites
    string = "{"
    for num, satt in sat.items(): 
        string += str(num) + ":{'position':{'x':" + str(satt.position.x) + ",'y':" + str(satt.position.y) + "},'distance':" + str(satt.distance) + "},"
    string += "}"
    return string

@app.route('/calculateIntersection')
def calc(): 
    return controller.getPoint(0, 1, 2)

@app.route('/setSettings')
def setSettings(): 
    json = json.loads(request.args.get("settings"))
    freq = json['freq']
    threshold = json['threshold']
    timeplay = json['timeplay']
    velocity = json['velocity']
    debug = bool(json['debug'])
    controller.calculator.freq = freq
    controller.calculator.threshold = threshold
    controller.calculator.timeplay = timeplay
    controller.calculator.velocity = velocity
    controller.calculator.debug = debug


app.run()


