import math



def useABC(a, b, c, debug):
    results = [] 
    for neg in [1, -1]: 
        inSqrt = b**2-4*a*c
        if (inSqrt < 0):
            raise(Exception("Cant use sqrt on numbers < 0"))
        top = b * -1 + (neg*(math.sqrt(inSqrt))) 
        bot = 2*a
        results.append(top/bot)

    return results

def calculateWithAxys0(c1, c2, debug): 
    xr = c1[0][0] - c2[0][0]
    yr = c1[0][1] - c2[0][1]
    r1 = c1[1]
    r2 = c2[1]

    # Wenn eine Achse = 0 (sonst 0 division)
    if (xr == 0 and yr != 0):
        xy = [xr, yr]
    elif (yr == 0 and xr != 0): 
        xy = [yr, xr]
    else: 
        circlesSameSpot(c1, c2, debug)
    
    if (math.sqrt(xr ** 2 + yr ** 2) > r1 + r2):
        raise("Circles are too far apart")

    y = (r2**2-r1**2-xy[1]**2)/(2*xy[1]) 
    xVals = []
    for val in [1, -1]: 
        xVals.append(val * math.sqrt(r1**2-y**2))
    
    if (yr == 0):
        return [(y, xVals[0]), (y, xVals[1])]
    else: 
        return [(xVals[0], y), (xVals[1], y)]
    

def circlesSameSpot(c1, c2, debug): 
    if (c1 == c2): 
        raise("Circles are equal")
    else: 
        raise("Circles are not touching")


def calculateIntersections(c1, c2, debug): # Input should look like this: (((x1, y1), r1), ((x2, y2), r1))
    xr = c1[0][0] - c2[0][0] # Relative Koordinaten, zur vereinfachung des Problems
    yr = c1[0][1] - c2[0][1] 
    r1 = c1[1]
    r2 = c2[1] 

    if (xr == 0 and yr == 0): 
        return circlesSameSpot(c1, c2, False)
    
    if (math.sqrt(xr**2 + yr**2) > r1 + r2):  # Punkte zu weit entfernt 
        raise("Circles are too far apart") 

    if (xr == 0 or yr == 0):
        return calculateWithAxys0(c1, c2, debug)
    
    resultForX = []
    resultForY = []
    for xy in [(xr, yr, resultForX), (yr, xr, resultForY)]: 
        d = (r2**2-r1**2)-xy[0]**2-xy[1]**2
        a = 1 + (xy[0]**2)/(xy[1]**2)   
        b = -((d * xy[0])/(xy[1]**2))
        c = (d**2)/(4*xy[1]**2)-(r1**2)
        xy[2].append(useABC(a, b, c, debug))
    
    resultForX = resultForX[0]
    resultForY = resultForY[0]
    points = []
    for i in range(len(resultForX)): 
        if (xr > 0 and yr > 0 or xr < 0 and yr < 0):
            points.append((resultForX[i], resultForY[len(resultForY) - i - 1]))
        else: 
            points.append((resultForX[i], resultForY[i]))
    

    return points
