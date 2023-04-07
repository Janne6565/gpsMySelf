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

def convertSettingsToObject(): 
    settings = {
        "freq": controller.freq,
        "threshold": controller.threshold,
        "timeplay": controller.timeplay,
        "velocity": controller.velocity,
        "debug": controller.debug
    }
    return settings

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
    loaded = json.loads(request.args.get("settings"))
    freq = loaded['freq']
    threshold = loaded['threshold']
    timeplay = loaded['timeplay']
    velocity = loaded['velocity']
    debug = bool(loaded['debug'])
    controller.freq = freq
    controller.threshold = threshold
    controller.timeplay = timeplay
    controller.velocity = velocity
    controller.debug = debug
    return "Changed Settings"

@app.route('/getSettings')
def getSettings(): 
    return json.dumps(convertSettingsToObject())


app.run()