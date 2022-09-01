import math 

def addVector(vec1, vec2): 
    return (vec1[0] + vec2[0], vec1[1] + vec2[1])

def substractVector(vec1, vec2): 
    return (vec1[0] - vec2[0], vec1[1] - vec2[1])

def magnitudeOfVector(vec1): 
    return math.sqrt(vec1[0]**2 + vec1[1]**2)

def multiplyVector(vec1, prime): 
    return (vec1[0] * prime, vec1[1] * prime)

def divideVector(vec1, div): 
    return (vec1[0] / div, vec1[1] / div)


