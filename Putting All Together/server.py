from flask import Flask, request
import allTogether, distanceCalculator, json
from threading import Thread

app = Flask(__name__)



class DistanceThreader: 
    result = -1
    finished = False
    
    def calcPoint(self):
        aud = distanceCalculator.AudioListener()
        self.result = aud.getDistanceToSpeaker(10000, True, 2, 334, 0.003)
        self.finished = True
        print("Finished the Thread")
    
    def startCalc(self): 
        thread = Thread(target=self.calcPoint)
        thread.start()
        print("Finished starting the Thread")



@app.route('/test')
def test():
    return "Hallo mein name ist janne"

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
holder = DistanceThreader()

@app.route('/getSound')
def getSound(): 
    if (holder.finished):
        return str(holder.result)
    else: 
        return "Not finished yet"

@app.route('/resetResult')
def resetResult(): 
    holder.result = None
    holder.finished = False
    return ""

@app.route('/makeSound')
def calcPoints(): 
    holder.startCalc()
    
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

app.run()


