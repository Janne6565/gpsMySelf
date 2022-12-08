from flask import Flask, request
import allTogether

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
        sateliteNr = int(request.args.get('id'))
        if (sateliteNr > 2): 
            raise("Invalid id")
    except: 
        return "Please enter a valid id"    
    controller.calculatePoint(sateliteNr)
    return "Finished"


@app.route('/getPoints')
def returnPoints(): 
    sat = controller.calculator.satelites
    string = "{"
    for num, satt in sat.items(): 
        string += str(num) + ":{'position':{'x':" + str(satt.position.x) + ",'y':" + str(satt.position.y) + "},'distance':" + str(satt.distance) + "),"
    string += "}"
    return string

@app.route('/calculateIntersection')
def calc(): 
    return controller.getPoint(0, 1, 2)

app.run()