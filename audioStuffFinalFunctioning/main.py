import distanceCalculator, trilateration, math, pyaudio

class Position:
     
    x = 0
    y = 0

    def __init__(self, posX, posY): 
        self.x = posX
        self.y = posY



class Satelite: 

    distance = 0
    position = Position(0,0)

    def setPosition(self, value): 
        self.position = value

    def setDistance(self, value): 
        self.distance = value

class Calculator: 

    satelites = {0: Satelite(), 1: Satelite(), 2: Satelite()}

    def setSatelitePosition(self, sateliteNr, satelitePosition):
        self.satelites[sateliteNr].setPosition(satelitePosition)
        return self

    def setSateliteDistance(self, sateliteNr, distance): 
        self.satelites[sateliteNr].setDistance(distance)
        return self
    
    def calculate(self, num1, num2, num3): 
        satelite1Compare = ((self.satelites[num1].position.x, self.satelites[num1].position.y), self.satelites[num1].distance)
        satelite2Compare = ((self.satelites[num2].position.x, self.satelites[num2].position.y), self.satelites[num2].distance)
        points = trilateration.calculateIntersections(satelite1Compare, satelite2Compare, False)

        lowestDistance = -1
        lowestPoint = (0, 0)

        print(points)
        for point in points: 
            satelite3Compare = self.satelites[num3]
            distance = math.sqrt((satelite3Compare.position.x - point[0])**2 + (satelite3Compare.position.y - point[1])**2)
            if (abs(distance - satelite3Compare.distance) < lowestDistance or lowestDistance == -1):
                lowestDistance = distance
                lowestPoint = point

        return lowestPoint


class Controller: 
    calculator = Calculator()

    def calculatePoint(indexOfPoint): 
        audio = distanceCalculator.AudioListener() 
        calculator.setSateliteDistance(indexOfPoint, audio.getDistanceToSpeaker(10000, True, 2, 334, 0.003))
    
    def setPosition(indexOfSatelite, position):
        calculator.setSatelitePosition(indexOfSatelite, position)

    def getPoint():
        calculator.calculate()


if __name__ == '__main__':
    calculator = Calculator()
    calculator.setSatelitePosition(0, Position(0, 0))
    calculator.setSatelitePosition(1, Position(0, 1))
    calculator.setSatelitePosition(2, Position(-1, 3))
    calculator.setSateliteDistance(0, 2)
    calculator.setSateliteDistance(1, 1)
    calculator.setSateliteDistance(2, 5)
    print(calculator.calculate(0, 1, 2))