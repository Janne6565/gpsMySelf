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
        print(inSqrt, top, bot, top/bot)

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

def testNewCalculation(c1, c2): 
    xr = c1[0][0] - c2[0][0]
    yr = c1[0][1] - c2[0][1]
    r1 = c1[1]
    r2 = c2[1]
    print(xr, yr, r1, r2)

    if (xr == 0 and yr == 0):
        return circlesSameSpot(c1, c2, False)
    
    if (math.sqrt(xr**2 + yr**2) > r1 + r2):  # Punkte zu weit entfernt 
        raise("Circles are too far apart") 

    d = (r2**2 - r1**2 - xr**2 - yr**2) / (2 * xr)
    a = 1 + (yr**2) / (xr**2)
    b = -2 * (d * yr) / xr
    c = d**2 - r1**2

    y = useABC(a, b, c, False)

    d = (r2**2 - r1**2 - xr**2 - yr**2) / (2 * yr)
    a = 1 + (xr**2) / (yr**2)
    b = -2 * (d * xr) / yr
    c = d**2 - r1**2

    x = useABC(a, b, c, False)
    realX = []
    for i in x:
        realX.append((i + c1[0][0]))
    
    realY = []
    for i in y:
        realY.append((i + c1[0][1]))

    return (realX, realY)



# print(testNewCalculation(((634, 584), 374), ((960, 120), 280)))
print(useABC(3.0208573625528645, 1671.6755094194543, 205314.1468665898, False))